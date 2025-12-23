# api/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 1. Instalar curl para el Healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 2. Copiar requirements e instalar dependencias (Caché Layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copiar el contenido de la carpeta 'api'
# Esto buscará 'app.py' dentro de tu carpeta api local y lo pondrá en /app/
COPY api/ .

# 4. Exponer el puerto
EXPOSE 8000

# 5. Healthcheck (Verifica que la API responda en la raíz)
HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1

# 6. Ejecutar uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]