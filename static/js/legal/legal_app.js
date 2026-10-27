/**
 * THE HALDANKAR METHOD — Privacy Policy Scripts
 */

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        initTheme();
        initScrollProgress();
    });

    function initTheme() {
        const themeBtn = document.getElementById('theme-toggle-btn');
        const themeIcon = document.getElementById('theme-toggle-icon');
        const html = document.documentElement;

        const savedTheme = localStorage.getItem('haldankar_theme_v2') || 'light';
        applyTheme(savedTheme);

        if (themeBtn) {
            themeBtn.addEventListener('click', () => {
                const currentTheme = html.getAttribute('data-theme') || 'light';
                const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
                applyTheme(nextTheme);
                localStorage.setItem('haldankar_theme_v2', nextTheme);
            });
        }

        function applyTheme(theme) {
            if (theme === 'dark') {
                html.setAttribute('data-theme', 'dark');
                if (themeIcon) themeIcon.textContent = '☀️';
            } else {
                html.removeAttribute('data-theme');
                if (themeIcon) themeIcon.textContent = '🌙';
            }
        }
    }

    function initScrollProgress() {
        const bar = document.getElementById('scroll-progress');
        if (!bar) return;

        window.addEventListener('scroll', () => {
            const scrollTop = window.scrollY || document.documentElement.scrollTop;
            const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const progress = (scrollTop / (docHeight || 1)) * 100;
            bar.style.width = Math.min(100, Math.max(0, progress)) + '%';
        }, { passive: true });
    }
})();
