from flask import Flask, render_template_string, send_from_directory
from pathlib import Path
import json

DATA_DIR = Path(__file__).parent.parent / "data"
INDEX_FILE = DATA_DIR / "index.json"

TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NASA Gallery</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body { background-color: #f8f9fa; }
h1 { text-align: center; margin: 2rem 0; }
.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    padding: 1rem;
}
.card {
    background: white;
    border-radius: 0.5rem;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.card img {
    width: 100%;
    height: auto;         /* full image height */
    object-fit: contain;  /* show entire image */
    display: block;
}
.card-body {
    padding: 0.5rem;
    text-align: center;
}
.card-title {
    font-size: 0.9rem;
    font-weight: 600;
    margin: 0;
}
</style>
</head>
<body>
<h1>🚀 NASA Gallery</h1>
<div class="gallery">
{% for item in items %}
<div class="card">
    <img src="{{ item.local_path }}" alt="{{ item.title }}" loading="lazy">
    <div class="card-body">
        <p class="card-title">{{ item.title }}</p>
        <small>{{ item.date }} | {{ item.source }}</small>
    </div>
</div>
{% endfor %}
</div>
</body>
</html>
"""

app = Flask(__name__)

@app.route("/")
def index():
    items = []
    if INDEX_FILE.exists():
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                items = json.load(f)
        except json.JSONDecodeError:
            items = []
    items = list(reversed(items))  # show newest first
    return render_template_string(TEMPLATE, items=items)

@app.route("/data/images/<path:filename>")
def serve_images(filename):
    return send_from_directory(DATA_DIR / "images", filename)

def serve():
    app.run(host="0.0.0.0", port=5500, debug=True)
