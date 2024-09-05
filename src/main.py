from fastapi import FastAPI

from src.api.recommendation_router import recommendations_router

app = FastAPI()

app.include_router(recommendations_router, prefix="/recommendations")