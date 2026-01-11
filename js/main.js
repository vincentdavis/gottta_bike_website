// Portfolio Site JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Close mobile nav on link click
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navCollapse = document.querySelector('.navbar-collapse');

    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            if (navCollapse.classList.contains('show')) {
                navCollapse.classList.remove('show');
            }
        });
    });

    // Form submission handler (prevents page reload for static site)
    const form = document.querySelector('#contact form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            // Get form values
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const subject = document.getElementById('subject').value;
            const message = document.getElementById('message').value;

            // Basic validation
            if (!name || !email || !message) {
                alert('Please fill in all required fields.');
                return;
            }

            // For a static site, you would typically:
            // 1. Use a service like Formspree, Netlify Forms, or EmailJS
            // 2. Or integrate with a backend API

            alert('Thank you for your message! This is a static site demo. To enable form submission, integrate with a form service.');
            form.reset();
        });
    }

    // Navbar background change on scroll
    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('shadow');
        } else {
            navbar.classList.remove('shadow');
        }
    });
});
