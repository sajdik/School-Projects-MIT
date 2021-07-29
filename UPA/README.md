# UPA2020
VUT FIT UPA project 2020

## Authors:
Ondrej Šajdík
Marek Šalgovič
Samuel Slávka 

## Execution pipepile
 Setup and execution pipeline uses set of make commands defined in Makefile.
 
### Local database setup
 #### Requirements: 
 1. [Docker](https://www.docker.com/)
 2. [docker-compose](https://docs.docker.com/compose/)
 3. Port _27017_ for [mongoDB](https://www.mongodb.com/) and port _5432_ for [postreSQL](https://www.postgresql.org/)
 
 #### Setup:
 
	make init
	make up
 
 The first step creates local database folder to persist data even after shutting down Docker containers.
 The seconds step starts Docker containers using docker-compose and exposes ports _27017_ and _5432_ for **mongoDB** and **postgreSQL** respectively.
 
### Fetch data from datasource
 #### Requirments:
 1. None
 
 #### Execution
 	make run-fetch
 
 Download the golang-image
 Run the _fetch_ script with default env variables. The script fetches data from datasource and saves it to **mongoDB** collection with name **_days_** in database **_upa_**.
 <br>It is possible to provide different env variable configuration to _fetch_ script to change its behaviour in docker-compose file.
 - **MONGO_URI** - mongoDB connection string
 - **SOURCE_URL** - to change URL of datasource
 - **FETCH_YEAR** - to change year of fetched data 

### Transfer from mongoDB to postgreSQL

 #### Requirments:
 1. None

 #### Execution
 	make run-transfer
 	
 Aggregates and exports table days from **mongoDB** to **json** file. Parses this file with **jq** and creates tables in **postgreSQL** to which these elements are inserted.

  ## Queries

 #### Requirments:
 1. None

 #### Execution:
 	

  ###### Query A - Ranking of currencies - which strenghtend/weakened the most: 
  	make run-select-strength from=<from date> to=<to_date> asc=[ASC/DESC]
  ###### Own query - Ranking of currencies - which is most stable/unstable: 
	make run-select-stability from=<from date> to=<to_date> asc=[ASC/DESC]

Date format: DD.MM.YYYY <br>
Strengtend / Stable - DESC (optional) <br>
Weakened / Unstable - ASC (optional) <br>

### Clean up

To clean up the workspace run:

	make down
	make clean
 
 This shuts-down the running database containers and cleans workspace from database data and program binaries. To shut down containers and keep data persistent run only `make down`.
