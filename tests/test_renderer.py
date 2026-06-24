import pytest
from groww_pulse.renderer import render_google_doc_content, render_email_payload, EmailPayload
from groww_pulse.summarizer import ThemeSummary, ActionIdea
from groww_pulse.config import Config, ProductConfig

@pytest.fixture
def sample_summaries():
    return [
        ThemeSummary(
            cluster_id=1, size=10, avg_rating=4.5,
            theme_name="Great App", description="Users love it.",
            quotes=["Quote 1"], action_ideas=[ActionIdea(idea="Do more", team="Product")]
        )
    ]

@pytest.fixture
def sample_config():
    return Config(product=ProductConfig(name="Groww", play_store_app_id=""), ingestion=None, clustering=None, llm=None)

def test_render_google_doc_content(sample_summaries, sample_config):
    doc = render_google_doc_content(sample_summaries, "2026-W24", sample_config)
    assert "Groww — Weekly Review Pulse (2026-W24)" in doc
    assert "Period: 2026-W24" in doc
    assert "1. Great App (10 reviews)" in doc
    assert "Users love it." in doc
    assert "- \"Quote 1\"" in doc
    assert "1. [Product] Do more" in doc
    assert "#" not in doc # No markdown hashes

def test_render_email_payload(sample_summaries, sample_config):
    email = render_email_payload(sample_summaries, "2026-W24", sample_config, "https://doc.link")
    assert email.subject == "Groww Review Pulse — 2026-W24"
    assert "<h2>Groww Review Pulse" in email.html_body
    assert "<li><strong>Great App</strong> (10 reviews)" in email.html_body
    assert "<a href=\"https://doc.link\">Read full report &rarr;</a>" in email.html_body
    assert "Groww Review Pulse — 2026-W24" in email.text_body
    assert "- Great App (10 reviews): Users love it." in email.text_body
    assert "Read full report: https://doc.link" in email.text_body
