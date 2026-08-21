
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Load variables from the .env file
load_dotenv()


# Read the PostgreSQL connection URL
DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the .env file")


# Create the connection to PostgreSQL
engine = create_engine(
    DATABASE_URL,
    echo=False
)


# SessionLocal creates database sessions.
# A session is used to read/write data in the database.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    Our Book, Member, and Loan models will inherit from this class.
    """
    pass