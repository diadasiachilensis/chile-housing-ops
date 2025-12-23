import os
import time
import psycopg2
import pandas as pd
from dotenv import load_dotenv

# --- IMPORTACIÓN MODULAR ---
# Importamos la función de extracción desde el otro script (extract_economic.py)
# Esto requiere que ambos archivos estén en la misma carpeta dentro del Docker
try:
    from extract_economic import extract_uf_data
except ImportError:
    # Fallback por si ejecutas esto fuera de la estructura de carpetas correcta
    print("⚠️ No se pudo importar extract_economic. Asegúrate de estar en la carpeta correcta.")
    from extract_economic import extract_uf_data

# Cargar variables de entorno (por si corres local sin Docker)
load_dotenv()

"""----- 1. CONFIGURACIÓN DE LA CONEXIÓN DB -----"""
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host     = os.getenv('POSTGRES_HOST', 'localhost'),
            database = os.getenv('POSTGRES_DB'),
            user     = os.getenv('POSTGRES_USER'),
            password = os.getenv('POSTGRES_PASSWORD')
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"⏳ La base de datos aún no está lista... Esperando. Error: {e}")
        return None

"""----- 2. FUNCIÓN DE CARGA (LOAD) -----"""
def load_uf_data(conn, df):
    """
    Recibe un DataFrame y lo inserta en PostgreSQL
    """
    if df is None or df.empty:
        print("⚠️ No hay datos nuevos para cargar.")
        return

    cursor = conn.cursor()
    
    insert_query = """
    INSERT INTO uf_data (date, value)
    VALUES (%s, %s)
    ON CONFLICT (date) DO NOTHING;
    """
    
    print(f"➡️ 📥 Iniciando carga de {len(df)} registros a PostgreSQL...")
    
    inserted_count = 0
    
    for index, row in df.iterrows():
        # Convertir timestamp de Pandas a date de Python
        date_obj = row['fecha'].date()
        value = row['valor']
        
        try:
            cursor.execute(insert_query, (date_obj, value))
            inserted_count += 1
        except Exception as e:
            print(f"❌ Error al insertar fila {date_obj}: {e}")
            conn.rollback() # Revertir solo esta transacción fallida

    # Guardar cambios permanentemente
    conn.commit()
    cursor.close()
    print(f"✅ Carga finalizada. {inserted_count} filas procesadas correctamente.")

"""----- 3. ORQUESTADOR PRINCIPAL -----"""
if __name__ == "__main__":
    print("🚀 Iniciando Pipeline ETL: Chile Housing Ops")
    
    # 1. Intentar conectar a la DB con reintentos (útil para Docker)
    conn = None
    max_retries = 5
    
    for i in range(max_retries):
        conn = get_db_connection()
        if conn:
            print("✅ Conexión exitosa a PostgreSQL")
            break
        print(f"⏳ Reintento {i+1}/{max_retries} en 5 segundos...")
        time.sleep(5)

    if conn:
        try:
            # 2. EXTRACCIÓN (Llamamos al especialista: extract_economic.py)
            # Esta función ya maneja la lógica de la API y bcchapi internamente
            df_uf = extract_uf_data()

            # 3. CARGA (Ejecutamos la carga con la conexión abierta)
            if not df_uf.empty:
                load_uf_data(conn, df_uf)
            else:
                print("⚠️ La extracción no devolvió datos. Saltando etapa de carga.")

        except Exception as e:
            print(f"❌ Error crítico en el pipeline: {e}")
        
        finally:
            conn.close()
            print("🔒 Conexión cerrada. Pipeline finalizado.")
    else:
        print("❌ Error fatal: No se pudo conectar a la base de datos después de varios intentos.")