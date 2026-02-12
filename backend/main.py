from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from calculator import calculate_square_area

# Create the FastAPI application instance
app = FastAPI()

# CORS = Cross-Origin Resource Sharing
# This controls which websites can talk to our API
app.add_middleware(
    CORSMiddleware,
    # Only allow these specific addresses to access our API
    allow_origins=[
        "http://127.0.0.1:8000",  # Our backend itself
        "http://localhost:8000",   # Same backend, different name
        "null",                    # Allows opening HTML directly from file://
    ],
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all HTTP headers
)

# Endpoint: POST /api/area/square
# Calculates the area of a square given a side length
@app.post("/api/area/square")
async def area_square(side: float):
    # SECURITY: Never trust user input!
    # Validate that side is positive
    if side <= 0:
        return {"error": "Side length must be positive"}
    
    # Validate that side isn't ridiculously large
    if side > 1000000:
        return {"error": "Value too large - maximum is 1,000,000"}
    
    # If validation passes, do the actual calculation
    area = calculate_square_area(side)
    return {"area": area}

# Simple test endpoint to verify the API is running
@app.get("/")
async def root():
    return {"message": "API is running"}