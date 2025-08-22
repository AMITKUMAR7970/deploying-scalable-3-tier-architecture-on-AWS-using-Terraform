// DevOps 3-Tier Application JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initTabNavigation();
    initEnvironmentTabs();
    initModuleTabs();
    initCopyButtons();
    initFileTreeToggle();
    
    // Initialize syntax highlighting
    if (typeof Prism !== 'undefined') {
        Prism.highlightAll();
    }
});

// Main tab navigation functionality
function initTabNavigation() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    console.log('Found tab buttons:', tabBtns.length);
    console.log('Found tab contents:', tabContents.length);
    
    tabBtns.forEach((btn, index) => {
        console.log(`Tab button ${index}:`, btn.getAttribute('data-tab'));
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const targetTab = btn.getAttribute('data-tab');
            console.log('Clicked tab:', targetTab);
            
            // Remove active class from all buttons and contents
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            btn.classList.add('active');
            const targetContent = document.getElementById(targetTab);
            console.log('Target content element:', targetContent);
            
            if (targetContent) {
                targetContent.classList.add('active');
                // Scroll to top of content
                targetContent.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            } else {
                console.error('Target content not found for tab:', targetTab);
            }
        });
    });
}

// Environment tabs (dev, staging, prod) functionality
function initEnvironmentTabs() {
    const envTabs = document.querySelectorAll('.env-tab');
    const envContents = document.querySelectorAll('.env-content');
    
    envTabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            const targetEnv = tab.getAttribute('data-env');
            
            // Remove active class from all env tabs and contents
            envTabs.forEach(t => t.classList.remove('active'));
            envContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            tab.classList.add('active');
            const targetContent = document.getElementById(`env-${targetEnv}`);
            if (targetContent) {
                targetContent.classList.add('active');
                // Re-highlight syntax for newly shown content
                if (typeof Prism !== 'undefined') {
                    Prism.highlightAllUnder(targetContent);
                }
            }
        });
    });
}

// Module tabs functionality
function initModuleTabs() {
    const moduleTabs = document.querySelectorAll('.module-tab');
    const moduleSections = document.querySelectorAll('.module-section');
    
    moduleTabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            const targetModule = tab.getAttribute('data-module');
            
            // Remove active class from all module tabs and sections
            moduleTabs.forEach(t => t.classList.remove('active'));
            moduleSections.forEach(section => section.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding section
            tab.classList.add('active');
            const targetSection = document.getElementById(`module-${targetModule}`);
            if (targetSection) {
                targetSection.classList.add('active');
                // Re-highlight syntax for newly shown content
                if (typeof Prism !== 'undefined') {
                    Prism.highlightAllUnder(targetSection);
                }
            }
        });
    });
}

// Copy to clipboard functionality
function initCopyButtons() {
    const copyBtns = document.querySelectorAll('.copy-btn');
    
    copyBtns.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const targetId = btn.getAttribute('data-copy');
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                try {
                    const textToCopy = targetElement.textContent;
                    
                    // Use different methods for copying based on browser support
                    if (navigator.clipboard && window.isSecureContext) {
                        await navigator.clipboard.writeText(textToCopy);
                    } else {
                        // Fallback for older browsers
                        const textArea = document.createElement('textarea');
                        textArea.value = textToCopy;
                        textArea.style.position = 'fixed';
                        textArea.style.left = '-999999px';
                        textArea.style.top = '-999999px';
                        document.body.appendChild(textArea);
                        textArea.focus();
                        textArea.select();
                        document.execCommand('copy');
                        textArea.remove();
                    }
                    
                    // Show success feedback
                    showCopyNotification('Code copied to clipboard!');
                    
                    // Change button icon temporarily
                    const originalIcon = btn.innerHTML;
                    btn.innerHTML = '<i class="fas fa-check"></i>';
                    btn.style.background = 'var(--color-success)';
                    btn.style.color = 'var(--color-btn-primary-text)';
                    
                    setTimeout(() => {
                        btn.innerHTML = originalIcon;
                        btn.style.background = '';
                        btn.style.color = '';
                    }, 1500);
                    
                } catch (err) {
                    console.error('Failed to copy text: ', err);
                    showCopyNotification('Failed to copy code', 'error');
                }
            }
        });
    });
}

