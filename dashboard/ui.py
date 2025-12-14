import streamlit as st
import pandas as pd
import requests
import os

# --- 1. Configuración de la API ---
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = 8000
API_URL = f"http://{API_HOST}:{API_PORT}/uf_history"

# --- 2. Configuración de la página Streamlit ---
st.set_page_config(
    page_title="Chile Housing Ops Dashboard",
    layout="wide"
)

# --- 3. Encabezado ---
st.title("🏠 Chile Housing Data: Histórico de UF")
st.markdown("Dashboard de ejemplo que consume datos de la API FastAPI y PostgreSQL.")

# --- 4. Función de Extracción de Datos de la API ---
@st.cache_data(ttl=600)
def get_uf_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        
        data = response.json()
        df = pd.DataFrame(data)
        
        # FIX: Normalizar nombres de columnas a minúsculas para evitar KeyError
        df.columns = df.columns.map(str).str.lower()
        
        # Aseguramos que 'date' sea un objeto datetime para manipulación
        df["date"] = pd.to_datetime(df["date"]).dt.date

        # Formatear el valor de la UF para visualización
        df['value_clp'] = df['value'].apply(lambda x: f"${x:,.2f}").str.replace(',', 'TEMP').str.replace('.', ',').str.replace('TEMP', '.')
        
        return df
        
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error al conectar con la API ({API_HOST}:{API_PORT}). Asegúrese de que el servicio 'api' esté corriendo.")
        st.caption(f"Detalles: {e}")
        return pd.DataFrame()

# --- 5. Visualización de los Datos ---
uf_df = get_uf_data()

if not uf_df.empty:
    st.header("Valores Históricos de UF")

    uf_df["date"] = pd.to_datetime(uf_df["date"]).dt.date
    uf_df["value"] = pd.to_numeric(uf_df["value"], errors="coerce")
    uf_df = uf_df.sort_values("date")

    st.line_chart(uf_df.set_index("date")[["value"]])

    st.table(uf_df[["date", "value_clp"]])

    latest_uf = uf_df.iloc[-1]["value_clp"]
    st.metric(label="Último Valor UF Registrado (CLP)", value=latest_uf)
else:
    st.warning("No se pudieron cargar los datos de la UF.")
