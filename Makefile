all:
	pipenv run flask run

lint:
	black . && isort . -s migrations
