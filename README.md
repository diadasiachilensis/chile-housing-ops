# 🏠 Chile Housing Ops - MVP

    

> **Rama:** `maqueta-inicial` (MVP)

Este proyecto establece una arquitectura de microservicios contenerizada para la ingesta, almacenamiento, exposición y visualización de indicadores económicos chilenos (inicialmente el valor de la UF). El objetivo principal es servir como base para implementar prácticas avanzadas de **DevOps, MLOps e Ingeniería de Datos**.

## 🏗️ Arquitectura del Sistema

El sistema está compuesto por 4 servicios orquestados mediante Docker Compose:

1.  **PostgreSQL (Persistencia):** Base de datos relacional inicializada con scripts SQL (`init.sql`) para definir el esquema.
2.  **ETL (Ingesta):** Script en Python que extrae datos (simulados/web scraping), los transforma y los carga en la base de datos.
3.  **API (Backend):** Servicio desarrollado con **FastAPI** que expone los datos almacenados mediante endpoints RESTful documentados automáticamente.
4.  **Dashboard (Frontend):** Interfaz interactiva desarrollada con **Streamlit** que consume la API para visualizar las tendencias de datos.

## 🛠️ Stack Tecnológico

  * **Lenguaje:** Python 3.11
  * **Contenerización:** Docker & Docker Compose
  * **Base de Datos:** PostgreSQL 16 (Alpine)
  * **Backend:** FastAPI + Uvicorn
  * **Frontend:** Streamlit
  * **Librerías Clave:** Pandas, Psycopg2-binary, Requests.

## 🚀 Pre-requisitos

Asegúrate de tener instalado en tu máquina local:

  * [Docker Engine](https://docs.docker.com/get-docker/)
  * [Docker Compose](https://docs.docker.com/compose/install/)
  * Git

## 🔧 Instalación y Ejecución

Sigue estos pasos para levantar el entorno completo:

### 1\. Clonar el repositorio

```bash
git clone https://github.com/diadasiachilensis/chile-housing-ops.git
cd chile-housing-ops
```

### 2\. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto. Puedes basarte en las siguientes variables (ajusta las credenciales según prefieras):

```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=chile_housing
API_HOST=api
```

### 3\. Levantar los Servicios

Utiliza Docker Compose para construir y levantar los contenedores. Docker se encargará de crear la red interna y los volúmenes.

```bash
docker compose up -d --build
```

*Nota: La primera vez que se ejecuta, PostgreSQL tomará unos segundos en inicializar la base de datos `chile_housing` y crear la tabla `uf_data` mediante el script `init.sql`.*

### 4\. Carga de Datos (ETL)

El servicio ETL está configurado para ejecutarse, cargar los datos y detenerse. Si necesitas forzar una recarga manual de datos, ejecuta:

```bash
docker compose run etl python etl/main.py
```

## 🖥️ Acceso a los Servicios

Una vez que los contenedores estén corriendo (`docker compose ps` para verificar), puedes acceder a:

| Servicio | URL | Descripción |
| :--- | :--- | :--- |
| **Dashboard** | `http://localhost:8501` | Visualización de la tabla de UF y métricas. |
| **API Docs** | `http://localhost:8000/docs` | Swagger UI para probar los endpoints de la API. |
| **API Redoc** | `http://localhost:8000/redoc` | Documentación alternativa de la API. |

## 📂 Estructura del Proyecto

```text
chile-housing-ops/
├── api/                # Microservicio de Backend (FastAPI)
│   ├── Dockerfile
│   └── app.py
├── dashboard/          # Microservicio de Frontend (Streamlit)
│   ├── Dockerfile
│   └── ui.py
├── etl/                # Scripts de Extracción y Carga
│   ├── Dockerfile
│   └── main.py
├── postgres/           # Configuración de BD
│   └── init.sql        # Script de inicialización (DDL)
├── docker-compose.yml  # Orquestación de servicios
├── .env                # Variables de entorno (no versionado)
└── README.md           # Documentación
```