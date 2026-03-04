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
	flake8 $(LINT_FILES)
	mypy $(LINT_FILES) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs

# --- OPTIONAL ENHANCEMENTS ---

# Strict linting as recommended by the subject
strict:
	mypy $(LINT_FILES) --strict
	flake8 $(LINT_FILES)

.PHONY: all install run debug clean lint strict