/*
 * script.js - Frontend logic
 * Updated: Now shows calculation history from MySQL
 */

// API URL (unchanged)
const API_URL = 'http://127.0.0.1:8000';

// Main calculation function (updated to show more info)
async function calculateArea() {
    const sideInput = document.getElementById('side');
    const resultElement = document.getElementById('result');
    const side = sideInput.value;
    
    // Validation (unchanged)
    if (!side || side <= 0) {
        resultElement.innerText = 'Please enter a positive number';
        return;
    }
    
    try {
        // Send request to backend (unchanged)
        const response = await fetch(`${API_URL}/api/area/square`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ side: parseFloat(side) })
        });
        
        const data = await response.json();
        
        // Show result WITH calculation ID from database
        if (data.error) {
            resultElement.innerText = `Error: ${data.error}`;
        } else {
            resultElement.innerText = `Area: ${data.area} (Saved as #${data.calculation_id})`;
            
            // Refresh the history display
            loadHistory();
        }
    } catch (error) {
        resultElement.innerText = 'Error: Could not connect to server';
        console.error('Error:', error);
    }
}

// NEW FUNCTION: Load calculation history from MySQL
async function loadHistory() {
    try {
        // Fetch the 5 most recent calculations
        const response = await fetch(`${API_URL}/api/calculations?limit=5`);
        const history = await response.json();
        
        // Find or create a history display element
        let historyElement = document.getElementById('history');
        
        // If history element doesn't exist, create it
        if (!historyElement) {
            historyElement = document.createElement('div');
            historyElement.id = 'history';
            historyElement.innerHTML = '<h3>Recent Calculations:</h3>';
            
            // Insert after the result element
            const resultElement = document.getElementById('result');
            resultElement.parentNode.insertBefore(historyElement, resultElement.nextSibling);
        }
        
        // Clear old history (keep the heading)
        while (historyElement.children.length > 1) {
            historyElement.removeChild(historyElement.lastChild);
        }
        
        // Add each calculation to the display
        if (history.length === 0) {
            const emptyMsg = document.createElement('p');
            emptyMsg.textContent = 'No calculations yet';
            historyElement.appendChild(emptyMsg);
        } else {
            history.forEach(calc => {
                const calcDiv = document.createElement('div');
                calcDiv.className = 'history-item';
                
                // Format the timestamp
                const date = new Date(calc.created_at);
                const timeString = date.toLocaleTimeString();
                
                calcDiv.innerHTML = `
                    <span class="history-shape">${calc.shape}</span>
                    <span class="history-input">${calc.input_value} → </span>
                    <span class="history-result">${calc.result}</span>
                    <span class="history-time">(${timeString})</span>
                `;
                
                historyElement.appendChild(calcDiv);
            });
        }
    } catch (error) {
        console.error('Failed to load history:', error);
    }
}

// Setup (unchanged)
document.addEventListener('DOMContentLoaded', function() {
    const button = document.querySelector('button');
    if (button) {
        button.addEventListener('click', calculateArea);
    }
    
    // Load history when page first opens
    loadHistory();
    
    // Optional: Refresh history every 30 seconds
    setInterval(loadHistory, 30000);
});

// Add to script.js - get calculation statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_URL}/api/stats/count`);
        const stats = await response.json();
        
        let statsElement = document.getElementById('stats');
        if (!statsElement) {
            statsElement = document.createElement('div');
            statsElement.id = 'stats';
            statsElement.innerHTML = '<h3>Statistics:</h3>';
            
            const historyElement = document.getElementById('history');
            historyElement.parentNode.insertBefore(statsElement, historyElement);
        }
        
        statsElement.innerHTML = `
            <h3>Statistics:</h3>
            <p>Total calculations: ${stats.count}</p>
        `;
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

// Update your DOMContentLoaded to also load stats
document.addEventListener('DOMContentLoaded', function() {
    const button = document.querySelector('button');
    if (button) {
        button.addEventListener('click', calculateArea);
    }
    
    loadHistory();
    loadStats();  // NEW: Load stats on page load
});