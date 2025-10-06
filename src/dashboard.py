from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
from pathlib import Path
import json
try:
    # when running as a script (python src/main.py) fetchers is a top-level module
    from fetchers import fetch_apod, fetch_mars
except Exception:
    # when imported as a package (import src.main) use package-qualified import
    from src.fetchers import fetch_apod, fetch_mars

DATA_DIR = Path(__file__).parent.parent / "data"
INDEX_FILE = DATA_DIR / "index.json"

app = Flask(__name__, template_folder="../templates")
app.secret_key = "dev-secret"  # lightweight flash messages for UI

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


@app.route('/fetch/apod', methods=['POST'])
def web_fetch_apod():
    """Trigger fetch_apod from the web UI. Accepts optional 'date' form field."""
    date = request.form.get('date') or None
    try:
        fetch_apod(date=date)
        flash('APOD fetched successfully', 'success')
    except Exception as e:
        flash(f'Error fetching APOD: {e}', 'danger')
    return redirect(url_for('index'))


@app.route('/fetch/mars', methods=['POST'])
def web_fetch_mars():
    """Trigger fetch_mars from the web UI. Accepts optional 'date' form field."""
    date = request.form.get('date') or None
    try:
        fetch_mars(date=date)
        flash('Mars photos fetched successfully', 'success')
    except Exception as e:
        flash(f'Error fetching Mars photos: {e}', 'danger')
    return redirect(url_for('index'))

@app.route("/data/images/<path:filename>")
def serve_images(filename):
    return send_from_directory(DATA_DIR / "images", filename)

def serve():
    app.run(host="0.0.0.0", port=5500, debug=True)
