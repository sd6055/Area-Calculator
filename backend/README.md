# Polygon Calculator Backend

This backend is a FastAPI application that calculates the area of polygons and stores the results in a MySQL database.

## Features

- Calculate the area of a square.
- Store calculation history in a MySQL database.
- Provide a RESTful API to create, retrieve, and delete calculations.

## Setup

1.  **Database Setup:**
    - Make sure you have MySQL installed and running.
    - Create a database named `polygon_calculator`.
    - Create a MySQL user named `calculator_app` with the password `calculator123` and grant it permissions to the `polygon_calculator` database.

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Backend

To run the backend server, use the following command:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

- `GET /`: Root endpoint, returns a welcome message.
- `POST /api/area/square`: Calculates the area of a square and saves it to the database.
  - **Request Body:** `{ "side": <float> }`
- `GET /api/calculations`: Get all calculations.
- `GET /api/calculations/recent`: Get the 5 most recent calculations.
- `GET /api/calculations/{calculation_id}`: Get a specific calculation by ID.
- `GET /api/calculations/shape/{shape}`: Get all calculations for a specific shape.
- `GET /api/stats/count`: Get the total number of calculations.
- `DELETE /api/calculations/{calculation_id}`: Delete a specific calculation.
