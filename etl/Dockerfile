# etl/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 1. Primero copiamos solo requirements e instalamos (para aprovechar caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. CRÍTICO: Copiamos TODO el contenido de la carpeta 'etl' al directorio actual de trabajo (/app)
# Esto asegura que main.py Y extract_economic.py se copien juntos.
COPY etl/ .

# 3. Comando por defecto (aunque docker-compose lo sobrescribe, es bueno tenerlo)
CMD ["python", "main.py"]