"""
main.py - The web layer
Now using crud.py for all database operations
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

# Your modules
from calculator import calculate_square_area
import models
import crud  # NEW: Import our CRUD operations
from database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

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

# Pydantic models
class SquareRequest(BaseModel):
    side: float

class CalculationResponse(BaseModel):
    id: int
    shape: str
    input_value: float
    result: float
    created_at: str
    
    class Config:
        from_attributes = True

@app.post("/api/area/square")
async def area_square(
    request: SquareRequest, 
    db: Session = Depends(get_db)
):
    """Calculate square area AND save to database"""
    # Validation
    if request.side <= 0:
        return {"error": "Side length must be positive"}
    if request.side > 1000000:
        return {"error": "Value too large - maximum is 1,000,000"}
    
    # Calculate
    area = calculate_square_area(request.side)
    
    # SAVE TO DATABASE using crud.py ✨
    db_calculation = crud.create_calculation(
        db=db,
        shape="square",
        input_value=request.side,
        result=area
    )
    
    return {
        "area": area,
        "calculation_id": db_calculation.id,
        "timestamp": db_calculation.created_at.isoformat() if db_calculation.created_at else None
    }

@app.get("/api/calculations", response_model=List[CalculationResponse])
async def get_all_calculations(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    """Get all calculations using crud.py"""
    calculations = crud.get_all_calculations(db, skip=skip, limit=limit)
    return calculations

@app.get("/api/calculations/recent", response_model=List[CalculationResponse])
async def get_recent_calculations(
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """Get most recent calculations using crud.py"""
    calculations = crud.get_recent_calculations(db, limit=limit)
    return calculations

@app.get("/api/calculations/{calculation_id}", response_model=CalculationResponse)
async def get_calculation_by_id(
    calculation_id: int,
    db: Session = Depends(get_db)
):
    """Get specific calculation using crud.py"""
    calculation = crud.get_calculation(db, calculation_id)
    if not calculation:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calculation

@app.get("/api/calculations/shape/{shape}", response_model=List[CalculationResponse])
async def get_calculations_by_shape(
    shape: str,
    db: Session = Depends(get_db)
):
    """Get calculations for a shape using crud.py"""
    calculations = crud.get_calculations_by_shape(db, shape)
    return calculations

@app.get("/api/stats/count")
async def get_calculation_count(
    shape: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get count of calculations, optionally by shape"""
    count = crud.count_calculations(db, shape)
    return {"count": count}

@app.delete("/api/calculations/{calculation_id}")
async def delete_calculation(
    calculation_id: int,
    db: Session = Depends(get_db)
):
    """Delete a specific calculation"""
    deleted = crud.delete_calculation(db, calculation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return {"message": f"Calculation {calculation_id} deleted"}

@app.get("/")
async def root():
    return {"message": "Polygon Calculator API with MySQL and CRUD operations!"}