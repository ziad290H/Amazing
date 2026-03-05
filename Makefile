# Variables
PYTHON = python3
PIP = pip
MAIN_SCRIPT = a_maze_ing.py
CACHE_DIRS = __pycache__ .mypy_cache .pytest_cache
LINT_FILES = .
CONFIG = config.txt

all: run


install:
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy pygame

run:
	$(PYTHON) $(MAIN_SCRIPT) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN_SCRIPT) $(CONFIG)

clean:
	rm -rf $(CACHE_DIRS)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

lint:
	$(PYTHON) -m flake8
	$(PYTHON) -m mypy $(LINT_FILES) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs


# Strict linting as recommended by the subject
strict:
	$(PYTHON) -m mypy $(LINT_FILES) --strict
	$(PYTHON) -m flake8 

.PHONY: all install run debug clean lint strict