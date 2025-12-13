import os
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

"""--- 1. MODELO DE DATOS (Pydantic Schema) ---"""
# Define la estructura de los datos que la API devolverá (response model)
class UFDara(BaseModel):    #Define una clase que hereda de BaseModel. Esta clase actúa como un contrato o esquema de datos.
    date: date              #Especifica que el campo date debe ser un objeto de fecha válido (date de Python).
    value: float            #Especifica que el campo value debe ser un número de punto flotante (decimal).

#Asegura que cuando un cliente pida datos de la UF, siempre obtenga objetos que cumplen exactamente esta forma.

"""--- 2. CONFIGURACIÓN DE LA CONEXIÓN DB ---"""
def get_db_connection():
    # Las variables de entorno son inyectadas por docker-compose desde el archivo .env
    return psycopg2.connect(                        #con psycopg2, estabelce la conexion con todos los parametros y devuelve el objeto de conexion 
        host     = os.getenv('POSTGRES_HOST'),      #obtiene el valor de DB desde la variable de entorno POSTGRES_HOST. Es Docker Compose, este valor es postgres
        database = os.getenv('POSTGRES_DB'),        #obtiene el nombre de la DB desde la variable de entorno
        user     = os.getenv('POSTGRES_USER'),      #obtiene el nombre de la base de datos chile_housing desde la varaible de entorno
        password = os.getenv('POSTGRES_PASSWORD')   #obtiene la contraseña desde la varible de entorno
    )

