import pytest
from groww_pulse.config import load_config
import os

def test_load_config():
    # Make sure we load the actual config file
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    config = load_config(config_path)
    assert config.product.name == "Groww"
    assert config.product.play_store_app_id == "com.nextbillion.groww"
    assert config.ingestion.window_weeks == 12
    assert config.llm.model == "gpt-4o-mini"
