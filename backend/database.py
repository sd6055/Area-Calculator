"""
database.py - Handles connection to MySQL
Purpose: Creates the bridge between your Python app and MySQL database
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# CONNECTION STRING - Tells SQLAlchemy how to find MySQL
# Format: mysql+pymysql://username:password@host:port/database_name
# Using YOUR custom username and password!
DATABASE_URL = "mysql+pymysql://calculator_app:calculator123@localhost:3306/polygon_calculator"

# ENGINE - The main connection point
# Think of this as the "bridge" between Python and MySQL
engine = create_engine(DATABASE_URL)

# SESSION FACTORY - Creates temporary connections to the database
# Each time your app needs to talk to the DB, it asks SessionLocal for a connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# BASE CLASS - All your database tables will inherit from this
# SQLAlchemy uses this to map Python classes to database tables
Base = declarative_base()

# DEPENDENCY - FastAPI uses this to get a database session for each request
# Each request gets its own connection, automatically closed when done
def get_db():
    db = SessionLocal()
    try:
        yield db  # This is where FastAPI uses the connection
    finally:
        db.close()  # Always close the connection when done!