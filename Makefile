all:
	pipenv run flask run

lint:
	pipenv run black . && pipenv run isort . -s migrations
