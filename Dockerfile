# Use the specified Python version
FROM python:3.11

# Set environment variables for Python
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

# Configure Poetry and install dependencies from the lock file
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root --only main

# Copy the source code and other project files
COPY ./src ./src
COPY ./alembic.ini ./alembic.ini
COPY ./commands ./commands

# Grant execute permissions to scripts
RUN dos2unix /app/commands/*.sh && \
    chmod +x /app/commands/*.sh

# Expose the port
EXPOSE 8000

# By default, run the web server (this can be overridden in docker-compose)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
