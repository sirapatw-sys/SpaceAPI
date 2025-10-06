import pytest
import json
from pathlib import Path
from src import fetchers

DATA_DIR = Path(__file__).parent.parent / "data"
INDEX_FILE = DATA_DIR / "index.json"

@pytest.fixture
def clear_index():
    """ลบไฟล์ index.json ก่อนและหลังเทสต์"""
    if INDEX_FILE.exists():
        INDEX_FILE.unlink()
    yield
    if INDEX_FILE.exists():
        INDEX_FILE.unlink()

def test_fetch_apod(clear_index):
    """ทดสอบการดึง APOD"""
    fetchers.fetch_apod()  # ใช้ default date
    assert INDEX_FILE.exists(), "ไฟล์ index.json ต้องถูกสร้าง"
    
    data = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    assert len(data) >= 1, "ต้องมีรายการอย่างน้อย 1 รายการ"
    
    item = data[0]
    assert "title" in item
    assert "date" in item
    assert "local_path" in item
    assert "source" in item
    assert item["source"] == "APOD"

def test_fetch_mars(clear_index):
    """ทดสอบการดึงภาพ Mars rover"""
    fetchers.fetch_mars()
    assert INDEX_FILE.exists(), "ไฟล์ index.json ต้องถูกสร้าง"
    
    data = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    assert len(data) >= 1, "ต้องมีรายการอย่างน้อย 1 รายการ"
    
    for item in data:
        assert "title" in item
        assert "date" in item
        assert "local_path" in item
        assert "source" in item
        assert item["source"] == "Mars Rover"
