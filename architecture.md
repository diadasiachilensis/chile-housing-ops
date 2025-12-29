
# Arquitectura del Sistema: Chile-Housing-ops

**Autor:** *Diadasia chilensis*

**Fecha:** Diciembre 2025

**Versión:** 1.0.0 (Fase de Diseño)

Este documento define la estructura de alto nivel del sistema siguiendo el modelo C4 y justifica las decisiones técnicas basándose en principios de Ingeniería de Software Moderna e Ingeniería de Datos.

---

## 1. Nivel 1: Diagrama de Contexto del Sistema

**Objetivo:** Visualizar cómo interactúa el sistema con el mundo exterior (Usuarios y Sistemas de Terceros).

```mermaid
C4Context
    title Diagrama de Contexto - Chile Housing Ops

    Person(admin, "Operador Inmobiliario", "Usuario que gestiona activos, visualiza tasaciones y configura alertas.")

    Enterprise_Boundary(b0, "Dominio del Proyecto") {
        System(housing_system, "Chile-Housing-ops System", "Plataforma central de orquestación de datos inmobiliarios y valuación.")
    }

    System_Ext(fuentes_datos, "Fuentes Inmobiliarias", "Portalinmobiliario, Yapo, TocToc (Alta Volatilidad/HTML).")
    System_Ext(servicios_fin, "Servicios Financieros", "API CMF/Banco Central (Datos Estructurados/JSON).")
    System_Ext(comms, "Sistema de Notificaciones", "Servidor SMTP / Slack Webhooks.")

    Rel(admin, housing_system, "Consulta dashboard y define estrategias", "HTTPS")
    Rel(housing_system, fuentes_datos, "Ejecuta Ingesta (Scraping)", "HTTPS")
    Rel(housing_system, servicios_fin, "Sincroniza UF/Dólar", "API REST")
    Rel(housing_system, comms, "Envía Alertas", "SMTP/Webhook")

```

---

## 2. Nivel 2: Diagrama de Contenedores

**Objetivo:** Mostrar las unidades desplegables, la elección tecnológica y los patrones de comunicación.

**Decisión Crítica:** Se implementa una Arquitectura Basada en Eventos para desacoplar la interfaz de usuario (Baja Latencia) del proceso de ingesta de datos (Alta Latencia/Batch).

```mermaid
C4Container
    title Diagrama de Contenedores - Arquitectura Reactiva & Data Pipeline

    Person(admin, "Operador Inmobiliario", "Usuario final")

    Container_Boundary(c1, "Chile-Housing-ops Quanta") {
        
        Container(spa, "Dashboard SPA", "React + TypeScript", "Interfaz de usuario (MVVM). Visualización de datos y gestión.")
        
        Container(api, "Orchestration API", "Python (FastAPI)", "API Gateway & Business Logic. Coordina peticiones síncronas.")
        
        Container(msg_broker, "Event Bus", "Redis", "Cola de mensajes para comunicación asíncrona y gestión de tareas.")
        
        Container(ingest_worker, "Ingestion Worker", "Python (Celery/Airflow)", "Ejecuta pipelines de scraping. Implementa patrones Factory & Strategy.")

        ContainerDb(raw_store, "Data Lake (Bronze Layer)", "Object Storage (S3/MinIO)", "Almacenamiento de HTML/JSON crudo e inmutable.")
        
        ContainerDb(op_db, "Operational DB (Silver Layer)", "PostgreSQL", "Datos relacionales, limpios y estructurados.")
    }

    System_Ext(ext_web, "Webs Externas", "Fuentes de Datos")

    %% Flujos
    Rel(admin, spa, "Interactúa", "HTTPS")
    Rel(spa, api, "API Calls", "JSON/HTTPS")

    Rel(api, op_db, "Lectura (Query)", "SQL")
    Rel(api, msg_broker, "Publica Comando 'Ingestar'", "Redis Pub/Sub")

    Rel(msg_broker, ingest_worker, "Consume Tarea", "Async Protocol")
    Rel(ingest_worker, ext_web, "Scraping", "HTTPS")
    
    Rel(ingest_worker, raw_store, "1. Guarda Raw Data", "Blob Write")
    Rel(ingest_worker, op_db, "2. Guarda Datos Procesados", "SQL Upsert")

```

---

## 3. Justificación Teórica y Alineación Bibliográfica

La arquitectura de 'Chile-Housing-ops' no es arbitraria; responde a *trade-offs* de ingeniería específicos analizados en la literatura especializada. A continuación, se detalla la matriz de correspondencia entre los conceptos teóricos y la implementación en los diagramas.

| Libro | Concepto Clave Aplicado | Aplicación en el Diagrama |
| --- | --- | --- |
| **Software Architecture: The Hard Parts** (Ford & Richards) | **Architectural Quanta & Static/Dynamic Coupling.** Identificamos que el "Scraping" y la "UI" tienen características operativas opuestas (alta vs. baja volatilidad), forzando una separación física. | En la decisión de separar el contenedor `API` del `Ingestion Worker` usando una cola asíncrona, creando dos *quanta* desplegables independientemente. |
| **Fundamentals of Software Architecture** (Richards & Ford) | **Event-Driven Architecture (EDA).** Priorizamos la elasticidad y la capacidad de reacción ante cambios de estado sobre una arquitectura monolítica en capas tradicional. | En la implementación del `Msg Broker (Redis)` como mediador para la comunicación asíncrona entre servicios. |
| **Head First Design Patterns** (Freeman et al.) | **Encapsulate What Varies.** Principio base para aislar la lógica de parsing que cambia con cada web (yapo, portalinmobiliario). | En la definición interna del `Ingestion Worker`, utilizando explícitamente **Strategy** (para algoritmos de limpieza) y **Factory** (para instanciar parsers). |
| **Data Engineering Design Patterns** (Späti / General) | **Decoupling Compute from Storage & Medallion Architecture.** La idea de que el procesamiento no debe estar atado a la base de datos final y debe existir trazabilidad. | En la creación del `Raw Store (Bronze Layer)` para preservar la data cruda (HTML) antes de su transformación a la `Operational DB (Silver Layer)`. |
| **Architecting Data and ML Platforms** (Desai et al.) | **Data Lineage & Replayability.** La capacidad de "reproducir" la historia de los datos si el código de parsing cambia o se corrige un bug. | En la arquitectura de flujo dual: los datos siempre se persisten primero en crudo, permitiendo reprocesamientos (backfill) futuros sin volver a scrapear la fuente. |

---

## 4. Bibliografía (APA 7.ª Edición)

* Desai, T., & Shah, M. (2023). *Architecting data and machine learning platforms: Enable analytics and AI-driven innovation*. O'Reilly Media.
* Ford, N., & Richards, M. (2021). *Software architecture: The hard parts: Modern trade-off analysis for distributed architectures*. O'Reilly Media.
* Freeman, E., Robson, E., Bates, B., & Sierra, K. (2004). *Head first design patterns*. O'Reilly Media.
* Reis, J., & Housley, M. (2022). *Fundamentals of data engineering: Plan and build robust data systems*. O'Reilly Media. [Referencia académica para patrones de ingeniería de datos].
* Richards, M., & Ford, N. (2020). *Fundamentals of software architecture: An engineering approach*. O'Reilly Media.
* Späti, S. (2023). *Data engineering design patterns*. O'Reilly Media / Self-published GitBook.
