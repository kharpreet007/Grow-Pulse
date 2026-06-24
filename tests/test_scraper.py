import pytest
from mcp_servers.playstore_reviews.scraper import is_valid_review, fetch_valid_reviews

def test_is_valid_review_word_count():
    assert not is_valid_review("Too short.")
    assert not is_valid_review("One two three four five six seven.")
    assert is_valid_review("One two three four five six seven eight.")

def test_is_valid_review_no_emojis():
    assert not is_valid_review("Good app but has a bug 🐛. Please fix.")
    assert is_valid_review("Good app but has a bug. Please fix.")

def test_is_valid_review_english_only():
    # Spanish
    assert not is_valid_review("Esta aplicación es muy buena pero tiene algunos errores.")
    # Hindi
    assert not is_valid_review("यह ऐप बहुत अच्छा है लेकिन इसमें कुछ बग हैं।")
    # English
    assert is_valid_review("This application is very good but it has some bugs.")

@pytest.mark.integration
def test_fetch_valid_reviews():
    # Fetch a small amount of live reviews to verify
    reviews = fetch_valid_reviews("com.nextbillion.groww", count=5)
    assert len(reviews) == 5
    for r in reviews:
        assert len(r.text.split()) >= 8
        assert r.rating in [1, 2, 3, 4, 5]
