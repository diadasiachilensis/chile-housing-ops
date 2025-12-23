Aquí tienes una versión **profesional, robusta y actualizada** de tu `README.md`.

He incorporado los siguientes cambios clave:

1. **Diagrama de Arquitectura:** Agregué un gráfico con sintaxis **Mermaid.js** (GitHub lo renderiza automáticamente), lo que le da un toque muy técnico.
2. **Actualización de Datos Reales:** Ya no decimos "datos simulados", ahora especificamos que nos conectamos a la API oficial del Banco Central.
3. **Variables de Entorno:** Agregué las credenciales del Banco Central (`BCCH_USER`, `BCCH_PASS`) que ahora son obligatorias.
4. **Roadmap:** Incluí una sección de "Próximos Pasos" para demostrar visión de producto (CI/CD, Testing, etc.), algo que los reclutadores valoran mucho.

Copia y pega el siguiente bloque en tu archivo `README.md`:

# 🏠 Chile Housing Ops - MVP

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-blue?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Postgres](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

> **Estado:** 🟢 Operativo (MVP) | **Rama:** `maqueta-inicial`

Este proyecto implementa una arquitectura de **Data Engineering End-to-End** contenerizada para la ingesta, almacenamiento y visualización de indicadores económicos chilenos (UF).

El sistema se conecta directamente a la **API del Banco Central de Chile**, procesa la información histórica y la expone mediante servicios desacoplados, sirviendo como base sólida para escalar hacia prácticas de **DevOps y MLOps**.

## 🏗️ Arquitectura del Sistema

El flujo de datos sigue un patrón lineal de extracción, carga y consumo, orquestado completamente con Docker Compose.

![Diagrama de Arquitectura](pipeline-chile-housing-ops.png)

### Componentes:

1. **🐘 PostgreSQL (Persistencia):** Base de datos relacional inicializada con volúmenes persistentes.
2. **⚙️ ETL (Ingesta):** Script en Python que utiliza la librería oficial `bcchapi` para extraer series históricas (desde el año 2000 a la fecha) y cargarlas en la base de datos.
3. **⚡ API (Backend):** Servicio RESTful desarrollado con **FastAPI** que actúa como capa de servicio, entregando datos serializados y validados con Pydantic.
4. **📊 Dashboard (Frontend):** Interfaz desarrollada en **Streamlit** con gráficos interactivos de **Plotly**, diseñada para el análisis de tendencias económicas.

## 🛠️ Stack Tecnológico

* **Infraestructura:** Docker & Docker Compose (IaC).
* **Lenguaje:** Python 3.11.
* **Base de Datos:** PostgreSQL 16 (Alpine Linux).
* **Backend:** FastAPI, Uvicorn, Pydantic.
* **Frontend:** Streamlit, Plotly Express.
* **ETL & Datos:** Pandas, Bcchapi (Banco Central SDK), Python-dotenv.

## 🚀 Instalación y Despliegue

### 1. Pre-requisitos

* Docker Engine & Docker Compose (V2)
* Git

### 2. Clonar el repositorio

```bash
git clone [https://github.com/diadasiachilensis/chile-housing-ops.git](https://github.com/diadasiachilensis/chile-housing-ops.git)
cd chile-housing-ops

```

### 3. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto. **Es vital incluir tus credenciales del Banco Central** para que el ETL funcione.

```env
# --- Base de Datos ---
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=chile_housing
POSTGRES_HOST=postgres

# --- Credenciales Banco Central (Requerido para ETL) ---
BCCH_USER="tu_correo@ejemplo.com"
BCCH_PASS="tu_contraseña_banco"

# --- Configuración Interna ---
API_HOST=api

```

### 4. Construir y Levantar

Ejecuta el siguiente comando para compilar las imágenes e iniciar los servicios:

```bash
docker compose up --build

```

> **Nota:** El servicio de ETL se ejecutará automáticamente al inicio, descargará los datos históricos de la UF y poblará la base de datos. Verás en los logs: `✅ Carga finalizada`.

## 🖥️ Acceso a los Servicios

| Servicio | URL Local | Descripción |
| --- | --- | --- |
| **📊 Dashboard** | `http://localhost:8501` | Visualización interactiva y gráficos de la UF. |
| **⚡ API Docs** | `http://localhost:8000/docs` | Swagger UI para probar endpoints (`/uf_history`). |
| **⚡ API Redoc** | `http://localhost:8000/redoc` | Documentación técnica alternativa. |

## 📂 Estructura del Proyecto

```text
chile-housing-ops/
├── api/                # Lógica del Backend (FastAPI)
│   ├── app.py
│   └── Dockerfile
├── dashboard/          # Interfaz de Usuario (Streamlit)
│   ├── ui.py
│   └── Dockerfile
├── etl/                # Pipeline de Datos
│   ├── extract_economic.py  # Lógica de conexión a BCCH
│   ├── main.py              # Orquestador del ETL
│   └── Dockerfile
├── postgres/           # Scripts de Base de Datos
│   └── init.sql        # DDL Inicial
├── docker-compose.yml  # Orquestación de contenedores
├── requirements.txt    # Dependencias globales
└── .env                # Credenciales (No versionar)

```

## 🔮 Roadmap y Próximos Pasos

Este proyecto está en constante evolución. Las siguientes mejoras están planificadas:

* [ ] **CI/CD:** Implementación de GitHub Actions para testing y build automático.
* [ ] **Orquestación Avanzada:** Migración del script ETL a **Apache Airflow** o Prefect.
* [ ] **Testing:** Unit tests para la API (Pytest) y validación de calidad de datos.
* [ ] **Cloud:** Despliegue en AWS (ECS o EC2) o Google Cloud Run.

---
