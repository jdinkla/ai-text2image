
init:
	./init.sh

run:
	python app.py

freeze:
	pip freeze -l > requirements.txt