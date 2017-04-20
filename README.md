# Flask API

Implementation of simple API to manipulate with songs.
API was implemented with Flask and MongoDB is used as a DB storage. Initial data lives in separate folder and is used to populate DB.
To set up API only Docker is needed and docker-compose takes care of creating images with required dependencies, populating data and building links between containers.

# Commands to work with the service

To create new images

	docker-compose build

To run containers and populate DB with initial data

	docker-compose up

To stop containers

	docker-compose stop

To run container without populating data

	docker-compose run SERVICE_NAME

To stop and remove containers

	docker-compose down

# Testing

Testing was implemented on top of Flask+unittesting. To run tests it is necessary to login to the container and execute

	python test/tests.py

# Future steps
To simplify future work and to follow standards it is necessary to start using OpenAPI and, for example, zalando/connexion.
In that case a lot of validation will be done via provided libraries.
Also py.test can be used for extended testing. In addition it would be wiser to generate new docker container with separate DB for testing.
