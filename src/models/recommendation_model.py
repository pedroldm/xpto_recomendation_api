from dataclasses import dataclass

@dataclass
class Recommendation:
    product_id: int
    product_title: str
    product_price: float
    product_image_url: str
    store_id: int
    store_name: str

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the Recommendation.
        """
        return (f"Recommendation for Product ID {self.product_id}: "
                f"{self.product_title} at ${self.product_price:.2f} "
                f"available at store '{self.store_name}' (Store ID: {self.store_id}).")

    def __repr__(self) -> str:
        """
        Return a string representation of the Recommendation that can be used to recreate the object.
        """
        return (f"Recommendation(product_id={self.product_id!r}, "
                f"product_title={self.product_title!r}, "
                f"product_price={self.product_price!r}, "
                f"product_image_url={self.product_image_url!r}, "
                f"store_id={self.store_id!r}, "
                f"store_name={self.store_name!r})")