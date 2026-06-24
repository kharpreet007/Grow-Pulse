import os
import json
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class DeliveryStatus:
    docs_status: str  # "pending", "appended", "failed"
    gmail_status: str  # "pending", "drafted", "sent", "failed"
    docs_id: Optional[str] = None
    gmail_draft_id: Optional[str] = None
    gmail_message_id: Optional[str] = None

@dataclass
class RunReceipt:
    iso_week: str
    timestamp: str
    status: str  # "success", "partial", "failed"
    error: Optional[str] = None
    review_window: int = 0
    reviews_ingested: int = 0
    clusters_found: int = 0
    themes_generated: int = 0
    delivery: Optional[DeliveryStatus] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
        
class ReceiptManager:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)
        
    def _get_receipt_path(self, iso_week: str) -> str:
        return os.path.join(self.storage_path, f"groww_{iso_week}.json")
        
    def save_receipt(self, receipt: RunReceipt):
        path = self._get_receipt_path(receipt.iso_week)
        with open(path, "w") as f:
            json.dump(receipt.to_dict(), f, indent=2)
            
    def load_receipt(self, iso_week: str) -> Optional[RunReceipt]:
        path = self._get_receipt_path(iso_week)
        if not os.path.exists(path):
            return None
            
        with open(path, "r") as f:
            data = json.load(f)
            
        delivery_data = data.get("delivery")
        if delivery_data:
            data["delivery"] = DeliveryStatus(**delivery_data)
            
        return RunReceipt(**data)
        
    def get_all_receipts(self) -> Dict[str, RunReceipt]:
        receipts = {}
        if not os.path.exists(self.storage_path):
            return receipts
            
        for filename in os.listdir(self.storage_path):
            if filename.startswith("groww_") and filename.endswith(".json"):
                iso_week = filename[6:-5]
                receipt = self.load_receipt(iso_week)
                if receipt:
                    receipts[iso_week] = receipt
        return receipts
