import numpy as np
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer
import umap.umap_ as umap
import hdbscan
import re

from mcp_servers.playstore_reviews.scraper import Review
from .config import ClusteringConfig

@dataclass
class Cluster:
    cluster_id: int
    size: int
    avg_rating: float
    representative_reviews: List[Review]

def normalize_text(text: str) -> str:
    """Basic text normalization: lowercase and remove excess whitespace."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

def generate_embeddings(reviews: List[Review], config: ClusteringConfig) -> np.ndarray:
    """Generates embeddings for a list of reviews."""
    if not reviews:
        return np.array([])
    texts = [normalize_text(r.text) for r in reviews]
    model = SentenceTransformer(config.embedding_model)
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings

def perform_clustering(embeddings: np.ndarray, config: ClusteringConfig) -> np.ndarray:
    """Applies UMAP and HDBSCAN to generate cluster labels."""
    if len(embeddings) < config.umap_n_neighbors:
        n_neighbors = max(2, len(embeddings) - 1)
    else:
        n_neighbors = config.umap_n_neighbors
        
    reducer = umap.UMAP(
        n_neighbors=n_neighbors, 
        n_components=config.umap_n_components, 
        metric='cosine',
        random_state=42
    )
    reduced_embeddings = reducer.fit_transform(embeddings)
    
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=config.hdbscan_min_cluster_size,
        min_samples=config.hdbscan_min_samples,
        metric='euclidean',
        cluster_selection_method='eom'
    )
    labels = clusterer.fit_predict(reduced_embeddings)
    return labels

def rank_and_build_clusters(reviews: List[Review], labels: np.ndarray, embeddings: np.ndarray, top_n: int = 5) -> List[Cluster]:
    """Builds Cluster objects and ranks them by size and rating delta."""
    if not reviews:
        return []
        
    global_mean = float(np.mean([r.rating for r in reviews]))
    
    clusters_dict = {}
    for idx, (label, review) in enumerate(zip(labels, reviews)):
        if label == -1: # Noise
            continue
        if label not in clusters_dict:
            clusters_dict[label] = {
                "reviews": [],
                "embeddings": [],
                "ratings": []
            }
        clusters_dict[label]["reviews"].append(review)
        clusters_dict[label]["embeddings"].append(embeddings[idx])
        clusters_dict[label]["ratings"].append(review.rating)
        
    cluster_objects = []
    for label, data in clusters_dict.items():
        size = len(data["reviews"])
        avg_rating = float(np.mean(data["ratings"]))
        
        # Calculate representatives (closest to centroid)
        centroid = np.mean(data["embeddings"], axis=0)
        distances = np.linalg.norm(data["embeddings"] - centroid, axis=1)
        
        # Top 5 closest to centroid
        top_indices = np.argsort(distances)[:5]
        representatives = [data["reviews"][i] for i in top_indices]
        
        cluster_objects.append(Cluster(
            cluster_id=int(label),
            size=size,
            avg_rating=avg_rating,
            representative_reviews=representatives
        ))
        
    # Rank by size (descending), then by rating delta (ascending/more negative)
    # Sorting key: (-size, rating_delta)
    cluster_objects.sort(key=lambda c: (-c.size, c.avg_rating - global_mean))
    
    return cluster_objects[:top_n]
