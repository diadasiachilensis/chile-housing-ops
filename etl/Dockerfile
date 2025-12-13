FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
COPY etl/main.py /app/main.py
# Ahora descomentamos la línea de instalación
RUN pip install --no-cache-dir -r requirements.txt
