
.PHONY: build
build:
	docker-compose build

.PHONY: start
start:
	docker-compose up

.PHONY: stop
stop:
	docker-compose stop

.PHONY: clean
clean:
	rm -rf pg_data
	docker system prune

.PHONY: test
test:
	docker exec -it crud_task_web_1 pytest api_test.py

.PHONY: restart
restart:
	make build
	make start
