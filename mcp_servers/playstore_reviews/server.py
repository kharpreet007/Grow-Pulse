from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP
from .scraper import fetch_valid_reviews
import dataclasses

# Initialize FastMCP server
mcp = FastMCP("playstore-reviews")

@mcp.tool()
def fetch_reviews(app_id: str = "com.nextbillion.groww", lang: str = "en", count: int = 1000, sort: str = "newest") -> List[Dict[str, Any]]:
    """
    Fetch valid Play Store reviews for a given app.
    Returns structured review data matching the Review schema.
    """
    results = fetch_valid_reviews(app_id, lang, count, sort)
    return [dataclasses.asdict(r) for r in results]
