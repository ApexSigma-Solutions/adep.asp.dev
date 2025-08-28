# Project Overview

This project is a FastAPI microservice that provides a web search tool and a multi-tenant To-Do list tool for the Society of Agents. It uses a SQLite database for data storage and requires a Serper API key for the search functionality.

**Key Technologies:**

*   **Backend:** FastAPI
*   **Database:** SQLite
*   **Data Validation:** Pydantic
*   **Database ORM:** SQLAlchemy

**Architecture:**

The application is structured into the following modules:

*   `main.py`: The main FastAPI application file, containing the API endpoints and dependency injection setup.
*   `database.py`: Configures the SQLAlchemy engine and session management.
*   `models.py`: Defines the SQLAlchemy database models for the To-Do list feature.
*   `schemas.py`: Defines the Pydantic schemas for data validation and serialization.

# Building and Running

**1. Install Dependencies:**

```bash
pip install -r requirements.txt
```

**2. Set up Environment Variables:**

Create a `.env` file in the project root and add your Serper API key:

```
SERPER_API_KEY="your_api_key_here"
```

**3. Run the Server:**

```bash
uvicorn main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.

# Development Conventions

*   **Coding Style:** The code follows the PEP 8 style guide.
*   **Testing:** The `README.md` file provides `curl` commands for testing the endpoints. It is recommended to create a more robust testing suite using a framework like `pytest`.
*   **Database Migrations:** The project does not currently use a database migration tool like Alembic. For future development, it is recommended to set up Alembic to manage database schema changes.
