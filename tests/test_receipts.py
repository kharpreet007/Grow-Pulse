import os
import json
import pytest
from datetime import datetime
from groww_pulse.receipts import RunReceipt, DeliveryStatus, ReceiptManager

def test_receipt_serialization(tmp_path):
    manager = ReceiptManager(str(tmp_path))
    
    receipt = RunReceipt(
        iso_week="2026-W24",
        timestamp=datetime.now().isoformat(),
        status="success",
        review_window=10,
        reviews_ingested=1200,
        clusters_found=5,
        themes_generated=5,
        delivery=DeliveryStatus(
            docs_status="appended",
            docs_id="doc123",
            gmail_status="drafted",
            gmail_draft_id="draft123"
        )
    )
    
    manager.save_receipt(receipt)
    
    # Verify file exists
    assert os.path.exists(os.path.join(tmp_path, "groww_2026-W24.json"))
    
    # Load and verify
    loaded = manager.load_receipt("2026-W24")
    assert loaded is not None
    assert loaded.iso_week == "2026-W24"
    assert loaded.reviews_ingested == 1200
    assert loaded.delivery.docs_status == "appended"
    assert loaded.delivery.docs_id == "doc123"
    assert loaded.delivery.gmail_draft_id == "draft123"

def test_load_nonexistent_receipt(tmp_path):
    manager = ReceiptManager(str(tmp_path))
    loaded = manager.load_receipt("2026-W99")
    assert loaded is None

def test_get_all_receipts(tmp_path):
    manager = ReceiptManager(str(tmp_path))
    
    r1 = RunReceipt(iso_week="2026-W01", timestamp="x", status="failed")
    r2 = RunReceipt(iso_week="2026-W02", timestamp="y", status="success")
    
    manager.save_receipt(r1)
    manager.save_receipt(r2)
    
    all_receipts = manager.get_all_receipts()
    assert len(all_receipts) == 2
    assert "2026-W01" in all_receipts
    assert "2026-W02" in all_receipts
