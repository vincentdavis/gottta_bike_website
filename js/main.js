// GOTTA.BIKE site JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // Close mobile nav on link click
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navCollapse = document.querySelector('.navbar-collapse');

    navLinks.forEach(function (link) {
        link.addEventListener('click', function () {
            if (navCollapse && navCollapse.classList.contains('show')) {
                navCollapse.classList.remove('show');
            }
        });
    });

    // Navbar background change on scroll
    const navbar = document.querySelector('.site-nav');
    function updateNav() {
        if (navbar) {
            navbar.classList.toggle('is-scrolled', window.scrollY > 40);
        }
    }
    updateNav();
    window.addEventListener('scroll', updateNav, { passive: true });

    // Reveal elements as they scroll into view
    const revealEls = document.querySelectorAll('.reveal');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!('IntersectionObserver' in window) || reducedMotion) {
        revealEls.forEach(function (el) {
            el.classList.add('is-visible');
        });
    } else {
        const observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
        );
        revealEls.forEach(function (el) {
            observer.observe(el);
        });
    }
});
