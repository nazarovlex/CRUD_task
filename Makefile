
.PHONY: build
build:
	sudo docker-compose build

.PHONY: start
start:
	sudo docker-compose up

.PHONY: stop
stop:
	sudo docker-compose stop

.PHONY: clean
clean:
	sudo rm -rf .artifacts
	sudo rm -rf .pytest_cache
	sudo docker system prune

.PHONY: test
test:
	sudo docker exec -it crud_task_web_1 pytest api_test.py

.PHONY: restart
restart:
	make build
	make start
