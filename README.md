# SpaceAPIA simple Python/Flask project to fetch and display NASA’s Astronomy Picture of the Day (APOD) and Mars rover images in a clean, responsive gallery.

Features

Fetch NASA APOD images automatically.

Fetch latest Mars rover photos (Curiosity).

Save images locally and maintain metadata in data/index.json.

Responsive Flask gallery to view images in full.

Lazy-loading for smooth scrolling of large image collections.

Folder Structure
SpaceAPI/
├─ data/                 # Downloaded images & index.json
│  ├─ images/
│  └─ index.json
├─ src/
│  ├─ main.py            # Entry point & CLI
│  ├─ fetchers.py        # APOD & Mars fetch logic
│  └─ dashboard.py       # Flask gallery
├─ README.md
└─ requirements.txt

Installation

Clone the repository:

git clone https://github.com/yourusername/SpaceAPI.git
cd SpaceAPI


Create a virtual environment (optional but recommended):

python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux


Install dependencies:

pip install -r requirements.txt

Usage
1. Fetch APOD images:
python src/main.py fetch-apod

2. Fetch Mars rover images:
python src/main.py fetch-mars

3. Serve the gallery locally:
python src/main.py serve


Open your browser at http://localhost:5500
 to view all images.

Notes

All images are stored in data/images/.

data/index.json contains metadata (title, date, local path, source, rover, camera).

The gallery automatically shows the newest images first.

Dependencies

Python 3.11+

Flask

Requests

Install all dependencies via:

pip install -r requirements.txt
