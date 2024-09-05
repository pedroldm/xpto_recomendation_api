import numpy as np
import pytest
from scipy import stats

from src.models.recommendation_model import Recommendation


@pytest.mark.asyncio
async def test_get_new_user_recommendations(recommendation_service):
    recommendations = await recommendation_service.get_new_user_recommendations(amount=10)
    assert len(recommendations) == 10
    assert all(isinstance(rec, Recommendation) for rec in recommendations)

@pytest.mark.asyncio
async def test_all_products_belong_to_db(recommendation_service, confidence_level=0.95):
    recommendations = [r for r in await recommendation_service.get_new_user_recommendations(amount=10) for i in range(100)]
    
    sample_size = len(recommendations)
    sample = np.random.choice(recommendations, sample_size, replace=False) if sample_size > 0 else recommendations
    
    correct_count = 0
    for p in sample:
        if p.product_id in recommendation_service.sales_df['product_id'].values: # type: ignore
            correct_count += 1
    
    proportion_correct = correct_count / sample_size
    
    assert proportion_correct >= confidence_level
    
@pytest.mark.asyncio
async def test_all_products_info_are_correct(recommendation_service, confidence_level=0.95):
    recommendations = [r for r in await recommendation_service.get_new_user_recommendations(amount=10) for i in range(100)]
    sample_size = len(recommendations)
    sample = np.random.choice(recommendations, sample_size, replace=False) if sample_size > 0 else recommendations
    
    correct_count = 0
    for r in sample:
        correspondent_row = recommendation_service.sales_df[
            (recommendation_service.sales_df['product_id'] == getattr(r, 'product_id')) & # type: ignore
            (recommendation_service.sales_df['store_id'] == getattr(r, 'store_id')) & # type: ignore
            (recommendation_service.sales_df['product_price'] == getattr(r, 'product_price')) # type: ignore
        ]
        if not correspondent_row.empty:
            correct_count += 1
    
    proportion_correct = correct_count / sample_size
    
    assert proportion_correct >= confidence_level