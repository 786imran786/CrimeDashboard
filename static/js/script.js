// Add any interactive functionality here
document.addEventListener('DOMContentLoaded', function() {
    // Add active class to current page link
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.neon-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Form validation for custom analysis
    const customForm = document.getElementById('custom-form');
    if (customForm) {
        customForm.addEventListener('submit', function(e) {
            const plotType = document.getElementById('plot_type').value;
            const yCol = document.getElementById('y_col').value;
            
            if (plotType === 'pie' && yCol) {
                alert('For pie charts, please leave Y-Axis empty');
                e.preventDefault();
                return false;
            }
            
            if (plotType !== 'pie' && !yCol) {
                alert('Please select a Y-Axis column for this plot type');
                e.preventDefault();
                return false;
            }
            
            return true;
        });
    }
});