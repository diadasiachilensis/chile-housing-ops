import os
import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import date

# --- 1. MODELO DE DATOS ---
class UFData(BaseModel):
    date: date
    value: float

# --- 2. CONFIGURACIÓN DB ---
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD')
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ Error de conexión DB: {e}")
        return None

# --- 3. APP FASTAPI ---
app = FastAPI(
    title="Chile Housing Ops API",
    description="API que sirve indicadores económicos reales (Banco Central) y datos inmobiliarios.",
    version="1.1.0"
)

# Configuración de CORS (Permite que el Dashboard consuma la API sin problemas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, cambia esto por la IP específica del dashboard
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Healthcheck"])
def read_root():
    return {"status": "ok", "service": "Chile Housing Ops API running"}

@app.get("/uf_history", response_model=List[UFData], tags=["Economics"])
def get_uf_history():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            raise HTTPException(status_code=503, detail="Database not available")
            
        cursor = conn.cursor()
        
        # Ordenamos ASC (cronológico) para que los gráficos se dibujen bien de izquierda a derecha
        query = "SELECT date, value FROM uf_data ORDER BY date ASC;" 
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Mapeo a lista de diccionarios
        uf_history = [{"date": row[0], "value": row[1]} for row in results]
        
        return uf_history
        
    except psycopg2.Error as e:
        print(f"❌ DB Error query: {e}")
        raise HTTPException(status_code=500, detail="Error ejecutando consulta en base de datos")
        
    finally:
        if conn:
            conn.close()