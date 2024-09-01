import pandas as pd
import numpy as np
from src.config import get_database_path, get_sales_bias, get_price_bias, get_store_sales_bias

class RecommendationsService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RecommendationsService, cls).__new__(cls, *args, **kwargs)
            cls._instance.initialize()
        return cls._instance

    def initialize(self) -> None:
        self.sales_df = pd.read_csv(get_database_path())
        self.sales_per_product = self.sales_df.groupby(by=['product_id'])['sales_per_day'].sum()
        self.sales_per_store = self.sales_df.groupby(by=['store_id'])['sales_per_day'].sum()

        self.sales_bias = get_sales_bias()
        self.price_bias = get_price_bias()
        self.store_sales_bias = get_store_sales_bias()

        self.sales_weights = self.sales_per_product ** self.sales_bias
        self.sales_weights /= self.sales_weights.sum()

        self.sales_df = self.sales_df.merge(self.sales_per_store, on='store_id', suffixes=('', '_store_score'))
        self.sales_df['combined_score'] = (
            self.price_bias * self.sales_df['product_price'] +
            self.store_sales_bias * self.sales_df['sales_per_day_store_score']
        )

    def choose_new_user_recommended_products(self, amount: int) -> pd.DataFrame:
        chosen_product_ids = np.random.choice(
            self.sales_per_product.index,
            size=amount,
            replace=False,
            p=self.sales_weights
        )

        return self.sales_df[self.sales_df['product_id'].isin(chosen_product_ids)]

    def choose_new_user_product_announcement(self, product: pd.DataFrame):
        chosen_announcement = product.sample(weights='combined_score').iloc[0]
        return {
            'product_id': chosen_announcement['product_id'],
            'product_title': chosen_announcement['product_title'],
            'product_price': chosen_announcement['product_price'],
            'product_image_url': chosen_announcement['product_image_url'],
            'store_name': chosen_announcement['store_name'],
            'store_id': chosen_announcement['store_id']
        }
    
    def get_new_user_recommendations(self, amount: int):
        recommended_products = self.choose_recommended_products(amount=amount)
        return [self.choose_product_announcement(product_df) for _, product_df in recommended_products.groupby(by=['product_id'])]