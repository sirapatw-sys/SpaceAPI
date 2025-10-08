import os
import requests
import json
from pathlib import Path
from datetime import date

# ใช้ .env หรือ Environment Variables จาก Render
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")

DATA_DIR = Path(__file__).parent.parent / "data"
INDEX_FILE = DATA_DIR / "index.json"

# Also save images to Flask's static folder so hosting platforms can serve them
STATIC_DIR = Path(__file__).parent.parent / "static"
STATIC_IMAGES = STATIC_DIR / "images"

# สร้าง data directory ถ้ายังไม่มี
DATA_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)
STATIC_IMAGES.mkdir(parents=True, exist_ok=True)


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
    media_type = data.get("media_type", "image")
    img_url = data.get("hdurl") or data.get("url")

    local_path = None
    if media_type == "image" and img_url:
        img_name = img_url.split("/")[-1]
        dst = STATIC_IMAGES / img_name
        if not dst.exists():
            img_data = requests.get(img_url).content
            with open(dst, "wb") as f:
                f.write(img_data)
        # path relative to Flask static folder
        local_path = f"images/{img_name}"

    item = {
        "type": "apod",
        "title": data.get("title", "Unknown"),
        "date": data.get("date", str(date or "")),
        "url": img_url,
        "local_path": local_path,
        "explanation": data.get("explanation", ""),
        "media_type": media_type,
        "source": "APOD"
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
        img_url = p["img_src"]
        img_name = img_url.split("/")[-1]
        dst = STATIC_IMAGES / img_name
        if not dst.exists():
            img_data = requests.get(img_url).content
            with open(dst, "wb") as f:
                f.write(img_data)

        items.append({
            "type": "mars",
            "date": p["earth_date"],
            "camera": p["camera"]["full_name"],
            "url": img_url,
            "local_path": f"images/{img_name}",
            "rover": p["rover"]["name"],
            "source": "Mars Rover"
        })

    # บันทึกใหม่
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

    print(f"✅ Saved {len(photos[:20])} Mars photos for {params['earth_date']}")
