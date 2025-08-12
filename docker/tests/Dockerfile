# Start from the same base Python image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    postgresql-client \
    dos2unix \
    && apt-get clean

# Install Poetry
RUN pip install --upgrade pip && pip install poetry

# Set the working directory
WORKDIR /app

# Copy dependency files
COPY poetry.lock pyproject.toml ./

# Configure Poetry and install ALL dependencies, including dev dependencies like pytest
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Copy the source code and other project files
COPY ./src ./src
COPY ./commands ./commands

# Grant execute permissions to scripts
RUN dos2unix /app/commands/*.sh && \
    chmod +x /app/commands/*.sh

# Expose the port (though not strictly necessary for the test runner)
EXPOSE 8000
