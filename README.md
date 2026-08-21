# Library Management System

A Python-based Library Management System built as a learning project to practice the complete backend development workflow, from business logic and database integration to REST APIs, authentication, testing, frontend integration, and version control.

## Overview

The system manages:

* Books
* Library members
* Book loans
* User authentication
* Google OAuth login

The project started with a domain/business-logic layer and was later extended with PostgreSQL, SQLAlchemy, Alembic migrations, a FastAPI REST API, authentication, and a simple web frontend.

This version represents the first completed learning version of the project.

---

## Features

### Books

Authenticated users can:

* View all books
* View a specific book
* Add a book
* Update a book
* Delete a book
* Borrow a book
* Return a book

A borrowed book cannot be deleted.

### Members

Authenticated users can:

* View all members
* View a specific member
* Add a member
* Update a member
* Delete a member

A member with active loans cannot be deleted.

### Loans

The system supports:

* Creating a loan
* Viewing active loans
* Returning a borrowed book

A book cannot be borrowed if it is already unavailable.

### Authentication

The API supports two authentication methods:

1. Email and password
2. Google OAuth

Passwords are securely hashed using Argon2 through `pwdlib`.

Authenticated API requests use JWT access tokens.

---

## Technologies

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* SQLAlchemy
* PostgreSQL
* Alembic

### Authentication & Security

* JWT
* PyJWT
* Argon2
* pwdlib
* Authlib
* Google OAuth 2.0 / OpenID Connect
* SessionMiddleware

### Frontend

* HTML
* CSS
* JavaScript
* Fetch API

### Testing

* pytest

### Version Control

* Git
* GitHub

### Optional

* Docker
* Docker Compose

Docker was explored during development but is not required to run the current version of the project.

---

## Project Architecture

The project follows a layered structure that separates business logic from database operations and API handling.

```text
Client / Frontend
       │
       ▼
    FastAPI
       │
       ▼
  Business Logic
    (Library)
       │
       ▼
 Repositories
       │
       ▼
 SQLAlchemy Models
       │
       ▼
 PostgreSQL
```

### Main layers

**API Layer**

`api.py`

Provides the REST API endpoints and handles authentication, HTTP requests, and responses.

**Business Logic Layer**

`library.py`

Contains the main library rules, such as:

* Preventing duplicate books and members
* Preventing borrowing of unavailable books
* Preventing deletion of borrowed books
* Preventing deletion of members with active loans
* Handling book returns

**Domain Models**

```text
book.py
member.py
loan.py
```

Represent the core business entities.

**Repository Layer**

```text
repositories/
```

Handles communication between the business layer and the database.

Repositories include:

* `BookRepository`
* `MemberRepository`
* `LoanRepository`
* `UserRepository`

**Database Layer**

```text
database.py
models.py
```

Uses SQLAlchemy to connect the application to PostgreSQL and define database models.

**Migration Layer**

```text
migrations/
```

Contains Alembic migration files used to create and update the database schema.

---

## Project Structure

```text
Library/
│
├── api.py
├── main.py
├── library.py
├── book.py
├── member.py
├── loan.py
│
├── database.py
├── models.py
├── schemas.py
├── security.py
├── google_oauth.py
│
├── repositories/
│   ├── __init__.py
│   ├── book_repository.py
│   ├── member_repository.py
│   ├── loan_repository.py
│   └── user_repository.py
│
├── migrations/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── style.css
│
├── tests.py/
│   ├── test_book.py
│   ├── test_library.py
│   ├── test_loan.py
│   ├── test_member.py
│   └── test_repositories.py
│
├── requirements.txt
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
└── .gitignore
```

---

## Requirements

Before running the project, make sure the following are installed:

* Python 3.14 or compatible Python version
* PostgreSQL
* Git

The required Python dependencies are listed in:

```text
requirements.txt
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Husseinabc/My_Library.git
cd My_Library
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

The `.env` file must not be committed to GitHub because it contains secrets and database credentials.

The application requires values similar to:

```text
DATABASE_URL=postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/DATABASE_NAME

SECRET_KEY=YOUR_SECRET_KEY

GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET
```

Use your own PostgreSQL credentials and Google OAuth credentials.

Never publish real secrets in the repository.

---

## Database Setup

Make sure PostgreSQL is running.

Create the PostgreSQL database configured in `DATABASE_URL`.

Then apply the Alembic migrations:

```bash
alembic upgrade head
```

This creates the database schema defined by the project's migration history.

The current schema includes tables for:

* `books`
* `members`
* `loans`
* `users`

---

## Running the Backend

From the project root, run:

```bash
python -m uvicorn api:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

