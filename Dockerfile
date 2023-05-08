# Use Python 3.9 slim version as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for some Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the poetry.lock and pyproject.toml files to the container
COPY pyproject.toml poetry.lock /app/

# Install Poetry and project dependencies
RUN pip3 install poetry && \
    poetry config virtualenvs.create false && \
    poetry shell && \
    poetry install --no-dev

# Copy the rest of the application files to the container
COPY . /app

# Expose the port on which the Streamlit app will listen
EXPOSE 8501

# Set the command to run when the container starts
CMD ["streamlit", "run", "chitchat/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
