# dashboard/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 1. Instalamos curl para que funcione el Healthcheck
# (Las imágenes 'slim' no lo traen por defecto)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 2. Copiamos requirements desde la raíz (contexto de docker-compose)
COPY requirements.txt .

# 3. Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiamos el código del dashboard
COPY dashboard/ui.py /app/ui.py

# 5. Exponer el puerto
EXPOSE 8501

# 6. Healthcheck para verificar que Streamlit responda
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 7. Ejecutar
CMD ["streamlit", "run", "ui.py", "--server.port=8501", "--server.address=0.0.0.0"]