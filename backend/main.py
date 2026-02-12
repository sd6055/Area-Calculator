from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # Pydantic helps us define and validate data shapes
from calculator import calculate_square_area

# ============ DATA MODEL ============
# This defines what a valid request to our API should look like
# We're telling FastAPI: "Expect a JSON object with a 'side' field that's a float"
class SquareRequest(BaseModel):
    side: float

# ============ APP SETUP ============
# Create the FastAPI application instance
app = FastAPI()

# ============ CORS CONFIGURATION ============
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

# ============ API ENDPOINTS ============

# Endpoint: POST /api/area/square
# Calculates the area of a square given a side length
# Now expects: {"side": 5} instead of just 5
@app.post("/api/area/square")
async def area_square(request: SquareRequest):  # FastAPI automatically parses the JSON into our SquareRequest object
    # SECURITY: Never trust user input!
    # Validate that side is positive
    if request.side <= 0:
        return {"error": "Side length must be positive"}
    
    # Validate that side isn't ridiculously large
    if request.side > 1000000:
        return {"error": "Value too large - maximum is 1,000,000"}
    
    # If validation passes, do the actual calculation
    area = calculate_square_area(request.side)  # Access the side value with request.side
    return {"area": area}

# Simple test endpoint to verify the API is running
@app.get("/")
async def root():
    return {"message": "API is running"}