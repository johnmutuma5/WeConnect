venv:
	virtualenv -p python3 venv

install:
	pip install -r requirements.txt

freeze:
	pip freeze | grep -v "pkg-resources" > requirements.txt

tables:
	python tables.py create

drop_tables:
	python tables.py drop

run:
	python run.py

test:
	nosetests --exe -v --with-coverage --cover-package=app
