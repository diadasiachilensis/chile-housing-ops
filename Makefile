# Variables
COMPOSE=docker compose

# Comandos
.PHONY: up down build logs clean

# Levantar todo el entorno
up:
	$(COMPOSE) up -d

# Construir y levantar (para cuando cambias código)
build:
	$(COMPOSE) up -d --build

# Bajar los servicios
down:
	$(COMPOSE) down

# Ver logs en tiempo real
logs:
	$(COMPOSE) logs -f

# Limpieza total (Borra volúmenes y contenedores) - ¡CUIDADO!
clean:
	$(COMPOSE) down -v
	docker system prune -f