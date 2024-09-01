import pandas as pd
import numpy as np
from src.config import get_database_path, get_sales_bias, get_price_bias, get_store_sales_bias
from src.models.recommendation_model import Recommendation

class RecommendationsService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RecommendationsService, cls).__new__(cls, *args, **kwargs)
            cls._instance.initialize()
        return cls._instance

    def initialize(self) -> None:
        """
        Initializes the RecommendationsService by loading data and setting up bias factors.

        This method reads the sales data from a CSV file, calculates sales per product and per store,
        applies sales and price biases, and prepares the combined score for products based on price
        and store sales.
        """
        self.sales_df = pd.read_csv(get_database_path())
        self.sales_per_product = self.sales_df.groupby(by=['product_id']).agg({'sales_per_day': 'sum'}).reset_index()
        self.sales_per_store = self.sales_df.groupby(by=['store_id']).agg({'sales_per_day': 'sum'}).reset_index()

        self.sales_bias = get_sales_bias()
        self.price_bias = get_price_bias()
        self.store_sales_bias = get_store_sales_bias()

        self.sales_per_product['sales_per_day'] **= self.sales_bias

        self.sales_df = self.sales_df.merge(self.sales_per_store, on='store_id', suffixes=('', '_store_score'))
        self.sales_df['price_and_store_combined_score'] = (
            self.price_bias * self.sales_df['product_price'] +
            self.store_sales_bias * self.sales_df['sales_per_day_store_score']
        )

    def choose_new_user_recommended_products(self, amount: int) -> pd.DataFrame:
        """
        Selects a specified number of recommended products based on sales data.

        Parameters:
        - amount (int): The number of recommended products to select.

        Returns:
        - pd.DataFrame: A DataFrame containing the recommended products, filtered by the selected product IDs.
        """
        chosen_product_ids = self.sales_per_product.sample(n=amount, weights='sales_per_day')['product_id']
        return self.sales_df[self.sales_df['product_id'].isin(chosen_product_ids)]

    def choose_new_user_product_announcement(self, product: pd.DataFrame) -> dict:
        """
        Chooses a product announcement from the given product DataFrame.

        Parameters:
        - product (pd.DataFrame): A DataFrame containing product details with weights for sampling.

        Returns:
        - Recommendation: A Recommendation dataclass instance with the details of the chosen product announcement.
        """
        chosen_announcement = product.sample(weights='combined_score').iloc[0]
        return Recommendation(
            product_id=chosen_announcement['product_id'],
            product_title=chosen_announcement['product_title'],
            product_price=chosen_announcement['product_price'],
            product_image_url=chosen_announcement['product_image_url'],
            store_id=chosen_announcement['store_id'],
            store_name=chosen_announcement['store_name']
        )
    
    def get_new_user_recommendations(self, amount: int):
        """
        Retrieves new user recommendations by selecting recommended products and choosing product announcements.

        Parameters:
        - amount (int): The number of recommended products to retrieve.

        Returns:
        - List[Recommendation]: A list of Recommendation dataclass instances, one for each unique product ID.
        """
        recommended_products = self.choose_new_user_recommended_products(amount=amount)
        return [self.choose_new_user_product_announcement(product_df) for _, product_df in recommended_products.groupby(by=['product_id'])]