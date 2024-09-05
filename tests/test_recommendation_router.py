import json

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.mark.asyncio
async def test_get_user_recommendations():
    client = TestClient(app)
    response = client.get('/recommendations/12345')
    recommendations = json.loads(response.text)
    
    assert response.status_code == 200
    assert len(recommendations) == 5
    assert all([k in r for k in ['product_id', 'product_title', 'product_price', 'product_image_url', 'store_id', 'store_name'] for r in recommendations])