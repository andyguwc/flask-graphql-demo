build:
	@docker build . --rm -t demo

start:
	@docker-compose up -d

stop:
	@docker-compose down

teardown:
	@docker-compose down -v

status:
	@docker-compose ps

restart: stop start

bootstrap: stop build start

bash: 
	@docker exec -it flask-demo_web_1 bash
	@docker run -it --rm --env-file .env demo bash

shell: 
	@docker exec -it flask-demo_web_1 flask shell

server-logs:
	@docker logs flask-demo_web_1