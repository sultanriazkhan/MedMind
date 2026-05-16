// static/js/main.js
// Main JavaScript file for Healthcare AI App

// Global Variables
window.healthApp = window.healthApp || {};

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('HealthAI App Initialized');
    
    // Initialize all components
    initTooltips();
    initModals();
    initAccordions();
    initTabs();
    initDropdowns();
    initFormValidation();
    initScrollAnimations();
    initLazyLoading();
    initSmoothScroll();
    
    // Set current year in footers
    setCurrentYear();
});

// Initialize Tooltips
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.classList.add('tooltip');
    });
}

// Initialize Modals
function initModals() {
    const modals = document.querySelectorAll('.modal');
    const triggers = document.querySelectorAll('[data-modal-trigger]');
    const closes = document.querySelectorAll('[data-modal-close]');
    
    triggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            const modalId = trigger.getAttribute('data-modal-trigger');
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        });
    });
    
    closes.forEach(close => {
        close.addEventListener('click', () => {
            const modal = close.closest('.modal');
            if (modal) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });
    
    // Close modal on backdrop click
    modals.forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });
}

// Initialize Accordions
function initAccordions() {
    const accordions = document.querySelectorAll('.accordion');
    
    accordions.forEach(accordion => {
        const headers = accordion.querySelectorAll('.accordion-header');
        
        headers.forEach(header => {
            header.addEventListener('click', () => {
                const content = header.nextElementSibling;
                const isActive = content.classList.contains('active');
                
                // Close all sections in this accordion
                if (!isActive) {
                    headers.forEach(h => {
                        const c = h.nextElementSibling;
                        c.classList.remove('active');
                    });
                }
                
                content.classList.toggle('active');
            });
        });
    });
}

// Initialize Tabs
function initTabs() {
    const tabs = document.querySelectorAll('.tabs');
    
    tabs.forEach(tabContainer => {
        const tabButtons = tabContainer.querySelectorAll('.tab');
        const tabPanes = document.querySelectorAll(tabContainer.getAttribute('data-target') || '.tab-pane');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const tabId = button.getAttribute('data-tab');
                
                // Update active states
                tabButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                
                // Show active pane
                tabPanes.forEach(pane => {
                    pane.classList.remove('active');
                    if (pane.id === tabId) {
                        pane.classList.add('active');
                    }
                });
            });
        });
    });
}

// Initialize Dropdowns
function initDropdowns() {
    const dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(dropdown => {
        const trigger = dropdown.querySelector('.dropdown-trigger');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        if (trigger && menu) {
            trigger.addEventListener('click', (e) => {
                e.stopPropagation();
                menu.classList.toggle('active');
            });
            
            // Close on click outside
            document.addEventListener('click', (e) => {
                if (!dropdown.contains(e.target)) {
                    menu.classList.remove('active');
                }
            });
        }
    });
}

// Initialize Form Validation
function initFormValidation() {
    const forms = document.querySelectorAll('[data-validate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            let isValid = true;
            const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    showInputError(input, 'This field is required');
                } else {
                    clearInputError(input);
                }
                
                // Email validation
                if (input.type === 'email' && input.value.trim()) {
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailRegex.test(input.value)) {
                        isValid = false;
                        showInputError(input, 'Please enter a valid email address');
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showToast('Please fix the errors in the form', 'error');
            }
        });
    });
}

// Show Input Error
function showInputError(input, message) {
    input.classList.add('error');
    const errorDiv = input.parentElement.querySelector('.error-message');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.classList.add('active');
    } else {
        const div = document.createElement('div');
        div.className = 'error-message text-danger text-xs mt-1';
        div.textContent = message;
        input.parentElement.appendChild(div);
    }
}

// Clear Input Error
function clearInputError(input) {
    input.classList.remove('error');
    const errorDiv = input.parentElement.querySelector('.error-message');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Initialize Scroll Animations
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('[data-animate]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const animation = entry.target.getAttribute('data-animate');
                entry.target.classList.add(`animate-${animation}`);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    animatedElements.forEach(el => observer.observe(el));
}

// Initialize Lazy Loading
function initLazyLoading() {
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => imageObserver.observe(img));
}

// Initialize Smooth Scroll
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]:not([href="#"])');
    
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            const target = document.querySelector(link.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Set Current Year
function setCurrentYear() {
    const yearElements = document.querySelectorAll('[data-year]');
    const currentYear = new Date().getFullYear();
    
    yearElements.forEach(el => {
        el.textContent = currentYear;
    });
}

// Copy to Clipboard
window.copyToClipboard = function(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(() => {
        showToast('Failed to copy', 'error');
    });
};

// Debounce Function
window.debounce = function(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

// Throttle Function
window.throttle = function(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
};