// Show copy notification
function showCopyNotification(message, type = 'success') {
    // Remove existing notification if any
    const existing = document.querySelector('.copy-notification');
    if (existing) {
        existing.remove();
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'copy-notification';
    notification.textContent = message;
    
    if (type === 'error') {
        notification.style.background = 'var(--color-error)';
    }
    
    // Add to document
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Hide and remove notification
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// File tree toggle functionality
function initFileTreeToggle() {
    const folderNodes = document.querySelectorAll('.tree-node');
    
    folderNodes.forEach(node => {
        const icon = node.querySelector('i');
        const children = node.querySelector('.tree-children');
        
        if (children && icon && icon.classList.contains('fa-folder')) {
            // Set initial state - folders are open by default
            children.style.display = 'block';
            
            node.style.cursor = 'pointer';
            node.addEventListener('click', (e) => {
                e.stopPropagation();
                
                if (children.style.display === 'none') {
                    children.style.display = 'block';
                    icon.classList.remove('fa-folder');
                    icon.classList.add('fa-folder-open');
                } else {
                    children.style.display = 'none';
                    icon.classList.remove('fa-folder-open');
                    icon.classList.add('fa-folder');
                }
            });
        }
    });
}

// Utility function to add smooth animations to elements
function addSmoothAnimations() {
    // Check if IntersectionObserver is supported
    if (!window.IntersectionObserver) {
        return;
    }
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate in
    const animateElements = document.querySelectorAll('.feature-card, .stat-card, .security-card, .step');
    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Initialize smooth animations when page loads
window.addEventListener('load', () => {
    setTimeout(addSmoothAnimations, 100);
});

// Handle window resize for responsive adjustments
window.addEventListener('resize', debounce(() => {
    // Adjust workflow diagram layout on mobile
    const workflowArrows = document.querySelectorAll('.workflow-arrow');
    
    if (window.innerWidth <= 768) {
        workflowArrows.forEach(arrow => {
            arrow.textContent = '↓';
        });
    } else {
        workflowArrows.forEach(arrow => {
            arrow.textContent = '→';
        });
    }
}, 250));

// Debounce utility function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Progress tracking for deployment steps
function initProgressTracking() {
    const steps = document.querySelectorAll('.step');
    let completedSteps = 0;
    
    steps.forEach((step, index) => {
        step.style.cursor = 'pointer';
        step.addEventListener('click', () => {
            step.classList.toggle('completed');
            
            if (step.classList.contains('completed')) {
                step.querySelector('.step-number').innerHTML = '<i class="fas fa-check"></i>';
                step.querySelector('.step-number').style.background = 'var(--color-success)';
                completedSteps++;
            } else {
                step.querySelector('.step-number').textContent = index + 1;
                step.querySelector('.step-number').style.background = 'var(--color-primary)';
                completedSteps--;
            }
        });
    });
}

// Dark mode toggle functionality
function initThemeToggle() {
    const themeToggle = document.querySelector('.theme-toggle');
    if (!themeToggle) return;
    
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-color-scheme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-color-scheme', newTheme);
        
        // Update toggle icon
        const icon = themeToggle.querySelector('i');
        if (newTheme === 'dark') {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        }
    });
}

// Initialize all enhanced features
document.addEventListener('DOMContentLoaded', () => {
    // Add small delay to ensure all elements are ready
    setTimeout(() => {
        initProgressTracking();
        initThemeToggle();
    }, 100);
});

// Add keyboard support for better accessibility
document.addEventListener('keydown', (e) => {
    // Allow Enter key to activate focused buttons
    if (e.key === 'Enter' && e.target.tagName === 'BUTTON') {
        e.target.click();
    }
    
    // Arrow keys for tab navigation
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        const focusedTab = document.activeElement;
        if (focusedTab.classList.contains('tab-btn')) {
            const tabs = Array.from(document.querySelectorAll('.tab-btn'));
            const currentIndex = tabs.indexOf(focusedTab);
            
            if (e.key === 'ArrowRight') {
                const nextIndex = (currentIndex + 1) % tabs.length;
                tabs[nextIndex].focus();
            } else {
                const prevIndex = currentIndex === 0 ? tabs.length - 1 : currentIndex - 1;
                tabs[prevIndex].focus();
            }
        }
    }
});

// Error handling wrapper
window.addEventListener('error', (e) => {
    console.error('JavaScript error:', e.error);
});

// Ensure all functionality works even if external libraries fail
window.addEventListener('DOMContentLoaded', () => {
    // Fallback if Prism.js fails to load
    if (typeof Prism === 'undefined') {
        console.warn('Prism.js not loaded, syntax highlighting disabled');
    }
});