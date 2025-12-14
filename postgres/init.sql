-- Aseguramos que nos conectamos a la base de datos creada por las variables de entorno
\connect chile_housing; 
-- Crear la tabla uf_data en la base de datos 'chile_housing'
CREATE TABLE IF NOT EXISTS uf_data (
    date DATE PRIMARY KEY,
    value NUMERIC(10, 2) NOT NULL
);