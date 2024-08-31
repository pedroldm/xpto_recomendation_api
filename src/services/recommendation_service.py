import pandas as pd


class RecommendationsService:
    _instance = None

    def __new__(cls, file_path: str, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RecommendationsService, cls).__new__(cls, *args, **kwargs)
            cls._instance.file_path = file_path  # Store the file path
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.sales_df = pd.read_csv(self.file_path)
