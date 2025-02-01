# Multilingual FAQ System: An Overview

This project offers a FastAPI-based solution for handling multilingual Frequently Asked Questions. It incorporates automatic translation capabilities, caching for speed, and is designed for seamless use.

## Core Capabilities

-   **FAQ Management:** Handles all the essential operations (Create, Read, Update, Delete) for your FAQ entries.
-   **Automated Translation:** Leverages Google Translate to provide automatic translations.
-   **Performance Boost:** Uses Redis caching to enhance system responsiveness and speed up data retrieval.
-   **Multilingual Support:** Designed to accommodate FAQs in various languages.
-   **RESTful API:** A well-structured API accessible through common methods, along with OpenAPI generated documentation.
-   **Containerized Deployment:** Docker integration makes deployment a straightforward process.

## Setting Up the System

### Quick Start with Docker

```bash
docker-compose up -d
```

### Manual Setup Instructions

1.  **Set Up the Environment:** Create a virtual environment for dependency isolation.
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # or
    .\venv\Scripts\activate  # Windows
    ```

2.  **Install Required Packages:**  Install all project dependencies specified in the requirements file.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Launch Redis:** Start the Redis server; this is needed for the caching mechanism.

4.  **Run the Application:** Fire up the FastAPI application.
    ```bash
    uvicorn app.main:app --reload
    ```

## Exploring the API

Once the application is running, navigate to `http://localhost:8000/docs` or `http://localhost:8000/redoc` to interact with the Swagger documentation.

### API Highlights

-   `POST /faqs/`: Use this endpoint to submit a new FAQ.
-   `GET /faqs/`: Obtain the list of FAQs, with the ability to filter by a particular language.

### Practical Examples

**Adding a New FAQ:**
```bash
curl -X POST "http://localhost:8000/faqs/" \
     -H "Content-Type: application/json" \
     -d '{"question_en": "What is FastAPI?", "answer_en": "FastAPI is a modern web framework."}'
```

**Retrieving FAQs in Hindi:**
```bash
curl "http://localhost:8000/faqs/?lang=hi"
```

## Testing Strategy

Execute all unit tests using pytest.
```bash
pytest
```

## Contributing Guide

1. **Fork the Project:** Create your own copy of the repository.
2. **Branching Strategy:** Develop your features in dedicated branches.
3. **Commit Messages:** Follow conventional commit standards for clear and concise logs.
4. **Push Your Changes:** Upload your branch to your forked repository.
5. **Submit a Pull Request:** Open a PR to merge your changes into the main project.

## License Information

This project is released under the MIT License.
