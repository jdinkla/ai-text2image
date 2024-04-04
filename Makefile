ENV_DIR="venv"
PYTHON=python3.11

init:
	mkdir -p $(ENV_DIR)
	$(PYTHON) -m venv $(ENV_DIR)
	source $(ENV_DIR)/bin/activate ; pip install -r requirements.txt

clean:
	rm -rf $(ENV_DIR) 

run:
	source $(ENV_DIR)/bin/activate ; $(PYTHON) app.py

freeze:
	pip freeze -l > requirements.txt
