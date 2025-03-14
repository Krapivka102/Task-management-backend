DC = docker-compose
EXEC = docker exec -it
ENV = --env-file .env
DC_FILE = docker-compose.yaml
STORAGES_CONTAINER = task_management_db_pg
APP_CONTAINER = task_management_backend

.PHONY: app-start
app-start:
	${DC} -f ${DC_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${DC_FILE} ${ENV} down

.PHONY: app-down-total
app-down-total:
	${DC} -f ${DC_FILE} ${ENV} down -v
