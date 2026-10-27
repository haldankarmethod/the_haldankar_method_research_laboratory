// Minimal nav mobile toggle — replaces nav.js mobile interaction section
(function () {
    'use strict';
    document.addEventListener('DOMContentLoaded', function () {
        const toggle = document.getElementById('mobile-toggle-btn');
        const nav = document.getElementById('header-nav');
        if (!toggle || !nav) return;

        toggle.addEventListener('click', function (e) {
            e.stopPropagation();
            const isOpen = nav.classList.contains('open');
            nav.classList.toggle('open', !isOpen);
            toggle.setAttribute('aria-expanded', String(!isOpen));
            toggle.textContent = isOpen ? '☰' : '✕';
        });

        // Dropdown toggle functionality for mobile and keyboard
        const dropdownContainer = document.getElementById('research-dropdown-container');
        const dropdownBtn = document.getElementById('research-dropdown-btn');

        if (dropdownContainer && dropdownBtn) {
            dropdownBtn.addEventListener('click', function (e) {
                e.stopPropagation();
                const isOpen = dropdownContainer.classList.contains('is-open');
                dropdownContainer.classList.toggle('is-open', !isOpen);
                dropdownBtn.setAttribute('aria-expanded', String(!isOpen));
            });
        }

        nav.querySelectorAll('.nav-link, .dropdown-link').forEach(function (link) {
            link.addEventListener('click', function () {
                nav.classList.remove('open');
                if (dropdownContainer) dropdownContainer.classList.remove('is-open');
                toggle.setAttribute('aria-expanded', 'false');
                toggle.textContent = '☰';
            });
        });

        document.addEventListener('click', function (e) {
            const header = document.getElementById('site-header');
            if (header && !header.contains(e.target)) {
                if (nav.classList.contains('open')) {
                    nav.classList.remove('open');
                    toggle.setAttribute('aria-expanded', 'false');
                    toggle.textContent = '☰';
                }
                if (dropdownContainer && dropdownContainer.classList.contains('is-open')) {
                    dropdownContainer.classList.remove('is-open');
                    if (dropdownBtn) dropdownBtn.setAttribute('aria-expanded', 'false');
                }
            }
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                if (dropdownContainer && dropdownContainer.classList.contains('is-open')) {
                    dropdownContainer.classList.remove('is-open');
                    if (dropdownBtn) dropdownBtn.setAttribute('aria-expanded', 'false');
                }
            }
        });

        // Contextual nav actions (open-toc)
        document.querySelectorAll('[data-action]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                const action = btn.getAttribute('data-action');
                if (action === 'open-toc') {
                    const overlay = document.getElementById('tocOverlay');
                    const drawer = document.getElementById('tocDrawer');
                    const closeBtn = document.getElementById('tocCloseBtn');
                    if (overlay && drawer) {
                        overlay.classList.add('is-active');
                        drawer.classList.add('is-active');
                        document.body.style.overflow = 'hidden';
                        if (closeBtn) closeBtn.focus();
                    }
                }
                window.dispatchEvent(new CustomEvent('nav-action', { detail: { action: action, target: btn } }));
            });
        });
    });
})();
