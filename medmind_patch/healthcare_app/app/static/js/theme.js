// static/js/theme.js
// Theme Management JavaScript

// Theme Configuration
const ThemeConfig = {
    light: {
        primary: '#3b82f6',
        background: '#ffffff',
        text: '#111827',
        card: '#f9fafb'
    },
    dark: {
        primary: '#60a5fa',
        background: '#111827',
        text: '#f9fafb',
        card: '#1f2937'
    }
};

// Theme Manager Class
class ThemeManager {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'light';
        this.init();
    }
    
    init() {
        this.applyTheme(this.theme);
        this.setupThemeToggle();
        this.setupSystemThemeListener();
    }
    
    applyTheme(theme) {
        const htmlElement = document.documentElement;
        htmlElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        this.theme = theme;
        
        // Update theme toggle button icon
        this.updateThemeIcon(theme);
        
        // Dispatch custom event
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
    }
    
    toggle() {
        const newTheme = this.theme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
        
        // Show toast notification
        if (window.showToast) {
            window.showToast(`${newTheme.charAt(0).toUpperCase() + newTheme.slice(1)} mode activated`, 'success');
        }
    }
    
    updateThemeIcon(theme) {
        const themeToggle = document.getElementById('theme-toggle');
        if (!themeToggle) return;
        
        const sunIcon = themeToggle.querySelector('.bi-sun-fill');
        const moonIcon = themeToggle.querySelector('.bi-moon-stars-fill');
        
        if (theme === 'light') {
            if (sunIcon) sunIcon.classList.remove('hidden');
            if (moonIcon) moonIcon.classList.add('hidden');
        } else {
            if (sunIcon) sunIcon.classList.add('hidden');
            if (moonIcon) moonIcon.classList.remove('hidden');
        }
    }
    
    setupThemeToggle() {
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggle());
        }
    }
    
    setupSystemThemeListener() {
        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            const systemTheme = e.matches ? 'dark' : 'light';
            const userPreference = localStorage.getItem('theme');
            
            // Only apply system theme if user hasn't manually set a preference
            if (!userPreference) {
                this.applyTheme(systemTheme);
            }
        });
    }
    
    getCurrentTheme() {
        return this.theme;
    }
    
    isDarkMode() {
        return this.theme === 'dark';
    }
    
    isLightMode() {
        return this.theme === 'light';
    }
}

// Initialize theme manager when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
});

// Apply theme based on system preference
function getSystemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

// Set theme with animation
function setThemeWithAnimation(theme) {
    const htmlElement = document.documentElement;
    const oldTheme = htmlElement.getAttribute('data-theme');
    
    if (oldTheme === theme) return;
    
    // Add transition class for smooth theme change
    document.body.classList.add('theme-transition');
    
    htmlElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    
    setTimeout(() => {
        document.body.classList.remove('theme-transition');
    }, 300);
}

// Export for global use
window.ThemeManager = ThemeManager;
window.getSystemTheme = getSystemTheme;
window.setThemeWithAnimation = setThemeWithAnimation;