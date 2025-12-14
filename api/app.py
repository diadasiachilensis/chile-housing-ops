import os  # Módulo para interactuar con el sistema operativo (necesario para leer variables de entorno).
import psycopg2  # Librería que permite a Python conectarse y comunicarse con PostgreSQL.
from fastapi import FastAPI, HTTPException  # Importa el framework principal para el servidor web y la clase para manejar errores HTTP.
from pydantic import BaseModel  # Clase base para definir esquemas de datos y asegurar su validación.
from typing import List, Optional  # Módulos de tipado de Python para indicar que se devuelve una lista de objetos.
from datetime import date  # Clase para manejar el tipo de dato fecha.

"""--- 1. MODELO DE DATOS (Pydantic Schema) ---"""
# Define la estructura de los datos que la API devolverá (response model)
class UFData(BaseModel):  # Define el esquema de datos esperado para un registro de UF.
    date: date  # El campo 'date' debe ser un objeto de fecha válido.
    value: float  # El campo 'value' debe ser un número decimal (punto flotante).
    
""" --- 2. CONFIGURACIÓN DE LA CONEXIÓN DB ---"""
def get_db_connection():  # Define la función encargada de abrir la conexión a la base de datos.
    # Las variables de entorno son inyectadas por docker-compose desde el archivo .env
    return psycopg2.connect(  # Intenta establecer y retornar el objeto de conexión a PostgreSQL.
        host=os.getenv('POSTGRES_HOST'),  # Obtiene el nombre del servicio DB ('postgres') desde las variables de entorno.
        database=os.getenv('POSTGRES_DB'),  # Obtiene el nombre de la base de datos ('chile_housing').
        user=os.getenv('POSTGRES_USER'),  # Obtiene el usuario de la base de datos ('admin').
        password=os.getenv('POSTGRES_PASSWORD')  # Obtiene la contraseña de la base de datos ('password').
    )

"""--- 3. INICIALIZACIÓN DE LA APLICACIÓN ---"""
# Crea una instancia de FastAPI
app = FastAPI(  # Crea la instancia principal de la aplicación FastAPI.
    title="Chile Housing Ops API",  # Título para la documentación automática (en /docs).
    description="API para servir datos históricos de la UF y análisis de propiedades.",  # Descripción para la documentación.
    version="1.0.0"  # Versión de la API.
)

"""--- 4. ENDPOINT PRINCIPAL (Root) ---"""
@app.get("/", tags=["Healthcheck"])  # Decorador: Asocia la función a las solicitudes GET en la ruta raíz (/).
def read_root():  # Define la función que maneja la solicitud GET /.
    return {"status": "ok", "service": "Chile Housing Ops API"}  # Devuelve una respuesta JSON simple (Healthcheck).

"""--- 5. ENDPOINT DE DATOS (UF History) ---"""
@app.get("/uf_history", response_model=List[UFData], tags=["Data"])  # Decorador: Asocia la función a solicitudes GET en /uf_history.
def get_uf_history():  # Define la función que recupera el historial de la UF.
    conn = None  # Inicializa la variable de conexión a None (necesario para el bloque 'finally').
    try:  # Inicia el bloque para manejar errores de conexión/DB.
        conn = get_db_connection()  # Intenta establecer la conexión con la base de datos.
        cursor = conn.cursor()  # Crea un objeto cursor para ejecutar comandos SQL.
        
        # Consulta SQL para obtener todos los datos de la UF
        query = "SELECT date, value FROM uf_data ORDER BY date DESC;"  # Define la consulta SQL para obtener fecha y valor ordenados.
        cursor.execute(query)  # Ejecuta la consulta SQL definida por la variable 'query'.
        
        # Obtener todos los resultados
        results = cursor.fetchall()  # Recupera todas las filas resultantes de la consulta como una lista de tuplas.
        
        # Mapear los resultados de la base de datos al esquema Pydantic (UFData)
        # Esto convierte cada tupla (date, value) en un diccionario
        uf_history = [{"date": row[0], "value": row[1]} for row in results]  # Convierte las tuplas (row) en diccionarios para Pydantic.
        
        return uf_history  # Devuelve la lista de datos mapeados, que FastAPI serializa a JSON.
        
    except psycopg2.Error as e:  # Captura errores específicos que provienen del adaptador de PostgreSQL.
        print(f"Error de base de datos en /uf_history: {e}")  # Imprime el error en los logs del servidor para depuración.
        # Lanza un error HTTP 500 si la base de datos falla
        raise HTTPException(status_code=500, detail="Database connection error.")  # Responde al cliente con un error 500.
        
    finally:  # Bloque que siempre se ejecuta, sin importar si hubo éxito o error.
        if conn:  # Verifica si la conexión a la DB se estableció (si 'conn' no es None).
            conn.close()  # Cierra la conexión a PostgreSQL para liberar recursos.