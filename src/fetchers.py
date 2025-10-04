import os
import json
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()
NASA_API_KEY = os.environ.get("NASA_API_KEY", "DEMO_KEY")

DATA_DIR = Path(__file__).parent.parent / "data"
IMAGES_DIR = DATA_DIR / "images"
INDEX_FILE = DATA_DIR / "index.json"

DATA_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)

def fetch_apod():
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    img_url = data.get("hdurl") or data.get("url")
    img_name = img_url.split("/")[-1]
    local_path = IMAGES_DIR / img_name
    if not local_path.exists():
        img_data = requests.get(img_url).content
        with open(local_path, "wb") as f:
            f.write(img_data)

    item = {
        "title": data.get("title"),
        "date": data.get("date"),
        "url": img_url,
        "local_path": f"/data/images/{img_name}",
        "source": "APOD"
    }
    _append_index(item)

def fetch_mars():
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos?api_key={NASA_API_KEY}"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    for photo in data.get("latest_photos", []):
        img_url = photo["img_src"]
        img_name = img_url.split("/")[-1]
        local_path = IMAGES_DIR / img_name
        if not local_path.exists():
            img_data = requests.get(img_url).content
            with open(local_path, "wb") as f:
                f.write(img_data)

        item = {
            "title": f"{photo['rover']['name']} {photo['camera']['full_name']}",
            "date": photo["earth_date"],
            "url": img_url,
            "local_path": f"/data/images/{img_name}",
            "source": "Mars Rover"
        }
        _append_index(item)

def _append_index(item: dict):
    data = []
    if INDEX_FILE.exists():
        if INDEX_FILE.stat().st_size > 0:  # file not empty
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
    data.append(item)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
