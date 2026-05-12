// static/js/animations.js
// Animation JavaScript for Healthcare AI App

// GSAP Animations (if GSAP is loaded)
if (typeof gsap !== 'undefined') {
    // Register ScrollTrigger plugin if available
    if (typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);
    }
    
    // Page transition animations
    function initPageTransitions() {
        const mainContent = document.querySelector('main');
        if (mainContent) {
            gsap.fromTo(mainContent, 
                { opacity: 0, y: 20 },
                { opacity: 1, y: 0, duration: 0.6, ease: 'power2.out' }
            );
        }
    }
    
    // Hero section animations
    function initHeroAnimations() {
        const heroTitle = document.querySelector('.hero-title');
        const heroSubtitle = document.querySelector('.hero-subtitle');
        const heroCTA = document.querySelector('.hero-cta');
        
        if (heroTitle) {
            gsap.fromTo(heroTitle, 
                { opacity: 0, y: 30 },
                { opacity: 1, y: 0, duration: 0.8, delay: 0.2 }
            );
        }
        
        if (heroSubtitle) {
            gsap.fromTo(heroSubtitle,
                { opacity: 0, y: 30 },
                { opacity: 1, y: 0, duration: 0.8, delay: 0.4 }
            );
        }
        
        if (heroCTA) {
            gsap.fromTo(heroCTA,
                { opacity: 0, y: 30 },
                { opacity: 1, y: 0, duration: 0.8, delay: 0.6 }
            );
        }
    }
    
    // Card stagger animations
    function initCardStagger() {
        const cards = document.querySelectorAll('.card-stagger');
        
        if (cards.length) {
            gsap.fromTo(cards,
                { opacity: 0, y: 30 },
                {
                    opacity: 1,
                    y: 0,
                    duration: 0.6,
                    stagger: 0.1,
                    scrollTrigger: {
                        trigger: cards[0].parentElement,
                        start: 'top 80%',
                        toggleActions: 'play none none reverse'
                    }
                }
            );
        }
    }
    
    // Number counter animation
    function initNumberCounters() {
        const counters = document.querySelectorAll('.counter');
        
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-target') || counter.textContent);
            const duration = 2000;
            const increment = target / (duration / 16);
            let current = 0;
            
            ScrollTrigger.create({
                trigger: counter,
                start: 'top 80%',
                onEnter: () => {
                    const interval = setInterval(() => {
                        current += increment;
                        if (current >= target) {
                            counter.textContent = target;
                            clearInterval(interval);
                        } else {
                            counter.textContent = Math.floor(current);
                        }
                    }, 16);
                },
                once: true
            });
        });
    }
    
    // Parallax effect
    function initParallax() {
        const parallaxElements = document.querySelectorAll('[data-parallax]');
        
        parallaxElements.forEach(el => {
            const speed = parseFloat(el.getAttribute('data-parallax')) || 0.5;
            
            gsap.to(el, {
                y: () => window.innerHeight * speed,
                ease: 'none',
                scrollTrigger: {
                    trigger: el,
                    start: 'top bottom',
                    end: 'bottom top',
                    scrub: true
                }
            });
        });
    }
    
    // Fade in on scroll
    function initFadeInScroll() {
        const fadeElements = document.querySelectorAll('[data-fade-in]');
        
        fadeElements.forEach(el => {
            gsap.fromTo(el,
                { opacity: 0, y: 20 },
                {
                    opacity: 1,
                    y: 0,
                    duration: 0.8,
                    scrollTrigger: {
                        trigger: el,
                        start: 'top 85%',
                        toggleActions: 'play none none reverse'
                    }
                }
            );
        });
    }
    
    // Initialize all GSAP animations
    document.addEventListener('DOMContentLoaded', () => {
        initPageTransitions();
        initHeroAnimations();
        initCardStagger();
        initNumberCounters();
        initParallax();
        initFadeInScroll();
    });
}

// Fallback CSS animations if GSAP is not available
function initCSSAnimations() {
    // Add animation classes to elements
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

// Hover animations
function initHoverAnimations() {
    const hoverElements = document.querySelectorAll('[data-hover]');
    
    hoverElements.forEach(el => {
        const animation = el.getAttribute('data-hover');
        
        el.addEventListener('mouseenter', () => {
            el.classList.add(`hover-${animation}`);
        });
        
        el.addEventListener('mouseleave', () => {
            el.classList.remove(`hover-${animation}`);
        });
    });
}

// Loading animation
function showLoadingAnimation() {
    const loader = document.getElementById('global-loader');
    if (loader) {
        loader.classList.add('active');
    }
}

function hideLoadingAnimation() {
    const loader = document.getElementById('global-loader');
    if (loader) {
        loader.classList.remove('active');
    }
}

// Skeleton loading animation
function showSkeletonLoader(containerId, count = 3) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = '';
    for (let i = 0; i < count; i++) {
        const skeleton = document.createElement('div');
        skeleton.className = 'skeleton-card';
        skeleton.innerHTML = `
            <div class="skeleton skeleton-image"></div>
            <div class="skeleton skeleton-title"></div>
            <div class="skeleton skeleton-text"></div>
            <div class="skeleton skeleton-text"></div>
        `;
        container.appendChild(skeleton);
    }
}

function hideSkeletonLoader(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = '';
    }
}

// Confetti animation for achievements
function showConfetti() {
    if (typeof confetti !== 'undefined') {
        confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 }
        });
    }
}

// Ripple effect for buttons
function initRippleEffect() {
    const buttons = document.querySelectorAll('.btn-ripple');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const x = e.clientX - e.target.offsetLeft;
            const y = e.clientY - e.target.offsetTop;
            
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// Export functions
window.showLoadingAnimation = showLoadingAnimation;
window.hideLoadingAnimation = hideLoadingAnimation;
window.showSkeletonLoader = showSkeletonLoader;
window.hideSkeletonLoader = hideSkeletonLoader;
window.showConfetti = showConfetti;

// Initialize animations on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    initCSSAnimations();
    initHoverAnimations();
    initRippleEffect();
});