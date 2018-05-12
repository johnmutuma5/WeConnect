venv:
	virtualenv -p python3.6 venv

install:
	pip install -r requirements.txt

freeze:
	pip freeze | grep -v "pylint" > requirements.txt

tables:
	python tables.py create

drop_all:
	python tables.py drop

run:
	python run.py

test:
	nosetests --exe -v --nocapture --with-coverage --cover-package=app
