init:
	mkdir database/generated \
	database/generated/mongodb \
	database/generated/mongodb/data \
	database/generated/mongodb/data/db \
	database/generated/postgresql \
	database/generated/postgresql/data \
	database/generated/shared; \

up:
	docker-compose up --scale  fetch=0

down:
	docker-compose down

clean:
	rm -rf database/generated

run-fetch-default:
	docker-compose run fetch /bin/fetch

run-fetch:
	docker-compose run fetch /bin/fetch -year=$(year)

run-fetch-mongo:
	docker-compose run fetch /bin/fetch -mongo=$(mongo) -year=$(year)

run-transfer:
	docker-compose exec mongo-service bash transfer/transfer1.sh
	docker-compose exec postgresql-service bash transfer/transfer2.sh

run-select-strength:
	docker-compose run select python strength.py $(from) $(to) $(asc)

run-select-stability:
	docker-compose run select python stability.py $(from) $(to) $(asc)