from dataclasses import dataclass
from typing import List, Optional
from google_play_scraper import reviews, Sort
import emoji
import langdetect
import re

HINGLISH_STOPWORDS = {
    "hai", "nahi", "bakwas", "ghatiya", "karo", "ka", "ki", "ke", "liye", 
    "bhi", "sirf", "hota", "karna", "wala", "mein", "aur", "toh", "tha", 
    "thi", "the", "kar", "mat", "kya", "kyu", "kese", "kaise", "kab", "kaha"
}

def is_hinglish(text: str) -> bool:
    words = set(re.findall(r'\b\w+\b', text.lower()))
    hinglish_count = len(words.intersection(HINGLISH_STOPWORDS))
    return hinglish_count >= 2

@dataclass
class Review:
    review_id: str
    author: str
    rating: int
    text: str
    timestamp: str
    thumbs_up: int
    app_version: Optional[str]

def is_valid_review(text: str) -> bool:
    if not text:
        return False
        
    # 1. Word count >= 8
    words = text.split()
    if len(words) < 8:
        return False
        
    # 2. No emojis
    if emoji.emoji_count(text) > 0:
        return False
        
    # 3. Only English language
    try:
        lang = langdetect.detect(text)
        if lang != 'en':
            return False
    except langdetect.LangDetectException:
        # If language cannot be detected reliably
        return False
        
    # 4. Filter Hinglish
    if is_hinglish(text):
        return False
        
    return True

def fetch_valid_reviews(app_id: str, lang: str = 'en', count: int = 1000, sort: str = 'newest') -> List[Review]:
    sort_order = Sort.NEWEST if sort.lower() == 'newest' else Sort.MOST_RELEVANT
    
    valid_reviews = []
    continuation_token = None
    
    while len(valid_reviews) < count:
        batch_size = min(200, count - len(valid_reviews) + 100)
        
        try:
            result, continuation_token = reviews(
                app_id,
                lang=lang,
                country='us',
                sort=sort_order,
                count=batch_size,
                continuation_token=continuation_token
            )
        except Exception as e:
            print(f"Error fetching reviews: {e}")
            break
            
        if not result:
            break
            
        for r in result:
            text = r.get('content', '')
            if is_valid_review(text):
                valid_reviews.append(Review(
                    review_id=r.get('reviewId'),
                    author=r.get('userName'),
                    rating=r.get('score'),
                    text=text,
                    timestamp=r.get('at').isoformat() if r.get('at') else "",
                    thumbs_up=r.get('thumbsUpCount', 0),
                    app_version=r.get('reviewCreatedVersion')
                ))
                
            if len(valid_reviews) >= count:
                break
                
        if not continuation_token:
            break
            
    return valid_reviews
