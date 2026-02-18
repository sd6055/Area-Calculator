"""
main.py - The web layer connecting everything
New: Now saves every calculation to MySQL!
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

# Your existing modules
from calculator import calculate_square_area

# NEW: Database modules
import models
from database import engine, get_db

# CREATE TABLES - This runs once when app starts
# If tables don't exist in MySQL, SQLAlchemy creates them
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

# CORS setup (unchanged)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "null",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request validation
class SquareRequest(BaseModel):
    side: float

# Pydantic model for response (includes database fields)
class CalculationResponse(BaseModel):
    id: int
    shape: str
    input_value: float
    result: float
    created_at: str
    
    class Config:
        from_attributes = True  # Tells Pydantic to work with SQLAlchemy models

@app.post("/api/area/square")
async def area_square(
    request: SquareRequest, 
    db: Session = Depends(get_db)  # Get database connection
):
    """
    Calculate square area AND save to database
    """
    # 1. VALIDATION (unchanged)
    if request.side <= 0:
        return {"error": "Side length must be positive"}
    if request.side > 1000000:
        return {"error": "Value too large - maximum is 1,000,000"}
    
    # 2. CALCULATION (unchanged)
    area = calculate_square_area(request.side)
    
    # 3. SAVE TO DATABASE ✨ NEW!
    # Create a new Calculation object
    db_calculation = models.Calculation(
        shape="square",
        input_value=request.side,
        result=area
    )
    
    # Add to database session
    db.add(db_calculation)
    
    # Commit transaction (permanently save)
    db.commit()
    
    # Refresh to get auto-generated ID and timestamp
    db.refresh(db_calculation)
    
    # 4. RETURN result with database info
    return {
        "area": area,
        "calculation_id": db_calculation.id,
        "timestamp": db_calculation.created_at.isoformat() if db_calculation.created_at else None
    }

@app.get("/api/calculations", response_model=List[CalculationResponse])
async def get_all_calculations(
    skip: int = 0,  # How many records to skip (for pagination)
    limit: int = 10,  # How many records to return
    db: Session = Depends(get_db)
):
    """
    Get all calculations, newest first
    """
    calculations = db.query(models.Calculation)\
        .order_by(models.Calculation.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    return calculations

@app.get("/api/calculations/{calculation_id}", response_model=CalculationResponse)
async def get_calculation_by_id(
    calculation_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific calculation by its ID
    """
    calculation = db.query(models.Calculation)\
        .filter(models.Calculation.id == calculation_id)\
        .first()
    
    if not calculation:
        raise HTTPException(status_code=404, detail="Calculation not found")
    
    return calculation

@app.get("/api/calculations/shape/{shape}", response_model=List[CalculationResponse])
async def get_calculations_by_shape(
    shape: str,
    db: Session = Depends(get_db)
):
    """
    Get all calculations for a specific shape
    """
    calculations = db.query(models.Calculation)\
        .filter(models.Calculation.shape == shape)\
        .order_by(models.Calculation.created_at.desc())\
        .all()
    return calculations

@app.get("/")
async def root():
    return {"message": "Polygon Calculator API with MySQL is running!"}