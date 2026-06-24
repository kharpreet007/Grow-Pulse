import pytest
import numpy as np
from mcp_servers.playstore_reviews.scraper import Review
from groww_pulse.config import ClusteringConfig
from groww_pulse.clustering import rank_and_build_clusters

def test_rank_and_build_clusters():
    reviews = [
        Review(review_id="1", author="A", rating=1, text="r1", timestamp="t", thumbs_up=0, app_version="1"),
        Review(review_id="2", author="B", rating=1, text="r2", timestamp="t", thumbs_up=0, app_version="1"),
        Review(review_id="3", author="C", rating=5, text="r3", timestamp="t", thumbs_up=0, app_version="1"),
        Review(review_id="4", author="D", rating=5, text="r4", timestamp="t", thumbs_up=0, app_version="1"),
    ]
    labels = np.array([0, 0, 1, 1])
    embeddings = np.array([
        [1.0, 0.0],
        [1.1, 0.1],
        [-1.0, 0.0],
        [-1.1, -0.1]
    ])
    
    clusters = rank_and_build_clusters(reviews, labels, embeddings, top_n=2)
    
    assert len(clusters) == 2
    # global_mean = 3.0
    # cluster 0: size 2, avg_rating 1.0 (delta -2.0)
    # cluster 1: size 2, avg_rating 5.0 (delta +2.0)
    # cluster 0 should be first due to more negative delta
    assert clusters[0].cluster_id == 0
    assert clusters[0].avg_rating == 1.0
    assert clusters[1].cluster_id == 1
    assert clusters[1].avg_rating == 5.0
