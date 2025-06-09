SHELL := /bin/bash

.PHONY: install run test clean

#Install dependencies of all llms
install:
	@echo "Creating and activating virtual environment..."
	python3 -m venv venv
	@echo "Installing dependencies..."
	source venv/bin/activate && pip3 install -r requirements.txt
	@echo "Installation complete!"

run:
	@echo "Starting the application..."
	source venv/bin/activate && python3 main.py

clean:
	@echo "Removing virtual environment and temporary files..."
	rm -rf venv
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -f {} +