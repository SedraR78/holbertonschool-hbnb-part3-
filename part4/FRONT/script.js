/* 
  HBNB Web Client - Tasks 0, 1 & 2
*/

// Utility functions
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function setCookie(name, value, days = 7) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = `expires=${date.toUTCString()}`;
    document.cookie = `${name}=${value}; ${expires}; path=/`;
}

// Task 1: Login
async function loginUser(email, password) {
    const response = await fetch('http://127.0.0.1:5001/api/v1/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    return response;
}

// Task 2: Fetch places
async function fetchPlaces(token) {
    const response = await fetch('http://127.0.0.1:5001//api/v1/places', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });
    
    if (!response.ok) throw new Error('Failed to fetch places');
    return await response.json();
}

// Task 2: Display places
function displayPlaces(places) {
    const container = document.getElementById('places-list');
    if (!container) return;

    container.innerHTML = places.map(place => `
        <div class="place-card">
            <h3>${place.name}</h3>
            <div class="place-price">$${place.price} per night</div>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        </div>
    `).join('');
}

// Task 2: Price filter
function setupPriceFilter(places) {
    const filter = document.getElementById('price-filter');
    if (!filter) return;

    filter.innerHTML = `
        <option value="">All Prices</option>
        <option value="10">$10</option>
        <option value="50">$50</option>
        <option value="100">$100</option>
    `;

    filter.addEventListener('change', function() {
        const maxPrice = this.value ? parseInt(this.value) : null;
        if (maxPrice) {
            const filtered = places.filter(place => place.price <= maxPrice);
            displayPlaces(filtered);
        } else {
            displayPlaces(places);
        }
    });
}

// Task 2: Authentication check
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
        // For demo - show sample places when not logged in
        displaySamplePlaces();
    } else {
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaces(token)
            .then(places => {
                displayPlaces(places);
                setupPriceFilter(places);
            })
            .catch(error => {
                console.error('Error:', error);
                displaySamplePlaces();
            });
    }
}

// Task 0: Sample data for design demo
function displaySamplePlaces() {
    const samplePlaces = [
        { id: 1, name: "Cozy Apartment", price: 89 },
        { id: 2, name: "Beach House", price: 120 },
        { id: 3, name: "Mountain Cabin", price: 150 }
    ];
    displayPlaces(samplePlaces);
    setupPriceFilter(samplePlaces);
}

// Initialize all pages
document.addEventListener('DOMContentLoaded', () => {
    // Task 1: Login page
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const errorDiv = document.getElementById('login-error');

            try {
                const response = await loginUser(email, password);
                if (response.ok) {
                    const data = await response.json();
                    setCookie('token', data.access_token);
                    window.location.href = 'index.html';
                } else {
                    errorDiv.textContent = 'Login failed';
                    errorDiv.style.display = 'block';
                }
            } catch (error) {
                errorDiv.textContent = 'Network error';
                errorDiv.style.display = 'block';
            }
        });
    }

    // Task 2: Index page
    if (window.location.pathname.includes('index.html') || 
        window.location.pathname === '/' || 
        window.location.pathname.endsWith('/')) {
        checkAuthentication();
    }

    // Task 0: Demo data for other pages
    if (window.location.pathname.includes('place.html')) {
        // Simple demo for place details page
        console.log('Place details page loaded');
    }
    
    if (window.location.pathname.includes('add_review.html')) {
        // Simple demo for add review page  
        console.log('Add review page loaded');
    }
});

document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ JavaScript is loaded!');
    
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        console.log('✅ Login form found!');
        
        loginForm.addEventListener('submit', async (event) => {
            console.log('✅ Form submit event caught!');
            event.preventDefault(); // This should stop the normal form submission
            
            // Rest of your login code...
        });
    } else {
        console.log('❌ Login form NOT found!');
    }
});