// The address where our backend API is running
// 127.0.0.1 is your own computer (localhost)
const API_URL = 'http://127.0.0.1:8000';

// This function runs when the user clicks the Calculate button
async function calculateArea() {
    // Get references to HTML elements we need to read/write
    const sideInput = document.getElementById('side');      // Input box
    const resultElement = document.getElementById('result'); // Where we show the answer
    const side = sideInput.value;                            // What user typed
    
    // FRONTEND VALIDATION: Catch errors before sending to backend
    // Check if input is empty, zero, or negative
    if (!side || side <= 0) {
        resultElement.innerText = 'Please enter a positive number';
        return;  // Stop here, don't call the API
    }
    
    try {
        // Send data to our backend API
        // fetch() is JavaScript's way of making HTTP requests
        const response = await fetch(`${API_URL}/api/area/square`, {
            method: 'POST',                                // We're sending data
            headers: {
                'Content-Type': 'application/json',        // Tell backend we're sending JSON
            },
            body: JSON.stringify({ side: parseFloat(side) }) // Convert to JSON format
        });
        
        // Wait for the backend to respond and parse the JSON response
        const data = await response.json();
        
        // Check if our API returned an error message
        if (data.error) {
            // Show the error message from the backend
            resultElement.innerText = `Error: ${data.error}`;
        } else {
            // No error! Show the calculated area
            resultElement.innerText = `Area: ${data.area}`;
        }
    } catch (error) {
        // Something went wrong with the network/connection
        // This happens if backend isn't running or address is wrong
        resultElement.innerText = 'Error: Could not connect to server';
        console.error('Error:', error);  // Log technical details to browser console
    }
}

// SETUP: This code runs when the page first loads
document.addEventListener('DOMContentLoaded', function() {
    // Find the Calculate button on the page
    const button = document.querySelector('button');
    
    // Tell the button: "When someone clicks you, run calculateArea"
    if (button) {
        button.addEventListener('click', calculateArea);
    }
});