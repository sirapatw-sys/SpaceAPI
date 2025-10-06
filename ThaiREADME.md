นี่คือเวอร์ชัน **README.md ภาษาไทย** สำหรับโปรเจกต์ SpaceAPI ของคุณ:

---

# SpaceAPI

โปรเจกต์ Python/Flask ง่าย ๆ สำหรับดึงและแสดง **ภาพดาราศาสตร์ประจำวัน (APOD)** ของ NASA และ **ภาพจากยานสำรวจดาวอังคาร** ในรูปแบบแกลเลอรีที่สะอาดและตอบสนองดี

---

## ฟีเจอร์

* ดึงภาพ APOD ของ NASA โดยอัตโนมัติ
* ดึงภาพล่าสุดจากยานสำรวจดาวอังคาร (Curiosity)
* บันทึกภาพลงในเครื่องพร้อมจัดเก็บ metadata ใน `data/index.json`
* แกลเลอรี Flask แบบ responsive สำหรับดูภาพเต็ม
* รองรับ lazy-loading เพื่อให้เลื่อนดูภาพจำนวนมากได้อย่างราบรื่น
* สามารถดึงภาพ APOD ตามวันที่ที่ระบุได้

---

## โครงสร้างโฟลเดอร์

```
SpaceAPI/
├─ data/ # ภาพดาวน์โหลด & metadata
│ ├─ images/
│ └─ index.json
├─ src/
│ ├─ main.py # จุดเริ่มต้น & CLI
│ ├─ fetchers.py # ฟังก์ชันดึง APOD & Mars
│ └─ dashboard.py # แกลเลอรี Flask
├─ templates/
│ └─ index.html # HTML template สำหรับแกลเลอรี (grid แบบ responsive)
├─ README.md
└─ requirements.txt
```

---

## การติดตั้ง

โคลนรีโพสิทอรี:

```bash
git clone https://github.com/yourusername/SpaceAPI.git
cd SpaceAPI
```

สร้าง virtual environment (แนะนำเพื่อแยก dependencies):

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

ติดตั้ง dependencies:

```bash
pip install -r requirements.txt
```

ตั้งค่า NASA API key ในไฟล์ `.env`:

```
NASA_API_KEY=YOUR_API_KEY_HERE
```

---

## การใช้งาน

1. **ดึงภาพ APOD** (สามารถระบุวันที่ `YYYY-MM-DD` ได้):

```bash
python src/main.py fetch-apod
python src/main.py fetch-apod --date 2025-10-06
```

2. **ดึงภาพยานสำรวจดาวอังคาร**:

```bash
python src/main.py fetch-mars
```

3. **รันแกลเลอรีในเครื่อง**:

```bash
python src/main.py serve
```

เปิดเบราว์เซอร์ที่ [http://localhost:5500](http://localhost:5500) เพื่อดูภาพทั้งหมด

---

## หมายเหตุ

* ภาพทั้งหมดถูกเก็บไว้ที่ `data/images/`

* `data/index.json` เก็บ metadata เช่น:

  * `title` – ชื่อภาพ
  * `date` – วันที่
  * `local_path` – พาธในเครื่อง
  * `source` – แหล่งที่มา
  * `rover` และ `camera` (สำหรับภาพดาวอังคาร)

* แกลเลอรีจะแสดงภาพล่าสุดก่อนอัตโนมัติ

---

## Dependencies

* Python 3.11+
* Flask
* Requests
* python-dotenv

ติดตั้งทั้งหมดด้วยคำสั่ง:

```bash
pip install -r requirements.txt
```

---