The root endpoint can be checked at:

```text
http://127.0.0.1:8000/
```

---

## Frontend

The frontend is included in the project and is served by FastAPI.

Open:

```text
http://127.0.0.1:8000/frontend/index.html
```

The frontend provides:

* Email/password login
* Google login
* Book management
* Member management
* Loan management
* Book return
* Logout

The frontend communicates with the FastAPI backend using HTTP requests and JWT authentication.

---

## API Documentation

FastAPI automatically provides interactive API documentation.

After starting the server, open:

```text
http://127.0.0.1:8000/docs
```

This provides Swagger UI, where the available API endpoints can be explored and tested.

---

## API Endpoints

### Books

| Method | Endpoint           | Description         |
| ------ | ------------------ | ------------------- |
| GET    | `/books`           | Get all books       |
| GET    | `/books/{book_id}` | Get a specific book |
| POST   | `/books`           | Add a book          |
| PATCH  | `/books/{book_id}` | Update a book       |
| DELETE | `/books/{book_id}` | Delete a book       |

### Members

| Method | Endpoint               | Description           |
| ------ | ---------------------- | --------------------- |
| GET    | `/members`             | Get all members       |
| GET    | `/members/{member_id}` | Get a specific member |
| POST   | `/members`             | Add a member          |
| PATCH  | `/members/{member_id}` | Update a member       |
| DELETE | `/members/{member_id}` | Delete a member       |

### Loans

| Method | Endpoint                  | Description      |
| ------ | ------------------------- | ---------------- |
| GET    | `/loans`                  | Get active loans |
| POST   | `/loans`                  | Borrow a book    |
| POST   | `/loans/{book_id}/return` | Return a book    |

### Authentication

| Method | Endpoint                | Description                      |
| ------ | ----------------------- | -------------------------------- |
| POST   | `/auth/register`        | Register with email and password |
| POST   | `/auth/login`           | Login with email and password    |
| GET    | `/auth/google`          | Start Google OAuth login         |
| GET    | `/auth/google/callback` | Google OAuth callback            |

---

## Testing

The project includes unit tests for the business logic and integration-style tests for the repository layer.

Run the tests with:

```bash
python -m pytest
```

The test suite covers areas such as:

* Book creation
* Book search
* Book update
* Book deletion
* Duplicate book prevention
* Member management
* Loan creation
* Loan validation
* Book return
* Repository operations

---

## Database Migrations

Alembic is used to manage database schema changes.

To apply existing migrations:

```bash
alembic upgrade head
```

To check the current migration:

```bash
alembic current
```

To view migration history:

```bash
alembic history
```

Future schema changes should be handled through new Alembic migration files rather than manually modifying the production database structure.

---

## Docker

Docker and Docker Compose files are included as an optional part of the project.

The Docker setup contains:

* A PostgreSQL container
* A FastAPI container

It can be started with:

```bash
docker compose up --build
```

However, Docker is **not required for the current development setup**.

The primary development setup uses a local PostgreSQL installation and the Python environment described by `requirements.txt`.

The Docker configuration uses its own PostgreSQL database configuration and should therefore be treated as a separate development environment unless the database configuration is intentionally synchronized.

---

## Git and GitHub

Git is used to track the history of the project.

The project is hosted on GitHub:

```text
https://github.com/Husseinabc/My_Library
```

The main development branch in the current repository is:

```text
master
```

The repository contains commits representing the development history of the project.

---

## Current Project Status

This version of the project is a completed learning version of a Library Management System.

It demonstrates the implementation of:

* Object-oriented business logic
* Automated testing
* PostgreSQL
* SQLAlchemy ORM
* Alembic migrations
* Repository pattern
* FastAPI REST API
* Pydantic schemas
* JWT authentication
* Password hashing with Argon2
* Google OAuth
* HTML/CSS/JavaScript frontend
* Git and GitHub
* Python dependency management

The current frontend is intentionally simple and represents the first version of the user interface.

Future versions may improve the user experience, architecture, features, automation, and AI capabilities.

---

## Future Ideas

Possible future development directions include transforming the project from a general library management system into a personal smart library.

Potential features include:

* Personal book collection management
* Reading progress tracking
* Book notes and summaries
* Book categorization
* Reading statistics
* Personal book lending history
* AI-assisted book classification
* AI-generated summaries
* Telegram or WhatsApp integration
* AI agents for updating reading progress
* Automation workflows
* RAG-based search over personal book notes

These features are not part of the current version.

---

## License

This project is currently a personal learning project.
