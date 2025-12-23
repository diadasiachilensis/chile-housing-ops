import streamlit as st
import pandas as pd
import requests
import os
import plotly.express as px  # Librería para gráficos interactivos

# --- 1. Configuración ---
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = 8000
# Al usar Docker, API_HOST será 'api'
API_URL = f"http://{API_HOST}:{API_PORT}/uf_history"

st.set_page_config(page_title="Chile Economic Pulse", layout="wide", page_icon="🇨🇱")

# --- 2. Título y Estilo ---
st.title("🇨🇱 Indicadores Macroeconómicos: Unidad de Fomento (UF)")
st.markdown("""
Esta visualización consume datos reales extraídos directamente del **Banco Central de Chile** a través de nuestro pipeline ETL automatizado.
""")

# --- 3. Función de Carga ---
@st.cache_data(ttl=3600) # Cache por 1 hora ya que la UF cambia diario
def get_uf_data():
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            return pd.DataFrame()
            
        df = pd.DataFrame(data)
        
        # Limpieza de tipos
        df["date"] = pd.to_datetime(df["date"])
        df["value"] = pd.to_numeric(df["value"])
        
        # Ordenar cronológicamente
        df = df.sort_values("date")
        
        return df
        
    except Exception as e:
        st.error(f"⚠️ No se pudo conectar con la API en {API_URL}")
        st.caption(str(e))
        return pd.DataFrame()

# --- 4. Renderizado ---
df = get_uf_data()

if not df.empty:
    # --- KPIs Principales ---
    col1, col2, col3 = st.columns(3)
    
    # Obtener último valor y penúltimo para calcular variación
    latest_rec = df.iloc[-1]
    prev_rec = df.iloc[-2] if len(df) > 1 else latest_rec
    
    val_actual = latest_rec['value']
    delta_val = val_actual - prev_rec['value']
    
    with col1:
        st.metric(
            label=f"Valor UF ({latest_rec['date'].strftime('%d-%m-%Y')})",
            value=f"${val_actual:,.2f}",
            delta=f"${delta_val:,.2f} (vs ayer)"
        )
    
    with col2:
        st.metric(label="Registros Totales", value=len(df))

    # --- Gráfico de Tendencia con Plotly ---
    st.subheader("📈 Evolución Histórica")
    
    # Crear el objeto figura de Plotly
    fig = px.line(
        df, 
        x="date", 
        y="value",
        title="Evolución del Valor de la UF",
        labels={"value": "Valor (CLP)", "date": "Fecha"}
    )
    
    # Personalización del Gráfico
    fig.update_traces(
        line_color="#FF4B4B",  # Color rojo 'Housing'
        hovertemplate="<b>Fecha:</b> %{x}<br><b>Valor:</b> $%{y:,.2f}<extra></extra>" # Formato moneda en tooltip
    )
    
    fig.update_layout(
        hovermode="x unified",  # Muestra una línea vertical al pasar el mouse
        template="plotly_white", # Fondo limpio
        xaxis_title="",
        yaxis_title="Valor en Pesos ($)",
        height=500
    )

    # Renderizar en Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # --- Tabla de Datos ---
    with st.expander("Ver tabla de datos completa"):
        # Formatear para mostrar
        display_df = df.copy()
        display_df['value'] = display_df['value'].apply(lambda x: f"${x:,.2f}")
        display_df['date'] = display_df['date'].dt.date
        st.dataframe(display_df.sort_values('date', ascending=False), use_container_width=True)

else:
    st.info("Esperando ejecución del ETL para poblar datos...")