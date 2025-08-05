// Main JavaScript file for the hotel booking system

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Date validation for search forms
    setupDateValidation();
    
    // Booking form validation
    setupBookingFormValidation();
    
    // Auto-dismiss alerts
    autoHideAlerts();
    
    // Smooth scrolling for anchor links
    setupSmoothScrolling();
});

// Date validation setup
function setupDateValidation() {
    const checkInInputs = document.querySelectorAll('input[name="check_in"]');
    const checkOutInputs = document.querySelectorAll('input[name="check_out"]');
    
    checkInInputs.forEach(checkInInput => {
        checkInInput.addEventListener('change', function() {
            const checkOutInput = this.closest('form').querySelector('input[name="check_out"]');
            if (checkOutInput) {
                const checkInDate = new Date(this.value);
                const nextDay = new Date(checkInDate);
                nextDay.setDate(nextDay.getDate() + 1);
                checkOutInput.min = nextDay.toISOString().split('T')[0];
                
                // Clear checkout if it's invalid
                if (checkOutInput.value && new Date(checkOutInput.value) <= checkInDate) {
                    checkOutInput.value = '';
                }
            }
        });
    });
}

// Booking form validation
function setupBookingFormValidation() {
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            if (!validateBookingForm()) {
                e.preventDefault();
                showAlert('Please correct the errors in the form.', 'danger');
            }
        });
        
        // Real-time price calculation
        const checkInInput = bookingForm.querySelector('input[name="check_in"]');
        const checkOutInput = bookingForm.querySelector('input[name="check_out"]');
        
        if (checkInInput && checkOutInput) {
            checkInInput.addEventListener('change', calculateBookingPrice);
            checkOutInput.addEventListener('change', calculateBookingPrice);
        }
    }
}

// Validate booking form
function validateBookingForm() {
    let isValid = true;
    const form = document.getElementById('bookingForm');
    
    // Check required fields
    const requiredFields = form.querySelectorAll('input[required], select[required]');
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    // Validate email format
    const emailField = form.querySelector('input[type="email"]');
    if (emailField && emailField.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailField.value)) {
            emailField.classList.add('is-invalid');
            isValid = false;
        } else {
            emailField.classList.remove('is-invalid');
        }
    }
    
    // Validate phone format
    const phoneField = form.querySelector('input[type="tel"]');
    if (phoneField && phoneField.value) {
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        if (!phoneRegex.test(phoneField.value.replace(/[\s\-\(\)]/g, ''))) {
            phoneField.classList.add('is-invalid');
            isValid = false;
        } else {
            phoneField.classList.remove('is-invalid');
        }
    }
    
    // Validate dates
    const checkIn = form.querySelector('input[name="check_in"]');
    const checkOut = form.querySelector('input[name="check_out"]');
    
    if (checkIn && checkOut && checkIn.value && checkOut.value) {
        const checkInDate = new Date(checkIn.value);
        const checkOutDate = new Date(checkOut.value);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        if (checkInDate < today) {
            checkIn.classList.add('is-invalid');
            isValid = false;
        } else {
            checkIn.classList.remove('is-invalid');
        }
        
        if (checkOutDate <= checkInDate) {
            checkOut.classList.add('is-invalid');
            isValid = false;
        } else {
            checkOut.classList.remove('is-invalid');
        }
    }
    
    return isValid;
}

// Calculate booking price
function calculateBookingPrice() {
    const form = document.getElementById('bookingForm');
    if (!form) return;
    
    const checkIn = form.querySelector('input[name="check_in"]').value;
    const checkOut = form.querySelector('input[name="check_out"]').value;
    const priceCalculation = document.getElementById('price-calculation');
    const totalPrice = document.getElementById('total-price');
    
    if (checkIn && checkOut && priceCalculation && totalPrice) {
        const checkInDate = new Date(checkIn);
        const checkOutDate = new Date(checkOut);
        const nights = Math.ceil((checkOutDate - checkInDate) / (1000 * 60 * 60 * 24));
        
        // Get base price from the page (this would be injected by the template)
        const basePriceElement = document.querySelector('[data-base-price]');
        const basePrice = basePriceElement ? parseFloat(basePriceElement.dataset.basePrice) : 0;
        
        if (nights > 0 && basePrice > 0) {
            const total = basePrice * nights;
            priceCalculation.textContent = `$${basePrice.toFixed(2)} × ${nights} night${nights > 1 ? 's' : ''}`;
            totalPrice.textContent = `$${total.toFixed(2)}`;
        } else {
            priceCalculation.textContent = 'Invalid date range';
            totalPrice.textContent = '$0.00';
        }
    }
}

// Auto-hide alerts after 5 seconds
function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (!alert.classList.contains('alert-permanent')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });
}

// Setup smooth scrolling for anchor links
function setupSmoothScrolling() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    if (alertContainer) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        alertContainer.insertBefore(alertDiv, alertContainer.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }
}

// Confirmation dialog for actions
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Format date
function formatDate(dateString, options = {}) {
    const defaultOptions = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    
    return new Date(dateString).toLocaleDateString('en-US', { ...defaultOptions, ...options });
}

// Loading state management
function setLoadingState(element, isLoading) {
    if (isLoading) {
        element.classList.add('loading');
        const originalText = element.textContent;
        element.dataset.originalText = originalText;
        element.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
    } else {
        element.classList.remove('loading');
        element.textContent = element.dataset.originalText || element.textContent;
    }
}

// Form submission with loading state
function submitFormWithLoading(form, submitButton) {
    setLoadingState(submitButton, true);
    
    // Re-enable button after form submission
    setTimeout(() => {
        setLoadingState(submitButton, false);
    }, 2000);
}

// Export functions for use in other scripts
window.BookingSystem = {
    showAlert,
    confirmAction,
    formatCurrency,
    formatDate,
    setLoadingState,
    submitFormWithLoading
};
