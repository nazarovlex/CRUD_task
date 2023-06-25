
.PHONY: build
build:
	docker-compose build

.PHONY: start
start:
	docker-compose up

.PHONY: clean
clean:
	rm -rf pg_data

.PHONY: test
test:
	docker exec -it crud_task_web_1 python -m pytest

.PHONY: restart
restart:
	make build
	make start
