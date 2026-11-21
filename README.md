# AI Student Career & Placement Assistant

An AI-powered student career and placement assistant that combines
machine-learning placement prediction, resume analysis, skill-gap
identification, retrieval-augmented generation (RAG), and an AI agent
connected to tools through the Model Context Protocol (MCP).

## Overview

The application is designed to help students with career and
placement-related tasks through a Streamlit interface.

The project brings together four main capabilities:

-   **Placement prediction:** Uses a machine-learning model to predict a
    student's placement outcome.
-   **Resume analysis:** Analyzes an uploaded PDF resume and its skills.
-   **Skill-gap analysis:** Matches a student's skills against the
    skills needed for a target role and identifies gaps.
-   **Career question answering:** Uses RAG with Chroma and a Groq LLM
    to answer questions using a knowledge base.
-   **AI agent:** Selects and invokes available tools, with MCP
    providing a standard way to expose and use those tools.

## Architecture

### High-level application flow

``` text
                         STUDENT
                            |
                            v
                      STREAMLIT APP
                            |
          +-----------------+------------------+----------------+
          |                 |                  |                |
          v                 v                  v                v
         ML              RESUME               RAG             AGENT
          |                 |                  |                |
          v                 v                  v                v
 Placement Prediction   Transformer          Chroma             MCP
                            |                  |                |
                            v                  v                v
                        Skill Gap           Groq LLM        MCP Server
                                                               |
                                                +--------------+-------------+
                                                |              |             |
                                                v              v             v
                                               ML          Skill Gap        RAG
                                               Tool           Tool          Tool
```

### Agent and MCP flow

The Streamlit application communicates with the agent layer. The agent
uses an MCP client to communicate with the MCP server; the server
exposes tools such as placement prediction, skill-gap analysis, and RAG.

``` text
Streamlit
    |
    v
agent.py
    |
    v
mcp_client.py
    |
    v
mcp_server.py
    |
    +------------------+------------------+
    |                  |                  |
    v                  v                  v
Placement Tool     Skill Gap Tool      RAG Tool
    |                  |                  |
    v                  v                  v
predict.py         skill_gap.py         rag.py
```

The intended design is for Streamlit to call the agent/client layer
rather than calling the MCP server directly.

### RAG pipeline

``` text
Knowledge Base
      |
      v
Document Loading
      |
      v
Text Splitting
      |
      v
Chunks
      |
      v
Embeddings
      |
      v
Vector Database (Chroma)
      |
      v
Retrieve Relevant Chunks
      |
      v
LLM (Groq)
      |
      v
Final Answer
```

RAG retrieves relevant information from a knowledge base before the
language model generates an answer.

## Main capabilities

  --------------------------------------------------------------------------
  Capability              Purpose                 Main project component
  ----------------------- ----------------------- --------------------------
  Placement prediction    Predicts placement      `src/predict.py`
                          outcome from student    
                          data                    

  Resume analysis         Processes a student's   `src/resume_analyzer.py`
                          resume and skills       

  Skill-gap analysis      Identifies skills to    `src/skill_gap.py`
                          improve for a target    
                          role                    

  Career Q&A              Retrieves relevant      `src/rag.py`
                          knowledge and generates 
                          an answer               

  Agent tools             Makes project           `src/tools.py`,
                          capabilities available  `src/agent.py`
                          as tools                

  MCP server              Exposes tools through   `src/mcp_server.py`
                          MCP                     

  User interface          Provides the            `app.py`
                          student-facing          
                          application             

  API backend             Provides HTTP endpoints FastAPI API package
                          for application         
                          functions               
  --------------------------------------------------------------------------

## Project structure

The following structure is based on the project layout recorded in the
supplied project notes. The API and deployment notes also refer to an
`api/` package and a `deployment/` directory; include those in the
repository if they exist in your implementation.

``` text
AI-Career-Assistant/
│
├── data/
│   ├── raw/
│   │   └── student_placement.csv
│   └── processed/
│       ├── train_processed.csv
│       └── test_processed.csv
│
├── models/
│   └── placement_model.joblib
│
├── reports/
│   ├── metrics.json
│   └── figures/
│       ├── actual_vs_predicted.png
│       └── residuals.png
│
├── documents/
│   ├── roadmap.txt
│   ├── ml_notes.txt
│   └── interview_questions.txt
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── dataset.py
│   ├── features.py
│   ├── train.py
│   ├── predict.py
│   ├── resume_analyzer.py
│   ├── skill_gap.py
│   ├── rag.py
│   ├── tools.py
│   ├── agent.py
│   └── mcp_server.py
│
├── app.py
├── requirements.txt
└── .env
```

## Technology and tools

The supplied notes identify these technologies and components:

-   **Python** --- application and ML implementation language.
-   **Streamlit** --- student-facing user interface.
-   **FastAPI** --- HTTP API backend.
-   **Uvicorn** --- ASGI server used to run FastAPI.
-   **Machine Learning** --- placement prediction.
-   **Transformer** --- resume/skill analysis component noted in the
    architecture.
-   **Chroma** --- vector database for RAG retrieval.
-   **Groq LLM** --- language model used in the career-question RAG
    flow.
-   **MCP** --- standard protocol for connecting the agent application
    to tools.
-   **Docker and Docker Compose** --- containerization and multi-service
    orchestration.
-   **Git and GitHub** --- source control and repository hosting.

The exact model names, embedding model, package versions, and
environment-variable names are not specified in the supplied notes.

## FastAPI backend

