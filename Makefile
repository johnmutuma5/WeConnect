venv:
	virtualenv -p python3 venv

install:
	pip install -r requirements.txt

freeze:
	pip freeze | grep -v "pkg-resources" > requirements.txt
