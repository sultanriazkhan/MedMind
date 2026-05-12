// static/js/sidebar.js
// Sidebar Navigation JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initSidebar();
    initMobileSidebar();
    setActiveNavItem();
});

// Initialize Desktop Sidebar
function initSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebarCollapse = document.getElementById('sidebar-collapse');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
        });
    }
    
    if (sidebarCollapse) {
        sidebarCollapse.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
        });
    }
    
    // Restore sidebar state
    const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    if (isCollapsed && sidebar) {
        sidebar.classList.add('collapsed');
    }
    
    // Initialize sidebar submenus
    const submenuTriggers = document.querySelectorAll('.sidebar-submenu-trigger');
    submenuTriggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            const parent = trigger.closest('.sidebar-item');
            parent.classList.toggle('expanded');
        });
    });
}

// Initialize Mobile Sidebar
function initMobileSidebar() {
    const mobileSidebar = document.getElementById('mobile-sidebar');
    const mobileToggle = document.getElementById('mobile-menu-toggle');
    const mobileOverlay = document.getElementById('mobile-overlay');
    const mobileClose = document.getElementById('mobile-menu-close');
    
    if (mobileToggle) {
        mobileToggle.addEventListener('click', openMobileSidebar);
    }
    
    if (mobileClose) {
        mobileClose.addEventListener('click', closeMobileSidebar);
    }
    
    if (mobileOverlay) {
        mobileOverlay.addEventListener('click', closeMobileSidebar);
    }
    
    // Close on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && mobileSidebar && mobileSidebar.classList.contains('active')) {
            closeMobileSidebar();
        }
    });
}

// Open Mobile Sidebar
function openMobileSidebar() {
    const mobileSidebar = document.getElementById('mobile-sidebar');
    const mobileOverlay = document.getElementById('mobile-overlay');
    
    if (mobileSidebar) {
        mobileSidebar.classList.add('active');
        mobileSidebar.style.transform = 'translateX(0)';
        document.body.style.overflow = 'hidden';
    }
    
    if (mobileOverlay) {
        mobileOverlay.classList.add('active');
        mobileOverlay.style.opacity = '1';
        mobileOverlay.style.visibility = 'visible';
    }
}

// Close Mobile Sidebar
function closeMobileSidebar() {
    const mobileSidebar = document.getElementById('mobile-sidebar');
    const mobileOverlay = document.getElementById('mobile-overlay');
    
    if (mobileSidebar) {
        mobileSidebar.classList.remove('active');
        mobileSidebar.style.transform = 'translateX(-100%)';
        document.body.style.overflow = '';
    }
    
    if (mobileOverlay) {
        mobileOverlay.classList.remove('active');
        mobileOverlay.style.opacity = '0';
        mobileOverlay.style.visibility = 'hidden';
    }
}

// Set Active Navigation Item
function setActiveNavItem() {
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.sidebar-nav a, .mobile-nav a');
    
    navItems.forEach(item => {
        const href = item.getAttribute('href');
        if (href && currentPath === href) {
            item.classList.add('active');
            
            // Expand parent submenu if exists
            const parent = item.closest('.sidebar-submenu');
            if (parent) {
                parent.classList.add('expanded');
            }
        }
    });
}

// Toggle Sidebar Submenu
window.toggleSubmenu = function(element) {
    const parent = element.closest('.sidebar-item');
    parent.classList.toggle('expanded');
};

// Sidebar State Management
class SidebarManager {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.isCollapsed = false;
    }
    
    toggle() {
        this.isCollapsed = !this.isCollapsed;
        if (this.sidebar) {
            this.sidebar.classList.toggle('collapsed', this.isCollapsed);
            localStorage.setItem('sidebarCollapsed', this.isCollapsed);
        }
    }
    
    expand() {
        this.isCollapsed = false;
        if (this.sidebar) {
            this.sidebar.classList.remove('collapsed');
            localStorage.setItem('sidebarCollapsed', false);
        }
    }
    
    collapse() {
        this.isCollapsed = true;
        if (this.sidebar) {
            this.sidebar.classList.add('collapsed');
            localStorage.setItem('sidebarCollapsed', true);
        }
    }
}

// Export for global use
window.SidebarManager = SidebarManager;
window.openMobileSidebar = openMobileSidebar;
window.closeMobileSidebar = closeMobileSidebar;
window.toggleSubmenu = toggleSubmenu;