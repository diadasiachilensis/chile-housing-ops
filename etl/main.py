import os
import requests
import psycopg2
from datetime import datetime

"""----- CONFIGURACION DE LA CONEXIÓN DB -----"""
#funcion que sera llamada para abrir la conexión a la base de datos
def get_db_connection():
    return psycopg2.connect(                        #con psycopg2, estabelce la conexion con todos los parametros y devuelve el objeto de conexion 
        host     = os.getenv('POSTGRES_HOST'),      #obtiene el valor de DB desde la variable de entorno POSTGRES_HOST. Es Docker Compose, este valor es postgres
        database = os.getenv('POSTGRES_DB'),        #obtiene el nombre de la DB desde la variable de entorno
        user     = os.getenv('POSTGRES_USER'),      #obtiene el nombre de la base de datos chile_housing desde la varaible de entorno
        password = os.getenv('POSTGRES_PASSWORD')   #obtiene la contraseña desde la varible de entorno
    )

"""----- FUNCIÓN DE EXTRACCIÓN (Simulación de API UF) -----"""
#funcion que simula la llamada a un API real para obtener los datos de la UF
#por simplicidad, se simulara los datos para 3 días

def extract_uf_data():
    print("➡️ 🔄 Extrayendo datos simulados de la UF… 📊💱")

    #Formato: (Fecha, Valor_UF)
    uf_data = [
        ('2025-12-10', 38000.50),
        ('2025-12-11', 38005.75),
        ('2025-12-12', 38010.10)
    ]

    return uf_data

"""----- FUNCIÓN DE CARGA (LOAD) -----"""
#define la funcion para la fase de CARGA (L en ETL) Recibe el objeto de conexión (conn) y los datos (uf_data)

def load_uf_data(conn, uf_data):
    
    #crea un cursor. El cursor es un objeto que permite enviar comandos SQL a la DB y manejar los resutlados.
    cursor = conn.cursor() 

    # define consulta SQL (CORRECCIÓN: data -> date y : -> ;)
    insert_query = """
    INSERT INTO uf_data (date, value)
    VALUES (%s, %s)
    ON CONFLICT (date) DO NOTHING;
    """
    #La clave es: ON CONFLICT (date) DO NOTHING;. Esto evita errores si intentamos cargar la misma fecha dos veces (la date es la clave primaria).

    print(f"➡️ 📥 Cargando {len(uf_data)} valores de UF en la tabla uf_data...") 

    #Itera sobre cada tupla (registro) en la lista de datos de la UF.
    for date_str, value in uf_data:
        #Convierte la cadena de texto de la fecha ('2025-12-10') en un objeto de fecha real de Python, que es lo que PostgreSQL espera.
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        try: 
            #Ejecuta la consulta SQL, reemplazando %s con los valores de la tupla (date_obj y value).
            cursor.execute(insert_query, (date_obj,value))
        except Exception as e:
            print(f"❌⚠️ Error al cargar UF para {date_str}: {e}")
            conn.rollback()                                         #Revertir la transacción si falla una fila

    #Confirma la transacción. Esto hace que todos los cambios (inserciones) sean permanentes en la base de datos.
    conn.commit()
    print("✅➡️ Carga de datos UF completada.")
    #cierra el cursor para liberar recrusos
    cursor.close()

"""----- FUNCIÓN PRINCIPAL DEL PIPELINE -----"""
if __name__ == "__main__":
    conn = None
    try:
        # 1. Conexión 
        #Intenta abrir la conexión a la DB. Si falla, el programa salta al bloque except.
        conn = get_db_connection()
        print("✅ Conexión exitosa a PostgreSQL")

        # 2. Extracción
        # Llama a la función que extrae los datos.
        data = extract_uf_data()

        # 3. Carga
        #Llama a la función que inserta los datos en PostgreSQL.
        load_uf_data(conn,data)

    #Captura errores específicos de la base de datos (ej. credenciales incorrectas, host no encontrado).
    except psycopg2.Error as e:
        print(f"❌🗄️ Error de base de datos: {e}")
    
    #Bloque que se ejecuta siempre, haya habido error o no.
    except Exception as e:
        print(f"❌🗄️ Ocurrió un error inesperado: {e}")

    finally:
        #Si la conexión se abrió (conn no es None), se asegura de cerrarla para liberar el recurso de la base de datos.
        if conn:
            conn.close()
            print("Conexión a PostgreSQL cerrada")