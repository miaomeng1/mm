PYTHON ?= python3

.PHONY: run test compile

run:
	$(PYTHON) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"

compile:
	$(PYTHON) -m compileall app tests

