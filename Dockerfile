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

# คัดลอกไฟล์ wait-for-it.sh เข้ามาใน container
COPY wait-for-it.sh /app/wait-for-it.sh

# เปลี่ยนสิทธิ์ให้ไฟล์ wait-for-it.sh สามารถรันได้
RUN chmod +x /app/wait-for-it.sh

# รัน migration และเริ่มเซิร์ฟเวอร์
CMD ["sh", "-c", "./wait-for-it.sh db:3306 -- python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
