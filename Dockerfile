# ใช้ Python 3.9 เป็น base image
FROM python:3.9

# กำหนด working directory ใน container
WORKDIR /app

# คัดลอกไฟล์ requirements.txt ไปยัง container
COPY requirements.txt .

# ติดตั้ง dependencies
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์โปรเจกต์ทั้งหมดไปยัง container
COPY . .

# รัน migration และเริ่มเซิร์ฟเวอร์
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]