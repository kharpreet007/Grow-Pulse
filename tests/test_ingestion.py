import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from groww_pulse.config import Config, IngestionConfig, ProductConfig
from groww_pulse.ingestion import ingest_reviews

@pytest.fixture
def mock_config():
    config = MagicMock(spec=Config)
    config.product = ProductConfig(name="Groww", play_store_app_id="com.test")
    config.ingestion = IngestionConfig(window_weeks=12, max_reviews=100)
    return config

@patch("groww_pulse.ingestion.fetch_raw_reviews")
def test_ingestion_pipeline(mock_fetch, mock_config):
    now = datetime.now()
    recent = (now - timedelta(weeks=1)).isoformat()
    old = (now - timedelta(weeks=13)).isoformat()
    
    mock_fetch.return_value = [
        {"review_id": "1", "text": "Good app user@example.com", "author": "John", "rating": 5, "timestamp": recent},
        {"review_id": "1", "text": "Duplicate review", "author": "John", "rating": 5, "timestamp": recent}, # Duplicate
        {"review_id": "2", "text": "Old review", "author": "Alice", "rating": 4, "timestamp": old}, # Old
        {"review_id": "3", "text": "Valid clean review", "author": "Bob 1234 5678 9012", "rating": 3, "timestamp": recent}, # PII in author
    ]
    
    reviews = ingest_reviews(mock_config, run_date=now)
    
    assert len(reviews) == 2 # Only ID 1 and 3 should survive
    assert reviews[0].review_id == "1"
    assert "user@example.com" not in reviews[0].text
    assert "[REDACTED]" in reviews[0].text
    
    assert reviews[1].review_id == "3"
    assert "1234 5678 9012" not in reviews[1].author
    assert "[REDACTED]" in reviews[1].author
