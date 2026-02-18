"""
models.py - Defines what your database tables look like
Purpose: Each class here becomes a table in MySQL
"""

from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Calculation(Base):
    """
    This class represents the 'calculations' table in MySQL
    Each attribute becomes a column in the table
    Each instance of this class becomes a row in the table
    """
    
    # __tablename__ tells SQLAlchemy what to name the table in MySQL
    __tablename__ = "calculations"
    
    # COLUMN DEFINITIONS - Each one is a column in your table
    id = Column(Integer, primary_key=True, index=True)  # Auto-incrementing ID
    shape = Column(String(50), nullable=False)  # 'square', 'circle', etc.
    input_value = Column(Float, nullable=False)  # User's input (side, radius, etc.)
    result = Column(Float, nullable=False)  # Calculated area
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Timestamp
    
    # REPRESENTATION - Helps when debugging
    def __repr__(self):
        return f"<Calculation {self.shape}: {self.input_value} → {self.result}>"