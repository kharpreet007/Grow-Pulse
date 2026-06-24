import pytest
import time
from unittest.mock import patch, MagicMock
from groww_pulse.config import LLMConfig
from groww_pulse.summarizer import Summarizer, ThemeSummary, ActionIdea
from groww_pulse.clustering import Cluster
from mcp_servers.playstore_reviews.scraper import Review

@pytest.fixture
def mock_config():
    return LLMConfig(
        model="llama-3.3-70b-versatile",
        provider="groq",
        temperature=0.2,
        max_tokens_per_minute=12000,
        max_tokens_per_day=100000,
        max_requests_per_minute=30,
        max_requests_per_day=1000,
        quote_validation=True
    )

@pytest.fixture
def mock_cluster():
    return Cluster(
        cluster_id=1,
        size=10,
        avg_rating=2.5,
        representative_reviews=[
            Review(review_id="1", author="A", rating=2, text="This is a test review about bugs.", timestamp="t", thumbs_up=0, app_version="1"),
            Review(review_id="2", author="B", rating=3, text="Another review with exact quote right here.", timestamp="t", thumbs_up=0, app_version="1")
        ]
    )

@patch("openai.OpenAI")
def test_summarizer_success(mock_openai, mock_config, mock_cluster):
    # Mock LLM Response
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.usage.total_tokens = 150
    mock_theme = ThemeSummary(
        cluster_id=1,
        size=10,
        avg_rating=2.5,
        theme_name="Bug Theme",
        description="Lots of bugs",
        quotes=["This is a test review about bugs.", "exact quote right here."],
        action_ideas=[ActionIdea(idea="Fix bugs", team="Eng")]
    )
    mock_response.choices[0].message.parsed = mock_theme
    mock_client.beta.chat.completions.parse.return_value = mock_response
    
    summarizer = Summarizer(mock_config)
    result = summarizer.summarize_cluster(mock_cluster)
    
    assert result is not None
    assert result.theme_name == "Bug Theme"
    assert len(result.quotes) == 2
    assert summarizer.total_tokens_today == 150
    assert summarizer.total_requests_today == 1

@patch("openai.OpenAI")
def test_summarizer_quote_validation_failure(mock_openai, mock_config, mock_cluster):
    # Mock LLM returning hallucinated quote
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    
    mock_response_1 = MagicMock()
    mock_response_1.usage.total_tokens = 100
    mock_theme_1 = ThemeSummary(
        cluster_id=1,
        size=10,
        avg_rating=2.5,
        theme_name="Bug Theme",
        description="Lots of bugs",
        quotes=["This quote is hallucinated and not in the text."],
        action_ideas=[]
    )
    mock_response_1.choices[0].message.parsed = mock_theme_1
    
    # Second attempt returns valid quote
    mock_response_2 = MagicMock()
    mock_response_2.usage.total_tokens = 100
    mock_theme_2 = ThemeSummary(
        cluster_id=1,
        size=10,
        avg_rating=2.5,
        theme_name="Bug Theme",
        description="Lots of bugs",
        quotes=["exact quote right here."],
        action_ideas=[]
    )
    mock_response_2.choices[0].message.parsed = mock_theme_2
    
    mock_client.beta.chat.completions.parse.side_effect = [mock_response_1, mock_response_2]
    
    summarizer = Summarizer(mock_config)
    result = summarizer.summarize_cluster(mock_cluster)
    
    assert result is not None
    assert len(result.quotes) == 1
    assert result.quotes[0] == "exact quote right here."
    assert summarizer.total_tokens_today == 200 # 100 + 100
    assert summarizer.total_requests_today == 2
    
@patch("openai.OpenAI")
def test_daily_token_budget_exceeded(mock_openai, mock_config, mock_cluster):
    mock_config.max_tokens_per_day = 50
    summarizer = Summarizer(mock_config)
    summarizer.total_tokens_today = 100 # Already exceeded
    
    result = summarizer.summarize_cluster(mock_cluster)
    assert result is None

@patch("openai.OpenAI")
@patch("time.sleep")
def test_minute_rate_limit(mock_sleep, mock_openai, mock_config, mock_cluster):
    mock_config.max_requests_per_minute = 1
    
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_response = MagicMock()
    mock_response.usage.total_tokens = 100
    mock_theme = ThemeSummary(
        cluster_id=1, size=10, avg_rating=2.5, theme_name="Test",
        description="Test", quotes=[], action_ideas=[]
    )
    mock_response.choices[0].message.parsed = mock_theme
    mock_client.beta.chat.completions.parse.return_value = mock_response
    
    summarizer = Summarizer(mock_config)
    summarizer.minute_window_start = time.time()
    
    # First call works fine, consumes the 1 request limit
    res1 = summarizer.summarize_cluster(mock_cluster)
    assert res1 is not None
    
    # Second call should sleep
    res2 = summarizer.summarize_cluster(mock_cluster)
    assert res2 is not None
    mock_sleep.assert_called_once()
