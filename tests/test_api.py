import pytest  # @ Importing pytest for writing and running tests.
from fastapi.testclient import TestClient  # @ Importing TestClient from FastAPI to simulate HTTP requests for testing.
from sqlalchemy import create_engine  # @ Importing create_engine from SQLAlchemy for setting up the database engine.
from sqlalchemy.orm import sessionmaker  # @ Importing sessionmaker to handle database sessions.
from app.main import app  # @ Importing the FastAPI app from the main module.
from app.database import Base, get_db  # @ Importing the Base (for models) and get_db (for database session) from the database module.

# Setting up an in-memory SQLite database for testing purposes.
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # @ Defining the database URL for testing.

# Creating a database engine using the test database URL.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})  # @ Setting up the engine.

# Creating a session maker bound to the test database engine.
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # @ Defining session maker for testing.

# Overriding the get_db function to use the test session for database operations during tests.
def override_get_db():  # @ Defining a function to override the get_db dependency.
    db = TestingSessionLocal()  # @ Creating a new session for the test.
    try:
        yield db  # @ Yield the session to be used in tests.
    finally:
        db.close()  # @ Closing the session after the test completes.

# Replacing the original get_db dependency with the overridden one.
app.dependency_overrides[get_db] = override_get_db  # @ Replacing the dependency in FastAPI app with the overridden one.

client = TestClient(app)  # @ Creating an instance of TestClient to simulate HTTP requests to the FastAPI app.

@pytest.fixture(autouse=True)  # @ Automatically setting up the database before each test and cleaning it up after.
def setup_database():
    Base.metadata.create_all(bind=engine)  # @ Creating all database tables before the test.
    yield  # @ Running the test.
    Base.metadata.drop_all(bind=engine)  # @ Dropping all database tables after the test.

# Test case to test the creation of a FAQ.
def test_create_faq():
    response = client.post(  # @ Sending a POST request to create a new FAQ.
        "/faqs/",  # @ The endpoint to create a FAQ.
        json={  # @ The request body containing the FAQ data.
            "question_en": "What is FastAPI?",  # @ The question for the FAQ.
            "answer_en": "FastAPI is a modern web framework for building APIs with Python."  # @ The answer for the FAQ.
        }
    )
    assert response.status_code == 200  # @ Checking if the response status code is 200 (OK).
    data = response.json()  # @ Parsing the response JSON data.
    assert data["question_en"] == "What is FastAPI?"  # @ Checking if the question in the response matches the input.
    assert "translations" in data  # @ Ensuring the response contains translations.

# Test case to test fetching the FAQs.
def test_get_faqs():
    # Creating a test FAQ first to test the GET functionality.
    client.post(
        "/faqs/",  # @ The endpoint to create a FAQ.
        json={  # @ The request body containing the FAQ data.
            "question_en": "Test Question",  # @ The question for the FAQ.
            "answer_en": "Test Answer"  # @ The answer for the FAQ.
        }
    )
    
    response = client.get("/faqs/")  # @ Sending a GET request to retrieve the FAQs.
    assert response.status_code == 200  # @ Checking if the response status code is 200 (OK).
    data = response.json()  # @ Parsing the response JSON data.
    assert len(data) > 0  # @ Ensuring that at least one FAQ is returned.
    
    # Test with language parameter.
    response = client.get("/faqs/?lang=hi")  # @ Sending a GET request to fetch FAQs with the 'hi' (Hindi) language.
    assert response.status_code == 200  # @ Checking if the response status code is 200 (OK).
    data = response.json()  # @ Parsing the response JSON data.
    assert len(data) > 0  # @ Ensuring that at least one FAQ is returned.
    assert any(t["language"] == "hi" for faq in data for t in faq["translations"])  # @ Verifying that a translation in Hindi is available.
