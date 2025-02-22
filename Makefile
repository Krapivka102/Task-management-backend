DC = docker-compose
EXEC = docker exec -it
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
STORAGES_FILE = docker_compose/storages.yaml
STORAGES_CONTAINER = task_management_db_pg
APP_CONTAINER = task_management_backend
LOGS = docker logs

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: all
all:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} ${ENV} down

.PHONY: app-down-total
app-down-total:
	${DC} -f ${APP_FILE} ${ENV} down -v

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} ${ENV} down

.PHONY: storages-down-total
storages-down-total:
	${DC} -f ${STORAGES_FILE} ${ENV} down -v

.PHONY: all-down
all-down:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} ${ENV} down

.PHONY: all-down-total
all-down-total:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} ${ENV} down -v

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f
