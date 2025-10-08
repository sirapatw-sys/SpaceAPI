import os
import requests
import json
from pathlib import Path
from datetime import date

# ใช้ .env หรือ Environment Variables จาก Render
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")

DATA_DIR = Path(__file__).parent.parent / "data"
INDEX_FILE = DATA_DIR / "index.json"

# สร้าง data directory ถ้ายังไม่มี
DATA_DIR.mkdir(exist_ok=True)


def fetch_apod(date: str | None = None):
    """
    Fetch NASA Astronomy Picture of the Day (APOD)
    and save metadata (not image file) into data/index.json
    """
    api_url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": NASA_API_KEY}
    if date:
        params["date"] = date

    print(f"Fetching APOD for date: {date or 'latest'}")
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    data = response.json()

    # เตรียมข้อมูลภาพ
    item = {
        "type": "apod",
        "title": data.get("title", "Unknown"),
        "date": data.get("date", str(date or "")),
        "url": data.get("url"),
        "explanation": data.get("explanation", ""),
        "media_type": data.get("media_type", "image")
    }

    # อ่าน index.json เดิม
    items = []
    if INDEX_FILE.exists():
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                items = json.load(f)
        except json.JSONDecodeError:
            items = []

    # เพิ่มรายการใหม่
    items.append(item)

    # บันทึกใหม่
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

    print(f"✅ Saved APOD for {item['date']} ({item['title']})")


def fetch_mars(date: str | None = None):
    """
    Fetch NASA Mars Rover Photos (Curiosity)
    and save metadata (not image file) into data/index.json
    """
    api_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
    params = {"api_key": NASA_API_KEY}

    # ถ้าไม่มีวันที่ ให้ใช้วันนี้
    params["earth_date"] = date or str(date or "2025-10-08")

    print(f"Fetching Mars photos for {params['earth_date']}")
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    data = response.json()

    photos = data.get("photos", [])
    if not photos:
        print("⚠️ No Mars photos found for that date.")
        return

    # อ่าน index.json เดิม
    items = []
    if INDEX_FILE.exists():
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                items = json.load(f)
        except json.JSONDecodeError:
            items = []

    # เพิ่มภาพทั้งหมด
    for p in photos[:20]:  # จำกัด 20 ภาพเพื่อความเบา
        items.append({
            "type": "mars",
            "date": p["earth_date"],
            "camera": p["camera"]["full_name"],
            "url": p["img_src"],  # ✅ ใช้ URL ตรงจาก NASA
            "rover": p["rover"]["name"]
        })

    # บันทึกใหม่
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

    print(f"✅ Saved {len(photos[:20])} Mars photos for {params['earth_date']}")
