.PHONY: install clobber run test lint
PYTHON=venv/bin/python
PIP=venv/bin/pip
LINT=venv/bin/flake8
TEST=venv/bin/nosetests

all: install

venv:
	virtualenv -p python2.7 venv

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

test: lint
	$(TEST) test/

lint:
	$(LINT) test sbc

clobber:
	rm -rf venv/

run:
	$(PYTHON) -m sbc.main

