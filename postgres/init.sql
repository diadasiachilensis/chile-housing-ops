-- TABLA DE PROPIEDADES (HECHOS)
CREATE TABLE IF NOT EXISTS properties (
    id SERIAL PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    comuna VARCHAR(100),
    price_clp NUMERIC,
    price_uf NUMERIC,
    surface_m2 NUMERIC,
    bedrooms INTEGER,
    bathrooms INTEGER,
    property_type VARCHAR(50),
    latitude NUMERIC,
    longitude NUMERIC,
    ingestion_date DATE
);

-- TABLA DE UNIDADES DE FOMENTO (UF)
CREATE TABLE IF NOT EXISTS uf_data (
    date DATE PRIMARY KEY,
    value NUMERIC NOT NULL
);

-- Crear un índice en la comuna para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_comuna ON properties (comuna);
