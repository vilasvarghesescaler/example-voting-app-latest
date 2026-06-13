import pytest
from unittest.mock import MagicMock, patch

# We patch redis BEFORE importing app so it doesn't fail on initialization
with patch('redis.Redis') as mock_redis:
    # Setup a fake redis instance template
    mock_instance = MagicMock()
    mock_redis.return_value = mock_instance
    from app import app

@pytest.fixture
def client():
    """Configures the Flask app for testing."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_voting_page_loads(client):
    """Validates that the main voting page HTML loads successfully (GET)."""
    response = client.get('/')
    assert response.status_code == 200
    # Checks if the default voting choices or elements exist on the page
    assert b"Cats" in response.data or b"Dogs" in response.data or b"Vote" in response.data