The API notes describe these application endpoints:

  Endpoint                  Purpose
  ------------------------- ---------------------------------------
  `GET /`                   Returns an API-running message
  `GET /health`             Returns the health status
  `POST /predict`           Placement prediction
  `POST /resume-analysis`   Resume analysis
  `POST /skill-gap`         Skill-gap analysis
  `/career-question`        Career question answering through RAG
  `/agent`                  Agent interaction

The exact request and response schemas for the feature endpoints should
be documented from the implemented API code.

### Run FastAPI locally

From the project root, the supplied notes use:

``` bash
uvicorn api.main:app --reload
```

Open the interactive API documentation:

``` text
http://127.0.0.1:8000/docs
```

FastAPI uses Pydantic `BaseModel` classes to validate structured request
data. For example, a student input model can declare `cgpa: float`,
allowing the API to validate that the submitted CGPA is numeric.

For file-upload endpoints, the notes identify FastAPI's `UploadFile` and
`File()` utilities. `HTTPException` can be used to return API errors,
and temporary-file handling can be used when an uploaded file needs to
be saved temporarily.

## Connect Streamlit to FastAPI

The intended request flow is:

``` text
Streamlit
    |
    v
requests.post()
    |
    v
FastAPI endpoint (for example, /predict)
    |
    v
Existing project function (for example, predict_placement())
    |
    v
API response
    |
    v
Streamlit
```

The existing functions in `src/` remain part of the backend workflow.
The Streamlit frontend sends HTTP requests to FastAPI rather than
directly invoking those functions.

For a local, non-containerized setup, the API host is typically
configured as:

``` python
API_URL = "http://127.0.0.1:8000"
```

When Streamlit and FastAPI run as services in the same Docker Compose
network, the supplied notes specify:

``` python
API_URL = "http://fastapi:8000"
```

The service name `fastapi` is used for service-to-service communication
inside the Compose network. The browser accesses the Streamlit service
through `http://localhost:8501`.

## Run with Docker

The supplied deployment notes include a single-image Docker workflow.

### Build the image

If the Dockerfile is in the project root:

``` bash
docker build -t ai-career-assistant .
```

If the Dockerfile is in `deployment/`:

``` bash
docker build -t ai-career-assistant -f deployment/Dockerfile .
```

### Run the container

``` bash
docker run -p 8080:8080 --env-file .env ai-career-assistant
```

Open:

``` text
http://localhost:8080
```

The port mapping and application port must match the port configured by
the actual Dockerfile/application.

### Docker Compose for Streamlit and FastAPI

For the two-service architecture, the project notes recommend Docker
Compose:

``` text
Streamlit container (port 8501)
          |
          v
FastAPI container (port 8000)
          |
          v
ML / RAG / Agent
```

Build the services:

``` bash
docker compose build
```

To rebuild without using the build cache:

``` bash
docker compose build --no-cache
```

Start the services:

``` bash
docker compose up
```

Stop and remove the containers created by Compose:

``` bash
docker compose down
```

When both services are running, the supplied notes list these local
URLs:

  Service              URL
  -------------------- ------------------------------
  Streamlit            `http://localhost:8501`
  FastAPI              `http://localhost:8000`
  FastAPI Swagger UI   `http://localhost:8000/docs`

The actual Compose service definitions and Dockerfile contents were not
included in the supplied notes. Confirm the configured ports and service
names against those files in the repository.

## Run the MCP server separately

The deployment notes include this command for starting an MCP server
from an existing image:

``` bash
docker run -p 8000:8000 mcp-server
```

This assumes that an image named `mcp-server` already exists and that
the server listens on the mapped container port.

## GitHub setup

Create a GitHub repository (the supplied example repository name is
`AI-Career-Assistant`), then run these commands from the project
directory:

``` bash
git init
git add .
git status
git commit -m "AI Career Assistant complete project"
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git branch -M main
git push -u origin main
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the URL of your own GitHub
repository.

Before committing, ensure that secrets and local environment files are
not accidentally published. The supplied notes show a `.env` file but do
not provide its contents; keep credentials and API keys private.

## Suggested development and deployment sequence

The supplied project notes describe this implementation order:

1.  Build and verify the Streamlit application.
2.  Add the FastAPI backend.
3.  Test the API using Swagger UI at `/docs`.
4.  Connect Streamlit to FastAPI using HTTP requests.
5.  Dockerize the FastAPI and Streamlit services.
6.  Test communication between the containers.
7.  Prepare and perform cloud deployment.

For the agent integration, first get the agent working with its tools,
then add MCP as the standard tool-connection layer.

## Important concepts

-   **RAG:** Gives the language model access to relevant information
    retrieved from a knowledge base.
-   **AI Agent:** Decides what action to take and which available tools
    to use for a task.
-   **MCP:** Provides a standard protocol through which an AI
    application can discover and use tools.

In this project, RAG provides knowledge, tools provide capabilities, and
the agent decides how to use those capabilities to help complete a
student's task.

## Configuration

Create a local `.env` file for the environment variables required by
your implementation. Do not commit secrets to GitHub.

The supplied notes do not specify the required variable names or values.
Refer to the project's configuration and application code to determine
them.

## Current implementation notes and items to verify

The supplied source notes describe the intended architecture and
selected commands, but do not include every implementation detail.
Before publishing this README as final project documentation, verify:

-   The exact installed packages and versions in `requirements.txt`.
-   The actual API endpoint paths and request/response schemas.
-   The model and embedding model names.
-   The required `.env` variable names.
-   The Dockerfile location, exposed ports, and Docker Compose service
    names.
-   Whether the MCP server uses port `8000` in the current
    implementation.
-   The actual cloud provider and deployment procedure.

------------------------------------------------------------------------

*Project name: AI Student Career & Placement Assistant*
