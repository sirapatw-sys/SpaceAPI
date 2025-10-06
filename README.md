# SpaceAPI

A simple Python/Flask project to fetch and display NASA’s **Astronomy Picture of the Day (APOD)** and **Mars rover images** in a clean, responsive gallery.

---

## Features

* Fetch NASA APOD images automatically.
* Fetch the latest Mars rover photos (Curiosity).
* Save images locally and maintain metadata in `data/index.json`.
* Responsive Flask gallery to view images in full.
* Lazy-loading for smooth scrolling of large image collections.
* Option to fetch APOD for a specific date.

---

## Folder Structure

```
SpaceAPI/
├─ data/ # Downloaded images & metadata
│ ├─ images/
│ └─ index.json
├─ src/
│ ├─ main.py # Entry point & CLI
│ ├─ fetchers.py # APOD & Mars fetch logic
│ └─ dashboard.py # Flask gallery
├─ templates/
│ └─ index.html # HTML template for gallery (responsive grid)
├─ README.md
└─ requirements.txt
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/SpaceAPI.git
cd SpaceAPI
```

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set up your NASA API key in a `.env` file:

```
NASA_API_KEY=YOUR_API_KEY_HERE
```

---

## Usage

1. **Fetch APOD images** (optionally for a specific date `YYYY-MM-DD`):

```bash
python src/main.py fetch-apod
python src/main.py fetch-apod --date 2025-10-06
```

2. **Fetch Mars rover images**:

```bash
python src/main.py fetch-mars
python src/main.py fetch-mars --date 2025-10-06
```

3. **Serve the gallery locally**:

```bash
python src/main.py serve
```

Open your browser at [http://localhost:5500](http://localhost:5500) to view all images.

---

## Notes

* All images are stored in `data/images/`.
* `data/index.json` contains metadata:

  * `title`
  * `date`
  * `local_path`
  * `source`
  * `rover` and `camera` (for Mars photos)
* The gallery automatically shows the newest images first.

---

## Dependencies

* Python 3.11+
* Flask
* Requests
* python-dotenv

Install all dependencies via:

```bash
pip install -r requirements.txt
```
