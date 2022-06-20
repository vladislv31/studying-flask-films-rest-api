build:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
	sudo docker-compose build
	rm ./requirements.txt
rebuild:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
	sudo docker-compose up -d --build
	rm ./requirements.txt
start:
	sudo docker-compose up -d
stop:
	sudo docker-compose stop
remove:
	sudo docker-compose down
init_db:
	sudo docker exec nix_films_api flask db migrate
	sudo docker exec nix_films_api flask db upgrade
	sudo docker exec nix_films_api flask db-init
seed_db:
	sudo docker exec nix_films_api flask db-seed
migrate_db:
	sudo docker exec nix_films_api flask db migrate
upgrade_db:
	sudo docker exec nix_films_api flask db upgrade
logs:
	sudo docker exec nix_films_api less app/logs/app.log
test_app:
	sudo docker exec nix_films_api python -m pytest -s