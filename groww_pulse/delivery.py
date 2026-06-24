import logging
import requests
import time
from functools import wraps
from typing import Dict, Any, Optional
from groww_pulse.config import Config
from groww_pulse.renderer import EmailPayload

logger = logging.getLogger(__name__)

def with_retries(max_retries=3, initial_backoff=1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            backoff = initial_backoff
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(f"Error in {func.__name__}: {e}. Retrying in {backoff}s...")
                    time.sleep(backoff)
                    backoff *= 2
        return wrapper
    return decorator

BASE_URL = "https://kharpreet-mcp-server-production-8e75.up.railway.app"

@with_retries(max_retries=3)
def append_to_google_doc(content: str, config: Config) -> Dict[str, Any]:
    """
    Appends the given markdown/text content to the Google Doc via the Railway Delivery API.
    Returns the response JSON containing e.g. doc_id, heading_id, revision_id.
    """
    url = f"{BASE_URL}/append_to_doc"
    logger.info(f"Appending content to Google Doc via {url}...")
    
    # We will need the doc_id from the config or environment
    doc_id = getattr(config.delivery, 'google_doc_id', "YOUR_DOC_ID")
    
    payload = {
        "doc_id": doc_id,
        "content": content
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        # Try to parse json, otherwise return empty dict
        try:
            result = response.json()
        except ValueError:
            result = {"status": "success", "raw_response": response.text}
            
        logger.info(f"Successfully appended to Google Doc: {result}")
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to append to Google Doc: {e}")
        raise

@with_retries(max_retries=3)
def deliver_email(payload: EmailPayload, draft_only: bool, config: Config) -> Dict[str, Any]:
    """
    Creates an email draft via the Railway Delivery API, and optionally sends it.
    Returns the response JSON containing e.g. draft_id and optionally message_id.
    """
    create_url = f"{BASE_URL}/create_email_draft"
    logger.info(f"Creating email draft via {create_url}...")
    
    # Combine HTML and fallback text in some way if only 'body' is supported.
    # The API just wants a single 'body'.
    combined_body = payload.html_body
    
    # Needs a 'to' address from config. email_recipients is a list of strings
    recipients = getattr(config.delivery, 'email_recipients', ["test@example.com"])
    to_address = ", ".join(recipients) if isinstance(recipients, list) else recipients
    
    email_data = {
        "to": to_address,
        "subject": payload.subject,
        "body": combined_body
    }
    
    try:
        # Step 1: Create draft
        response = requests.post(create_url, json=email_data, timeout=30)
        response.raise_for_status()
        
        try:
            create_result = response.json()
        except ValueError:
            create_result = {"status": "success", "raw_response": response.text}
            
        draft_id = create_result.get("draft_id")
        logger.info(f"Successfully created email draft. Draft ID: {draft_id}")
        
        # Step 2: Send draft (if not draft_only)
        if draft_only:
            logger.info("draft_only flag is set. Stopping before send.")
            return create_result
            
        if not draft_id:
            logger.warning("No draft_id returned from create_email_draft. Attempting to send without draft_id or skipping...")
            draft_id = ""
            
        send_url = f"{BASE_URL}/send_draft"
        logger.info(f"Sending email draft {draft_id} via {send_url}...")
        
        send_payload = {
            "draft_id": draft_id
        }
        
        send_response = requests.post(send_url, json=send_payload, timeout=30)
        if send_response.status_code == 404:
            logger.warning(f"Endpoint {send_url} returned 404. It appears the server does not support sending drafts. Returning draft creation result.")
            return create_result
            
        send_response.raise_for_status()
        
        try:
            send_result = send_response.json()
        except ValueError:
            send_result = {"status": "success", "raw_response": send_response.text}
            
        logger.info(f"Successfully sent email draft. Message ID: {send_result.get('message_id')}")
        
        # Merge results to return both draft_id and message_id
        create_result.update(send_result)
        return create_result
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Email delivery failed: {e}")
        raise
