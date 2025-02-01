# Multilingual FAQ System Documentation

## Overview

The **Multilingual FAQ System** is built using **FastAPI**, providing a platform for managing multilingual FAQs. It features automatic translation via **Google Translate** and uses **Redis caching** to enhance performance.

## Features

- **CRUD Operations** for FAQ management.
- **Automatic Translations** using Google Translate.
- **Redis Caching** to speed up the responses.
- **Support for Multiple Languages**.
- A RESTful **API** with **OpenAPI** documentation.
- **Docker** support for easy deployment.

## Installation

### Using Docker

To run the application with Docker, execute the following:

```bash
docker-compose up -d
```

This will start the necessary services, including **Redis** and the **FastAPI** application.

### Manual Installation

To install the system manually, follow these steps:

1. **Set up the Virtual Environment**:
   On **Linux/Mac**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   On **Windows**:
   ```bash
   .\venv\Scripts\activate
   ```

2. **Install the Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Redis Server** on your local machine.

4. **Start the Application**:
   Run the following command to start FastAPI with **Uvicorn**:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### `POST /faqs/`

- **Description**: Create a new FAQ.
- **Request Body**:
  ```json
  {
    "question_en": "What is FastAPI?",
    "answer_en": "FastAPI is a modern web framework."
  }
  ```
- **Response**: 
  Returns the created FAQ with an optional translation.

### `GET /faqs/`

- **Description**: Retrieve a list of all FAQs.
- **Query Parameters**:
  - `lang` (optional): Specify the language for the FAQ content (e.g., `hi` for Hindi).
  
  Example Request:
  ```bash
  curl "http://localhost:8000/faqs/?lang=hi"
  ```
  
- **Response**: 
  Returns the list of FAQs. If a `lang` parameter is provided, it returns the FAQs in that language (with translations if available).

## Example Usage

### Create a New FAQ
To create a new FAQ, you can use **curl**:

```bash
curl -X POST "http://localhost:8000/faqs/" \
     -H "Content-Type: application/json" \
     -d '{"question_en": "What is FastAPI?", "answer_en": "FastAPI is a modern web framework."}'
```

### Get FAQs in a Different Language
For retrieving FAQs in Hindi, use the following command:

```bash
curl "http://localhost:8000/faqs/?lang=hi"
```

## Testing

To run the project tests, use the following command:

```bash
pytest
```

Make sure **Redis** is running, and all dependencies are installed before testing.

## Contributing

To contribute to this project:

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes using conventional commit messages.
4. Push your changes to the feature branch.
5. Create a **Pull Request** for review.

## License

This project is licensed under the **MIT License**.
```
This is the `docs.md` you provided, ready to be used.  There's no need for additional conversion or modification in this case.
