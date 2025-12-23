import os
import pandas as pd
import bcchapi
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

def extract_uf_data():
    """
    Conecta a la API del Banco Central de Chile (SIETE) y extrae los datos de la UF.
    Retorna: DataFrame de Pandas con columnas ['fecha', 'valor']
    """
    print("➡️ 🔄 Iniciando extracción de UF desde Banco Central (Clase Siete)...")

    # 1. Obtener credenciales
    bcch_user = os.getenv('BCCH_USER')
    bcch_pass = os.getenv('BCCH_PASS')

    if not bcch_user or not bcch_pass:
        print("❌ Error: Faltan credenciales (BCCH_USER o BCCH_PASS).")
        return pd.DataFrame()

    try:
        # 2. Autenticación
        siete = bcchapi.Siete(bcch_user, bcch_pass)
        
        # 3. Solicitar serie de la UF (Código: F073.UFF.PRE.Z.D)
        # CORRECCIÓN: Agregamos el parámetro 'observado' que es obligatorio.
        df = siete.cuadro(
            series=["F073.UFF.PRE.Z.D"], 
            nombres=["valor"],            
            desde="2023-01-01",           # Traemos desde 2023 para que sea rápido y ligero
            frecuencia="D",
            observado={"valor": "last"}   # <--- ¡ESTO FALTABA!
        )
        
        # 4. Limpieza y Transformación
        # La librería devuelve la fecha como ÍNDICE. La movemos a columna.
        df.reset_index(inplace=True)
        
        # Renombrar la columna del índice a 'fecha'
        df.rename(columns={'index': 'fecha'}, inplace=True)
        
        # Validación de columnas
        if len(df.columns) == 2:
            df.columns = ['fecha', 'valor']
        
        # Asegurar tipos de datos
        df['fecha'] = pd.to_datetime(df['fecha'])
        df['valor'] = pd.to_numeric(df['valor'])
        
        print(f"✅ Extracción exitosa. {len(df)} registros obtenidos.")
        try:
            print(f"   Último dato: {df.iloc[-1]['fecha'].date()} -> {df.iloc[-1]['valor']}")
        except:
            pass
        
        return df

    except Exception as e:
        print(f"❌ Error crítico en API Banco Central: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    df_test = extract_uf_data()
    if not df_test.empty:
        print("\nVista previa:")
        print(df_test.head())