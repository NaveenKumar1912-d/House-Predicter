/**
 * House Price Predictor — Frontend Logic
 * Connects to Flask API at http://localhost:5000
 */

const API_URL = 'http://localhost:5000/predict';

// DOM Elements
const predictionForm = document.getElementById('predictionForm');
const predictBtn = document.getElementById('predictBtn');
const btnLoader = document.getElementById('btnLoader');
const resultSection = document.getElementById('resultSection');
const errorSection = document.getElementById('errorSection');
const resetBtn = document.getElementById('resetBtn');
const retryBtn = document.getElementById('retryBtn');

// Initialize background particles
function createParticles() {
    const container = document.getElementById('bgParticles');
    const count = 30;
    for (let i = 0; i < count; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 8 + 's';
        particle.style.animationDuration = (6 + Math.random() * 6) + 's';
        particle.style.width = (2 + Math.random() * 3) + 'px';
        particle.style.height = particle.style.width;
        container.appendChild(particle);
    }
}

// Format number as Indian currency
function formatINR(num) {
    if (num >= 10000000) {
        return (num / 10000000).toFixed(2) + ' Cr';
    } else if (num >= 100000) {
        return (num / 100000).toFixed(2) + ' Lakh';
    }
    return num.toLocaleString('en-IN');
}

// Animate number counting up
function animateValue(element, start, end, duration) {
    const startTime = performance.now();
    const range = end - start;

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
        const current = Math.round(start + range * eased);
        element.textContent = formatINR(current);
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    requestAnimationFrame(update);
}

// Set loading state
function setLoading(loading) {
    if (loading) {
        predictBtn.classList.add('loading');
        predictBtn.disabled = true;
    } else {
        predictBtn.classList.remove('loading');
        predictBtn.disabled = false;
    }
}

// Show result
function showResult(data) {
    resultSection.style.display = 'block';
    errorSection.style.display = 'none';

    // Scroll to result
    setTimeout(() => {
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);

    // Animate price
    const priceEl = document.getElementById('priceValue');
    animateValue(priceEl, 0, data.predicted_price, 1500);

    // Price range
    document.getElementById('rangeLow').textContent = '₹' + formatINR(data.price_range.low);
    document.getElementById('rangeHigh').textContent = '₹' + formatINR(data.price_range.high);

    // Animate range bar
    setTimeout(() => {
        document.getElementById('rangeFill').style.width = '80%';
    }, 300);

    // Badge
    const badge = document.getElementById('resultBadge');
    const category = data.category || 'Mid-Range';
    badge.textContent = category;
    badge.className = 'result-badge';
    if (category === 'Affordable') {
        badge.classList.add('affordable');
    } else if (category === 'Mid-Range') {
        badge.classList.add('mid-range');
    } else {
        badge.classList.add('premium');
    }

    // Details
    document.getElementById('confidenceValue').textContent = data.confidence;
    document.getElementById('modelUsed').textContent = data.model_used;
    document.getElementById('currencyValue').textContent = data.currency;
    document.getElementById('categoryValue').textContent = category;
}

// Show error
function showError(message) {
    errorSection.style.display = 'block';
    resultSection.style.display = 'none';
    document.getElementById('errorMessage').textContent = message;
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Form submit handler
predictionForm.addEventListener('submit', async function (e) {
    e.preventDefault();
    setLoading(true);
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';

    const payload = {
        bedrooms: parseInt(document.getElementById('bedrooms').value),
        bathrooms: parseInt(document.getElementById('bathrooms').value),
        sqft: parseInt(document.getElementById('sqft').value),
        year_built: parseInt(document.getElementById('yearBuilt').value),
        floors: parseInt(document.getElementById('floors').value),
        garage: document.getElementById('garage').checked ? 1 : 0,
        pool: document.getElementById('pool').checked ? 1 : 0,
        location: document.getElementById('location').value
    };

    // Client-side validation
    if (payload.bedrooms < 1 || payload.bedrooms > 10) {
        showError('Bedrooms must be between 1 and 10.');
        setLoading(false);
        return;
    }
    if (payload.sqft < 200 || payload.sqft > 10000) {
        showError('Square feet must be between 200 and 10,000.');
        setLoading(false);
        return;
    }
    if (payload.year_built < 1900 || payload.year_built > 2026) {
        showError('Year built must be between 1900 and 2026.');
        setLoading(false);
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || data.details?.join(', ') || 'Prediction failed');
        }

        if (data.status === 'success') {
            showResult(data);
        } else {
            throw new Error(data.error || 'Unknown error occurred');
        }
    } catch (err) {
        if (err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
            showError('Cannot connect to the server. Make sure Flask API is running on http://localhost:5000');
        } else {
            showError(err.message);
        }
    } finally {
        setLoading(false);
    }
});

// Reset button
resetBtn.addEventListener('click', function () {
    resultSection.style.display = 'none';
    document.getElementById('rangeFill').style.width = '0%';
    document.getElementById('predictionForm').scrollIntoView({ behavior: 'smooth', block: 'center' });
});

// Retry button
retryBtn.addEventListener('click', function () {
    errorSection.style.display = 'none';
    document.getElementById('predictionForm').scrollIntoView({ behavior: 'smooth', block: 'center' });
});

// Add hover glow effect on inputs
document.querySelectorAll('.input-wrapper input, .select-wrapper select').forEach(el => {
    el.addEventListener('focus', function () {
        this.closest('.form-group').style.transform = 'translateY(-2px)';
    });
    el.addEventListener('blur', function () {
        this.closest('.form-group').style.transform = 'translateY(0)';
    });
});

// Init
createParticles();
