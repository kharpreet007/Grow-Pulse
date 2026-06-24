import yaml
from dataclasses import dataclass
from typing import List
import os

@dataclass
class ProductConfig:
    name: str
    play_store_app_id: str

@dataclass
class IngestionConfig:
    window_weeks: int
    max_reviews: int

@dataclass
class ClusteringConfig:
    embedding_model: str
    umap_n_components: int
    umap_n_neighbors: int
    hdbscan_min_cluster_size: int
    hdbscan_min_samples: int

@dataclass
class LLMConfig:
    model: str
    provider: str
    temperature: float
    max_tokens_per_minute: int
    max_tokens_per_day: int
    max_requests_per_minute: int
    max_requests_per_day: int
    quote_validation: bool

@dataclass
class DeliveryConfig:
    google_doc_id: str
    email_recipients: List[str]
    draft_only: bool

@dataclass
class ReceiptsConfig:
    storage_path: str

@dataclass
class Config:
    product: ProductConfig
    ingestion: IngestionConfig
    clustering: ClusteringConfig
    llm: LLMConfig
    delivery: DeliveryConfig
    receipts: ReceiptsConfig

def load_config(path: str = "config.yaml") -> Config:
    if not os.path.isabs(path):
        # Resolve path relative to the current working directory, or default to repo root
        path = os.path.abspath(path)

    with open(path, "r") as f:
        data = yaml.safe_load(f)
    
    return Config(
        product=ProductConfig(**data.get("product", {})),
        ingestion=IngestionConfig(**data.get("ingestion", {})),
        clustering=ClusteringConfig(**data.get("clustering", {})),
        llm=LLMConfig(**data.get("llm", {})),
        delivery=DeliveryConfig(**data.get("delivery", {})),
        receipts=ReceiptsConfig(**data.get("receipts", {}))
    )
