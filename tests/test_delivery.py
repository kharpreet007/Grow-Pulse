import pytest
from unittest.mock import patch, MagicMock
from groww_pulse.delivery import append_to_google_doc, deliver_email
from groww_pulse.renderer import EmailPayload
from groww_pulse.config import Config

@pytest.fixture
def mock_config():
    return Config(product=None, ingestion=None, clustering=None, llm=None)

@patch('groww_pulse.delivery.requests.post')
def test_append_to_google_doc(mock_post, mock_config):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "success", "doc_id": "123"}
    mock_post.return_value = mock_response
    
    result = append_to_google_doc("Test content", mock_config)
    assert result["doc_id"] == "123"
    mock_post.assert_called_once()
    assert "append_doc" in mock_post.call_args[0][0]
    assert mock_post.call_args[1]['json'] == {"content": "Test content"}

@patch('groww_pulse.delivery.requests.post')
def test_deliver_email_draft_only(mock_post, mock_config):
    mock_response = MagicMock()
    mock_response.json.return_value = {"draft_id": "draft_456"}
    mock_post.return_value = mock_response
    
    payload = EmailPayload("Subject", "HTML", "TEXT", "LINK")
    result = deliver_email(payload, True, mock_config)
    
    assert result["draft_id"] == "draft_456"
    assert mock_post.call_count == 1
    assert "create_email_draft" in mock_post.call_args[0][0]
    
@patch('groww_pulse.delivery.requests.post')
def test_deliver_email_send(mock_post, mock_config):
    mock_create_resp = MagicMock()
    mock_create_resp.json.return_value = {"draft_id": "draft_456"}
    
    mock_send_resp = MagicMock()
    mock_send_resp.json.return_value = {"message_id": "msg_789"}
    
    mock_post.side_effect = [mock_create_resp, mock_send_resp]
    
    payload = EmailPayload("Subject", "HTML", "TEXT", "LINK")
    result = deliver_email(payload, False, mock_config)
    
    assert result["draft_id"] == "draft_456"
    assert result["message_id"] == "msg_789"
    assert mock_post.call_count == 2
