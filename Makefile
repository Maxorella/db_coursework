clean:
	docker-compose down

build:
	docker-compose build

stop:
	docker-compose stop
	
run: stop build
	docker-compose up -d
	python ./lab1/app.py

flow:
	docker-compose down -v
	docker-compose up -d --build
	docker exec -it db_coursework-db-1  mysql -u root