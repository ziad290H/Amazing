# Makefile for Amazing Maze Project

PYTHON = python3
ENTRY = main.py
CONFIG = config.txt

all: run

run:
	@$(PYTHON) $(ENTRY) $(CONFIG)

clean:
	@rm -rf __pycache__
	@rm -f output_maze.txt

.PHONY: all run clean