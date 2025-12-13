FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
COPY api/app.py /app/app.py
RUN pip install --no-cache-dir -r requirements.txt
# Comando de arranque (usaremos uvicorn para ejecutar la API)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
