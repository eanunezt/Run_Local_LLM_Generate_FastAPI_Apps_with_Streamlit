![ Banner](/doc/banner.png)

Streamlit DDL to JSON & FastAPI Code Generator

==============================================

This project is a **Streamlit-based application** that allows users to input SQL DDL statements, convert them into a structured JSON format using a **local LLM (Ollama)**, and generate a FastAPI project based on the JSON schema. The generated project can be downloaded as a ZIP file.

Features

--------

-   **SQL DDL to JSON Conversion:**

    Uses an **Agentic RAG** approach to transform SQL table definitions into a structured JSON format.

-   **Local LLM Integration:**

    Runs a **local Large Language Model (LLM) using Ollama** to process SQL and generate JSON.

-   **FastAPI Project Generation:**

    Uses the generated JSON schema to create a **FastAPI-based application**.

-   **One-Click Download:**

    The final project is packaged into a ZIP file for easy download.

Architecture

------------

The application consists of two main services managed via **Docker Compose**:

1.  **Streamlit App (`streamlitsrv`)**

    -   Runs the web interface

    -   Handles user input for SQL DDL statements

    -   Calls the LLM model via the Agentic RAG pipeline

    -   Generates the FastAPI project

    -   Provides a download button for the ZIP file

2.  **Ollama LLM Server (`ollamasrv`)**

    -   Serves the LLM model locally

    -   Loads and processes SQL-to-JSON conversion requests

### Tech Stack

-   **Frontend:** Streamlit

-   **Backend:** Python (FastAPI)

-   **LLM Framework:** Ollama + LangChain

-   **Containerization:** Docker & Docker Compose

How It Works

------------

1.  **User Inputs SQL DDL:**

    -   The user enters a SQL `CREATE TABLE` statement in the Streamlit app.

2.  **Agentic RAG + LLM Processes the Input:**

    -   The LLM (running on Ollama) converts the SQL into structured JSON.

3.  **FastAPI Project is Generated:**

    -   The app generates a FastAPI application using the JSON model.

4.  **Download the FastAPI Project:**

    -   The project is zipped and available for download.

Setup Instructions

------------------

### 1\. Clone the Repository

`git clone <your-repo-url>

cd <your-project-folder>`

### 2\. Start the Services

`docker-compose build`

`docker-compose up -d`

### 3\. Access the Streamlit App

Open a web browser and go to:

`http://localhost:8501`

### 4\. Enter SQL DDL & Generate Code

-   Paste a SQL `CREATE TABLE` statement.

-   Click **"Generate Project"** to convert SQL to JSON and create a FastAPI project.

-   Download the generated ZIP file.

Example Usage

-------------

**Input (SQL DDL):**

sql

`CREATE TABLE users (

    id SERIAL PRIMARY KEY,

    name VARCHAR(100),

    email VARCHAR(100) UNIQUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);`

**Output (Generated JSON):**

json

`{

    "models": [

        {

            "name": "User",

            "fields": [

                {"name": "id", "type": "integer", "primary_key": true},

                {"name": "name", "type": "string"},

                {"name": "email", "type": "string", "unique": true},

                {"name": "created_at", "type": "datetime", "default": "CURRENT_TIMESTAMP"}

            ]

        }

    ]

}`

**Generated FastAPI Project Structure:**

`
fastapi-app/

	───pyproject.toml
	───README.md
	───src/
		database.py
		main.py│   │
	───user/
		controller.py
		model.py
		repository.py
		service.py
	───tests/
`

Environment Variables

---------------------

The app uses the following environment variables (configured in `docker-compose.yml`):

| Variable | Description | Default Value |

| --- | --- | --- |

| `MODEL_LLM` | The LLM model used by Ollama | `mistral` |

| `BASE_URL_SRV_LLM` | Base URL for Ollama API | `http://localhost:11434` |

Future Improvements

-------------------

-   Add more customization options for project generation.

-   Support additional frameworks beyond FastAPI.

-   Improve LLM accuracy and handling of complex SQL statements.

License

-------

This project is open-source and available under the **MIT License**.