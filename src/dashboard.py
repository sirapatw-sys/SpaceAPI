from flask import Flask, render_template, send_from_directory
from pathlib import Path
import json

DATA_DIR = Path(__file__).parent.parent / "data"
INDEX_FILE = DATA_DIR / "index.json"

app = Flask(__name__, template_folder="../templates")

@app.route("/")
def index():
    items = []
    if INDEX_FILE.exists():
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                items = json.load(f)
        except json.JSONDecodeError:
            items = []
    items = list(reversed(items))  # newest first
    return render_template("index.html", items=items)

@app.route("/data/images/<path:filename>")
def serve_images(filename):
    return send_from_directory(DATA_DIR / "images", filename)

def serve():
    app.run(host="0.0.0.0", port=5500, debug=True)
