import json
import dataclasses
from datetime import datetime, timedelta
from mcp_servers.playstore_reviews.scraper import fetch_valid_reviews
from groww_pulse.pii import scrub_pii
import os

print("Fetching reviews directly (bypassing MCP for environment testing)...")
# Fetch a large number of reviews and filter for 10 weeks
reviews = fetch_valid_reviews("com.nextbillion.groww", count=5000)

now = datetime.now()
ten_weeks_ago = now - timedelta(weeks=10)

actual_reviews = []
normalized_reviews = []

for r in reviews:
    try:
        dt = datetime.fromisoformat(r.timestamp.replace('Z', '+00:00')).replace(tzinfo=None)
    except Exception:
        continue
        
    if dt < ten_weeks_ago:
        continue

    r_dict = dataclasses.asdict(r)
    
    # Remove requested fields
    for field in ["review_id", "author", "timestamp"]:
        r_dict.pop(field, None)
    actual_reviews.append(r_dict)
    
    n_dict = r_dict.copy()
    text, _ = scrub_pii(n_dict["text"])
    n_dict["text"] = text
    normalized_reviews.append(n_dict)

with open("data/actual_reviews.json", "w") as f:
    json.dump(actual_reviews, f, indent=2)

with open("data/normalized_reviews.json", "w") as f:
    json.dump(normalized_reviews, f, indent=2)

print(f"Successfully saved {len(actual_reviews)} reviews from the last 10 weeks into data/actual_reviews.json and data/normalized_reviews.json")
