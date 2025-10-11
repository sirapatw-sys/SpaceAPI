import os
import requests
import json
from pathlib import Path

# ใช้ .env หรือ Environment Variables จาก Render
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")

# โฟลเดอร์เก็บข้อมูลและภาพ
DATA_DIR = Path(__file__).parent.parent / "data"
IMAGES_DIR = DATA_DIR / "images"
INDEX_FILE = DATA_DIR / "index.json"

# สร้างโฟลเดอร์ถ้าไม่มี
DATA_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def fetch_apod(date: str | None = None):
    """Fetch NASA APOD และบันทึก metadata + ภาพใน data/images"""
    api_url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": NASA_API_KEY}
    if date:
        params["date"] = date

    print(f"Fetching APOD for date: {date or 'latest'}")
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    data = response.json()

    media_type = data.get("media_type", "image")
    img_url = data.get("hdurl") or data.get("url")

    local_path = None
    if media_type == "image" and img_url:
        img_name = img_url.split("/")[-1]
        dst = IMAGES_DIR / img_name
        if not dst.exists():
            img_data = requests.get(img_url).content
            with open(dst, "wb") as f:
                f.write(img_data)
        local_path = f"/data/images/{img_name}"

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

    items = []
    if INDEX_FILE.exists():
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                items = json.load(f)
        except json.JSONDecodeError:
            items = []

    items.append(item)

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

    print(f"✅ Saved APOD for {item['date']} ({item['title']})")


def fetch_mars(date: str | None = None):
    """Fetch NASA Mars Rover Photos และบันทึก metadata + ภาพใน data/images"""
    if date is None:
        # ดึง latest_photos
        api_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos"
        params = {"api_key": NASA_API_KEY}
    else:
        # ดึง photos ตามวัน
        api_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
        params = {"api_key": NASA_API_KEY, "earth_date": date}

    print(f"Fetching Mars photos for {date or 'latest'}")
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    data = response.json()

    photos = data.get("latest_photos", []) if date is None else data.get("photos", [])
    if not photos:
        print(f"⚠️ No Mars photos found for {date or 'latest'}.")
        return

    items = []
    if INDEX_FILE.exists():
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                items = json.load(f)
        except json.JSONDecodeError:
            items = []

    for p in photos[:20]:
        img_url = p["img_src"]
        img_name = img_url.split("/")[-1]
        dst = IMAGES_DIR / img_name
        if not dst.exists():
            img_data = requests.get(img_url).content
            with open(dst, "wb") as f:
                f.write(img_data)

        items.append({
            "type": "mars",
            "date": p["earth_date"],
            "camera": p["camera"]["full_name"],
            "url": img_url,
            "local_path": f"/data/images/{img_name}",
            "rover": p["rover"]["name"],
            "source": "Mars Rover"
        })

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

    print(f"✅ Saved {len(photos[:20])} Mars photos for {date or 'latest'}")
