import json
import os
import asyncio
from typing import List, Dict, Any
from datetime import datetime, timedelta

from mcp_servers.playstore_reviews.scraper import fetch_valid_reviews, Review as ScraperReview
from .config import Config
from .pii import scrub_pii
import dataclasses

async def fetch_raw_reviews(config: Config) -> List[Dict[str, Any]]:
    """
    Fetches raw reviews directly from the scraper (bypassing MCP for python 3.9 compatibility).
    Includes 3 retries with exponential backoff.
    """
    import time
    
    max_retries = 3
    backoff = 1.0
    
    for attempt in range(max_retries):
        try:
            reviews = fetch_valid_reviews(
                app_id=config.product.play_store_app_id,
                count=config.ingestion.max_reviews
            )
            return [dataclasses.asdict(r) for r in reviews]
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed to fetch reviews after {max_retries} attempts.")
                raise
            print(f"Error fetching reviews: {e}. Retrying in {backoff}s...")
            time.sleep(backoff)
            backoff *= 2

def ingest_reviews(config: Config, run_date: datetime = None) -> List[ScraperReview]:
    """
    Ingests reviews via MCP, filters by date, scrubs PII, and deduplicates.
    """
    if run_date is None:
        run_date = datetime.now()
        
    raw_reviews_data = asyncio.run(fetch_raw_reviews(config))
    
    if not raw_reviews_data:
        print("No reviews fetched.")
        return []
        
    window_start = run_date - timedelta(weeks=config.ingestion.window_weeks)
    
    clean_reviews = []
    seen_ids = set()
    total_redactions = 0
    
    for r_data in raw_reviews_data:
        review_id = r_data.get("review_id")
        
        # 1. Deduplication
        if review_id in seen_ids:
            continue
        seen_ids.add(review_id)
        
        timestamp_str = r_data.get("timestamp")
        if not timestamp_str:
            continue
            
        try:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except ValueError:
            continue
            
        # 2. Date filtering
        dt_naive = dt.replace(tzinfo=None)
        if dt_naive < window_start:
            continue
            
        # 3. PII Scrubbing
        scrubbed_text, count_text = scrub_pii(r_data.get("text", ""))
        scrubbed_author, count_author = scrub_pii(r_data.get("author", ""))
        
        total_redactions += (count_text + count_author)
        
        clean_reviews.append(ScraperReview(
            review_id=review_id,
            author=scrubbed_author,
            rating=r_data.get("rating"),
            text=scrubbed_text,
            timestamp=timestamp_str,
            thumbs_up=r_data.get("thumbs_up", 0),
            app_version=r_data.get("app_version")
        ))
        
    print(f"Filtered {len(raw_reviews_data)} reviews to {len(clean_reviews)} within {config.ingestion.window_weeks}-week window")
    print(f"Total PII redactions: {total_redactions}")
    
    return clean_reviews
