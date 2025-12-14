FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
COPY dashboard/ui.py /app/ui.py
RUN pip install --no-cache-dir -r requirements.txt
# Comando de arranque (usaremos streamlit para ejecutar la UI)
CMD ["streamlit", "run", "ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
