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
        # 2. Autenticación usando la clase Siete (Según documentación oficial)
        siete = bcchapi.Siete(bcch_user, bcch_pass)
        
        # 3. Solicitar serie de la UF (Código: F073.UFF.PRE.Z.D)
        # Usamos el método 'cuadro'.
        # 'desde="2000-01-01"' asegura que traigamos historia para que el gráfico se vea bonito.
        df = siete.cuadro(
            series=["F073.UFF.PRE.Z.D"], 
            nombres=["valor"],            # Renombramos la columna automáticamente
            desde="2000-01-01",           # Traer datos históricos desde el año 2000
            frecuencia="D"                # Frecuencia Diaria
        )
        
        # 4. Limpieza y Transformación
        # La librería devuelve la fecha como ÍNDICE. La movemos a columna.
        df.reset_index(inplace=True)
        
        # Renombrar la columna del índice (que suele llamarse 'index' o venir sin nombre) a 'fecha'
        df.rename(columns={'index': 'fecha'}, inplace=True)
        
        # Si la columna de fecha quedó con otro nombre tras el reset, forzamos los nombres:
        # El DataFrame debería tener 2 columnas: [Fecha, Valor]
        if len(df.columns) == 2:
            df.columns = ['fecha', 'valor']
        
        # Asegurar tipos de datos
        df['fecha'] = pd.to_datetime(df['fecha'])
        df['valor'] = pd.to_numeric(df['valor'])
        
        print(f"✅ Extracción exitosa. {len(df)} registros obtenidos.")
        print(f"   Último dato: {df.iloc[-1]['fecha'].date()} -> {df.iloc[-1]['valor']}")
        
        return df

    except Exception as e:
        print(f"❌ Error crítico en API Banco Central: {e}")
        return pd.DataFrame()

# Bloque de prueba local
if __name__ == "__main__":
    df_test = extract_uf_data()
    if not df_test.empty:
        print("\nVista previa:")
        print(df_test.head())