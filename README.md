# 🎬 Online Cinema API

**A modern, high-performance RESTful API for an online cinema platform, built with FastAPI and an asynchronous Python stack.**

![Python Version](https://img.shields.io/badge/python-3.11-blue?style=for-the-badge&logo=python) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
---

## 🚀 About The Project

**Online Cinema API** is a robust backend for a digital platform that allows users to register, browse a movie catalog, manage their profiles, and much more. The project is built on a modern, asynchronous Python stack to ensure high performance and scalability, following clean architecture principles.

### ✨ Key Features

* **Full Authentication System:** Secure user registration with email activation, login, a complete password reset flow, and JWT (access/refresh token) management.
* **Profile Management:** Create, update, and view user profiles, including avatar uploads to S3-compatible storage.
* **Movie Catalog:** Browse a paginated list of movies and retrieve detailed information for any film.
* **Content Management (CRUD):** A full suite of endpoints for managing movies, genres, actors, and other entities, designed for moderator and admin roles.
* **Role-Based Access Control (RBAC):** Foundation for permission handling for Users, Moderators, and Admins.

---

## 🛠️ Tech Stack

| Category | Technology |
| :--- | :--- |
| **Backend** | Python, FastAPI, Pydantic |
| **Database & ORM** | PostgreSQL, SQLAlchemy 2.0 (Async), Alembic |
| **Containerization** | Docker, Docker Compose |
| **Testing** | Pytest, pytest-asyncio, HTTPX, Codecov |
| **Tooling** | Poetry, MinIO (S3), MailHog |

---

## 🏁 Getting Started

### Prerequisites

Ensure you have the following installed on your local machine:
* [Docker](https://www.docker.com/get-started) & Docker Compose
* [Poetry](https://python-poetry.org/docs/#installation)

### **How to Run the Project**

Follow these steps to set up and run the **Movie Theater API** project on your local machine.

---

## **1. Clone the Repository**

Start by cloning the project repository from GitHub:

```bash
git clone  https://github.com/mgoryn/online-cinema
cd online-cinema
```

---

## **2. Create and Activate a Virtual Environment**

It is recommended to use a virtual environment to isolate project dependencies:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

---

## **3. Install Dependencies with Poetry**

This project uses **Poetry** for dependency management. Install dependencies as follows:

```bash
# Install Poetry if not already installed
pip install poetry

# Install project dependencies
poetry install
```

---

## **4. Create a `.env` File**

Create a `.env` file in the project root directory with the following variables. Customize the values as needed:

```env
# PostgreSQL
POSTGRES_DB=movies_db
POSTGRES_DB_PORT=5432
POSTGRES_USER=admin
POSTGRES_PASSWORD=some_password
POSTGRES_HOST=postgres_theater

# pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@gmail.com
PGADMIN_DEFAULT_PASSWORD=admin

# JWT keys
SECRET_KEY_ACCESS=838qKq7dGp34hWij3c8txA5ZD2qm9ybt
SECRET_KEY_REFRESH=cFzRk8kllHMW71wQKLXBqDzl24fkhisw
JWT_SIGNING_ALGORITHM=HS256

# MailHog
MAILHOG_USER=admin
MAILHOG_PASSWORD=some_password

# Email settings for MailHog
EMAIL_HOST=mailhog_theater
EMAIL_PORT=1025
EMAIL_HOST_USER=testuser@mate.com
EMAIL_HOST_PASSWORD=test_password
EMAIL_USE_TLS=False

# MinIO (S3-Compatible Storage)
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=some_password
MINIO_HOST=minio-theater
MINIO_PORT=9000
MINIO_STORAGE=theater-storage
```

---

## **5. Run the Project with Docker Compose**

The project is **Dockerized** for easy setup. To start all the required services (**PostgreSQL, pgAdmin, FastAPI app, MailHog, MinIO, and Alembic migrator**), run:

```bash
docker-compose up --build
```

**Notes**:
- The first run **may take some time** as the database will be populated with initial data.
- Logs for services can be viewed using:

  ```bash
  docker-compose logs -f
  ```

---

## **6. Access the Services**

| Service        | URL |
|---------------|--------------------------|
| **API**       | `http://localhost:8000` |
| **pgAdmin**   | `http://localhost:3333` (Use `.env` credentials) |
| **MailHog UI** | `http://localhost:8025` (SMTP testing) |
| **MinIO Console** | `http://localhost:9001` (S3-compatible storage) |

---

## **7. Verify Setup**

After all services are running, you can test the API by accessing the **OpenAPI documentation**:

```plaintext
http://localhost:8000/docs
```

---

## **8. Running the Development Server without Docker**

If you prefer running the application **without Docker**, follow these steps:

1. **Ensure PostgreSQL is running** on your system with credentials matching `.env`.
2. **Apply migrations manually**:

   ```bash
   poetry run alembic upgrade head
   ```

3. **Start the development server**:

   ```bash
   poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

---

## **9. Running End-to-End (E2E) Tests**

The project includes **E2E tests** that validate the system using a **separate testing environment**. These tests run inside **dedicated containers** using `docker-compose-tests.yml`.

### **Steps to Run E2E Tests**
1. **Start the test environment**:
   ```bash
   docker-compose -f docker-compose-tests.yml up --build
   ```

2. **Run E2E tests manually (inside a container)**:
   ```bash
   docker exec -it backend_theater_test pytest -m e2e --maxfail=5 --disable-warnings -v --tb=short
   ```

3. **Stop the test environment**:
   ```bash
   docker-compose -f docker-compose-tests.yml down -v
   ```

---

## **10. Running Tests Locally**

For **unit and integration tests**, use:

```bash
pytest -m "unit or integration" --disable-warnings -v
```
---

In the Swagger UI, you will find:
* **A complete list of all available endpoints**, grouped by tags (e.g., `accounts`, `movies`, `profiles`).
* **Detailed information for each endpoint**, including the HTTP method, URL, summary, and description.
* **A breakdown of all required parameters** (path, query, body) with their data types and validation rules.
* **Example request bodies** and detailed schemas for all possible responses, including error codes.
* **An interactive "Try it out" button** that allows you to execute API requests directly from your browser.

This is the primary source of truth for understanding how to use the API, what parameters to send, and what each action does.

---

## 🧪 Testing

The project uses a separate configuration for testing, which runs against a temporary in-memory SQLite database to ensure test isolation and speed.

To run the entire test suite and generate a coverage report, execute:
```bash
docker-compose -f docker-compose-tests.yml run --rm tests
```
This command will start `pytest`, run all tests, and display a code coverage report in the console.

---

## 📚 API Documentation

Once the project is running, interactive **Swagger UI** documentation is automatically generated and available at:
* [**http://localhost:8000/docs**](http://localhost:8000/docs)

Alternative **ReDoc** documentation is available here:
* [**http://localhost:8000/redoc**](http://localhost:8000/redoc)

---

## 📂 Project Structure

The project follows a clean and scalable architecture, separating concerns into distinct modules:
```
online-cinema/
├── src/database/migrations/  # Database migrations
├── commands/                 # Startup scripts
├── src/
│   ├── config/               # Configuration and dependencies
│   ├── database/             # Models, sessions, validators
│   ├── exceptions/           # Custom exceptions
│   ├── notifications/        # Email sending logic
│   ├── routes/               # API endpoints (routers)
│   ├── schemas/              # Pydantic schemas
│   ├── security/             # Auth and JWT logic
│   ├── storages/             # File storage clients
│   └── tests/                # Unit and integration tests
├── .env.sample               # Environment file example
├── docker-compose-local.yml  # Docker Compose for development
└── Dockerfile                # Instructions for the app image
```

---

## 🤝 Contributing

Contributions are welcome! Please follow the standard Fork -> Feature Branch -> Pull Request workflow.
