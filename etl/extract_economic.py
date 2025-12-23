import os
import pandas as pd
import bcchapi
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno (útil si lo corres localmente fuera de Docker)
load_dotenv()

def extract_uf_data():
    """
    Conecta a la API del Banco Central de Chile y extrae los datos de la UF.
    Retorna: DataFrame de Pandas con columnas ['fecha', 'valor']
    """
    print("➡️ 🔄 Iniciando extracción de UF desde Banco Central...")

    # 1. Obtener credenciales de las variables de entorno
    bcch_user = os.getenv('BCCH_USER')
    bcch_pass = os.getenv('BCCH_PASS')

    # Validación de seguridad
    if not bcch_user or not bcch_pass:
        print("❌ Error: Faltan credenciales (BCCH_USER o BCCH_PASS).")
        return pd.DataFrame()

    try:
        # 2. Autenticación con la librería oficial
        banco = bcchapi.BancoCentral(bcch_user, bcch_pass)
        
        # 3. Solicitar serie de la UF (Código oficial: F073.UFF.PRE.Z.D)
        # Nota: Por defecto trae los últimos datos. 
        # Si quieres historia completa, puedes agregar argumentos de fecha, 
        # pero para el flujo diario esto basta.
        df = banco.get_series('F073.UFF.PRE.Z.D')
        
        # 4. Limpieza y Transformación (Pandas)
        # La librería devuelve la fecha como índice. La movemos a columna.
        df.reset_index(inplace=True)
        
        # Renombrar columnas para estandarizar (index -> fecha, valor -> valor)
        # La librería suele poner el código de la serie como nombre de columna.
        # Lo forzamos a nombres amigables.
        df.columns = ['fecha', 'valor']
        
        # Asegurar tipos de datos correctos
        df['fecha'] = pd.to_datetime(df['fecha'])
        df['valor'] = pd.to_numeric(df['valor'])
        
        print(f"✅ Extracción exitosa. {len(df)} registros obtenidos.")
        print(f"   Último dato: {df.iloc[-1]['fecha'].date()} -> {df.iloc[-1]['valor']}")
        
        return df

    except Exception as e:
        print(f"❌ Error crítico en API Banco Central: {e}")
        # Retornamos DataFrame vacío para no romper el pipeline, pero avisamos el error
        return pd.DataFrame()

# Bloque de prueba (solo se ejecuta si corres este script directamente)
if __name__ == "__main__":
    df_test = extract_uf_data()
    if not df_test.empty:
        print("\nVista previa de los datos:")
        print(df_test.head())