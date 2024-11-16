FROM python:3.10-slim

WORKDIR /app
COPY . /app

# Install Poetry
RUN pip install poetry

# Create a virtual environment
RUN python -m venv /venv

# Activate the virtual environment and install dependencies
RUN . /venv/bin/activate && poetry install --no-root

# Command to run the application
CMD ["/venv/bin/python", "src/__main__.py"]