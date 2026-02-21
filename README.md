# Polygon Calculator

This project is a full-stack web application that calculates the area of polygons and stores the results. It consists of a FastAPI backend and a simple HTML, CSS, and JavaScript frontend.

## Project Structure

-   `/backend`: Contains the FastAPI application, which handles the business logic, interacts with the database, and provides a RESTful API.
-   `/frontend`: Contains the user interface, which is a single-page application that communicates with the backend API.

## Features

-   **Backend (FastAPI & MySQL):**
    -   Calculates the area of a square.
    -   Stores calculation history in a MySQL database.
    -   Provides API endpoints for creating, retrieving, and deleting calculations.
-   **Frontend (HTML, CSS, JS):**
    -   A simple user interface to calculate the area of a square.
    -   Displays the result and a history of recent calculations.
    -   Automatically refreshes the history.

## Getting Started

### 1. Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Set up the database:**
    -   Make sure you have MySQL installed and running.
    -   Create a database named `polygon_calculator`.
    -   Create a MySQL user named `calculator_app` with the password `calculator123` and grant it permissions to the `polygon_calculator` database.
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the backend server:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

### 2. Frontend Usage

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Open in browser:**
    -   Open the `index.html` file in your web browser.

You can now use the Polygon Calculator!

## Technologies Used

-   **Backend:**
    -   Python
    -   FastAPI
    -   SQLAlchemy
    -   MySQL
-   **Frontend:**
    -   HTML
    -   CSS
    -   JavaScript
