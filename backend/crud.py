"""
crud.py - Database operations (Create, Read, Update, Delete)
Purpose: All functions that talk directly to the database live here
This keeps main.py clean and focused on web stuff
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc
import models
from typing import List, Optional

# ============ CREATE operations ============

def create_calculation(db: Session, shape: str, input_value: float, result: float):
    """
    Save a new calculation to the database
    
    Args:
        db: Database session
        shape: Type of shape ('square', 'circle', etc.)
        input_value: The user's input (side, radius, etc.)
        result: Calculated area
    
    Returns:
        The saved Calculation object (with ID and timestamp)
    """
    # Create the database object
    db_calculation = models.Calculation(
        shape=shape,
        input_value=input_value,
        result=result
    )
    
    # Add to database
    db.add(db_calculation)
    db.commit()
    db.refresh(db_calculation)  # Get the auto-generated ID and timestamp
    
    return db_calculation

# ============ READ operations ============

def get_calculation(db: Session, calculation_id: int):
    """
    Get a single calculation by its ID
    
    Args:
        db: Database session
        calculation_id: The ID of the calculation to fetch
    
    Returns:
        Calculation object or None if not found
    """
    return db.query(models.Calculation)\
             .filter(models.Calculation.id == calculation_id)\
             .first()

def get_all_calculations(db: Session, skip: int = 0, limit: int = 100):
    """
    Get multiple calculations, newest first, with pagination
    
    Args:
        db: Database session
        skip: How many records to skip (for pagination)
        limit: Maximum number of records to return
    
    Returns:
        List of Calculation objects
    """
    return db.query(models.Calculation)\
             .order_by(desc(models.Calculation.created_at))\
             .offset(skip)\
             .limit(limit)\
             .all()

def get_calculations_by_shape(db: Session, shape: str, limit: int = 50):
    """
    Get all calculations for a specific shape
    
    Args:
        db: Database session
        shape: The shape to filter by ('square', 'circle', etc.)
        limit: Maximum number of records to return
    
    Returns:
        List of Calculation objects for that shape
    """
    return db.query(models.Calculation)\
             .filter(models.Calculation.shape == shape)\
             .order_by(desc(models.Calculation.created_at))\
             .limit(limit)\
             .all()

def get_recent_calculations(db: Session, limit: int = 10):
    """
    Get the most recent calculations (convenience function)
    
    Args:
        db: Database session
        limit: How many recent calculations to return
    
    Returns:
        List of the most recent Calculation objects
    """
    return get_all_calculations(db, skip=0, limit=limit)

def count_calculations(db: Session, shape: Optional[str] = None):
    """
    Count total calculations, optionally filtered by shape
    
    Args:
        db: Database session
        shape: If provided, only count this shape
    
    Returns:
        Integer count
    """
    query = db.query(models.Calculation)
    if shape:
        query = query.filter(models.Calculation.shape == shape)
    return query.count()

# ============ UPDATE operations ============

def update_calculation_result(db: Session, calculation_id: int, new_result: float):
    """
    Update a calculation's result (rarely needed, but here for completeness)
    
    Args:
        db: Database session
        calculation_id: Which calculation to update
        new_result: The new area value
    
    Returns:
        Updated Calculation object or None if not found
    """
    calculation = get_calculation(db, calculation_id)
    if calculation:
        calculation.result = new_result
        db.commit()
        db.refresh(calculation)
    return calculation

# ============ DELETE operations ============

def delete_calculation(db: Session, calculation_id: int):
    """
    Delete a specific calculation
    
    Args:
        db: Database session
        calculation_id: Which calculation to delete
    
    Returns:
        True if deleted, False if not found
    """
    calculation = get_calculation(db, calculation_id)
    if calculation:
        db.delete(calculation)
        db.commit()
        return True
    return False

def delete_all_calculations(db: Session):
    """
    Delete ALL calculations (use with caution!)
    
    Args:
        db: Database session
    
    Returns:
        Number of records deleted
    """
    count = db.query(models.Calculation).delete()
    db.commit()
    return count