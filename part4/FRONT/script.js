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

function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

// Fonction pour mettre à jour l'UI en fonction de l'authentification
function updateAuthUI() {
    const token = getCookie('token');
    const loginLinks = document.querySelectorAll('#login-link, .login-button[href="login.html"]');
    const logoutButtons = document.querySelectorAll('.logout-button');
    
    if (token) {
        // Utilisateur connecté
        loginLinks.forEach(link => link.style.display = 'none');
        logoutButtons.forEach(btn => btn.style.display = 'block');
    } else {
        // Utilisateur non connecté
        loginLinks.forEach(link => link.style.display = 'block');
        logoutButtons.forEach(btn => btn.style.display = 'none');
    }
}

// Logout function
function logout() {
    deleteCookie('token');
    updateAuthUI();
    window.location.href = 'index.html';
}

// Données de test
const sampleData = {
    places: [
        { id: 1, title: "Cozy Apartment in Paris", price: 120, description: "Beautiful apartment with Eiffel Tower view" },
        { id: 2, title: "Beach House in Bali", price: 200, description: "Luxurious beachfront villa with private pool" },
        { id: 3, title: "Mountain Cabin in Colorado", price: 150, description: "Rustic cabin with stunning mountain views" }
    ],
    placeDetails: {
        1: { 
            id: 1, title: "Cozy Apartment in Paris", price: 120, host_name: "Jean Dupont",
            description: "Beautiful apartment with stunning Eiffel Tower view in the heart of Paris.",
            amenities: ["WiFi", "Kitchen", "TV", "Air Conditioning", "Washer"]
        }
    },
    reviews: {
        1: [
            { user_name: "Marie Laurent", rating: 5, text: "Amazing location and the host was very responsive!" }
        ]
    }
};

// Task 2: Display places
function displayPlaces(places) {
    const container = document.getElementById('places-list');
    if (!container) return;
    
    container.innerHTML = places.map(place => `
        <div class="place-card">
            <div class="place-card-content">
                <h3>${place.title}</h3>
                <div class="place-price">$${place.price} per night</div>
                <p>${place.description}</p>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            </div>
        </div>
    `).join('');
}

// Task 3: Display place details
function displayPlaceDetails(place) {
    const container = document.getElementById('place-details');
    if (!container) return;

    container.innerHTML = `
        <div class="place-info">
            <h2>${place.title}</h2>
            <div class="price">$${place.price} per night</div>
            <div class="host">Host: ${place.host_name}</div>
            <div class="description">${place.description}</div>
            <h3>Amenities</h3>
            <ul class="amenities-list">
                ${place.amenities.map(amenity => `<li>${amenity}</li>`).join('')}
            </ul>
        </div>
    `;
}

// Task 3: Display reviews
function displayReviews(reviews) {
    const container = document.getElementById('reviews-container');
    if (!container) return;

    if (reviews && reviews.length > 0) {
        container.innerHTML = reviews.map(review => `
            <div class="review-card">
                <div class="review-header">
                    <div class="review-user">${review.user_name}</div>
                    <div class="review-rating">${'⭐'.repeat(review.rating)}</div>
                </div>
                <div class="review-comment">${review.text}</div>
            </div>
        `).join('');
    } else {
        container.innerHTML = '<p>No reviews yet. Be the first to review!</p>';
    }
}

// Task 2: Price filter
function setupPriceFilter(places) {
    const filter = document.getElementById('price-filter');
    if (!filter) return;

    filter.addEventListener('change', function() {
        const maxPrice = this.value ? parseInt(this.value) : null;
        const filtered = maxPrice ? places.filter(place => place.price <= maxPrice) : places;
        displayPlaces(filtered);
    });
}

// Initialize all pages
document.addEventListener('DOMContentLoaded', function() {
    // Mettre à jour l'UI d'authentification sur toutes les pages
    updateAuthUI();
    
    // Task 1: Login page
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const errorDiv = document.getElementById('login-error');

            try {
                // Remplacer par ton API réelle
                const response = await fetch('http://localhost:5001/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    'Accept': 'application/json'
                    // Ajouter le header CORS si nécessaire
                        // 'Access-Control-Allow-Origin': '*'
                    },
                    body: JSON.stringify({ email, password })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    setCookie('token', data.access_token);
                    
                    // Mettre à jour l'UI
                    updateAuthUI();
                    
                    // Rediriger vers la page d'accueil
                    window.location.href = 'index.html';
                } else {
                    const errorData = await response.json();
                    if (errorDiv) {
                        errorDiv.textContent = errorData.message || 'Login failed';
                        errorDiv.style.display = 'block';
                    }
                }
            } catch (error) {
                console.error('Login error:', error);
                // Mode démo - auto login
                setCookie('token', 'demo-token-' + Date.now());
                updateAuthUI();
                window.location.href = 'index.html';
            }
        });
    }

    // Task 2: Index page
    if (window.location.pathname.includes('index.html') || 
        window.location.pathname === '/' || 
        window.location.pathname.endsWith('/')) {
        displayPlaces(sampleData.places);
        setupPriceFilter(sampleData.places);
    }

    // Task 3: Place details page
    if (window.location.pathname.includes('place.html')) {
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('id') || '1';
        
        const place = sampleData.placeDetails[placeId];
        const reviews = sampleData.reviews[placeId];
        
        if (place) {
            displayPlaceDetails(place);
            displayReviews(reviews);
        }
        
        // Afficher/masquer le bouton "Add Review" selon l'authentification
        const addReviewBtn = document.getElementById('add-review-btn');
        if (addReviewBtn) {
            const token = getCookie('token');
            addReviewBtn.style.display = token ? 'block' : 'none';
        }
    }

    // Task 4: Add review page
    if (window.location.pathname.includes('add_review.html')) {
        const token = getCookie('token');
        if (!token) {
            window.location.href = 'index.html';
            return;
        }

        const reviewForm = document.getElementById('review-form');
        const errorDiv = document.getElementById('review-error');
        const successDiv = document.getElementById('review-success');

        if (reviewForm) {
            reviewForm.addEventListener('submit', async function(event) {
                event.preventDefault();
                
                const reviewText = document.getElementById('review').value;
                const rating = document.getElementById('rating').value;

                if (!reviewText || !rating) {
                    if (errorDiv) {
                        errorDiv.textContent = 'Please fill in all fields';
                        errorDiv.style.display = 'block';
                    }
                    return;
                }

                try {
                    // Simuler l'envoi de la review
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    
                    if (successDiv) {
                        successDiv.textContent = 'Review submitted successfully!';
                        successDiv.style.display = 'block';
                        reviewForm.reset();
                    }
                    
                    // Rediriger après 2 secondes
                    setTimeout(() => {
                        const urlParams = new URLSearchParams(window.location.search);
                        const placeId = urlParams.get('placeId');
                        window.location.href = placeId ? `place.html?id=${placeId}` : 'index.html';
                    }, 2000);
                    
                } catch (error) {
                    if (errorDiv) {
                        errorDiv.textContent = 'Failed to submit review. Please try again.';
                        errorDiv.style.display = 'block';
                    }
                }
            });
        }
    }
});