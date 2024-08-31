from fastapi import FastAPI

from src.api.recommendations import recommendations_router

app = FastAPI()

app.include_router(recommendations_router, prefix="/recommendations")