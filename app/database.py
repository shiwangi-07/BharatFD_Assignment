from sqlalchemy import create_engine  # @ Importing the SQLAlchemy function to create database engines.
from sqlalchemy.ext.declarative import declarative_base  # @ Importing the base class for model definitions.
from sqlalchemy.orm import sessionmaker  # @ Importing the sessionmaker to handle database sessions.
import redis  # @ Importing the Redis client library to interact with the Redis server.

# @ URL for the SQLite database. `faq.db` is the local SQLite database file.
SQLALCHEMY_DATABASE_URL = "sqlite:///./faq.db"

# @ Creating the SQLAlchemy engine that connects to the database. The `check_same_thread` argument is specific to SQLite to allow multiple threads to access the database.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# @ Creating a sessionmaker that is used to create sessions for interacting with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @ Defining the base class for all models in SQLAlchemy.
Base = declarative_base()

# @ Redis connection initialization. Connecting to a local Redis server running on port 6379, using database 0.
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# @ Function to provide a session for the database. It is used in a context manager pattern (with `yield`).
# @ It ensures that the session is properly closed after use to avoid database connection leaks.
def get_db():
    db = SessionLocal()  # @ Creating a new database session.
    try:
        yield db  # @ Yielding the session to be used in the context where this function is called.
    finally:
        db.close()  # @ Closing the session after use.
