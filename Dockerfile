# 1. ใช้ Python 3.11 base image
FROM python:3.11-slim

# 2. ตั้ง working directory ใน container
WORKDIR /app

# 3. คัดลอกไฟล์ requirements.txt ไปก่อน เพื่อ cache การติดตั้ง dependencies
COPY requirements.txt .

# 4. ติดตั้ง dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. คัดลอกไฟล์โปรเจกต์ทั้งหมดไปใน container
COPY . .

# 6. กำหนด environment variables
ENV FLASK_ENV=production
ENV NASA_API_KEY="a1IpVQQllCVpJ40EiscMZEoYmMXiDuv2ZzQbrNus"
ENV PORT=5500

# 7. เปิด port ที่ container จะใช้
EXPOSE 5500

# 8. สั่งให้รัน Flask app
CMD ["python", "src/main.py", "serve"]
