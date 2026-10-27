/**
 * ACTUAL PROFIT — DIGITAL RESEARCH SERIES CLIENT SCRIPT
 * Manages Table of Contents slide-out drawer, scroll spy, and interactive diagrams.
 */

document.addEventListener('DOMContentLoaded', () => {
    initTocDrawer();
    initReadingProgressBar();
    initYAxisToggle();
});

/* --------------------------------------------------------------------------
   1. TABLE OF CONTENTS DRAWER
   -------------------------------------------------------------------------- */
function initTocDrawer() {
    const overlay = document.getElementById('tocOverlay');
    const drawer = document.getElementById('tocDrawer');
    const closeBtn = document.getElementById('tocCloseBtn');

    function closeDrawer() {
        if (overlay) overlay.classList.remove('is-active');
        if (drawer) drawer.classList.remove('is-active');
        document.body.style.overflow = '';
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', closeDrawer);
    }

    if (overlay) {
        overlay.addEventListener('click', closeDrawer);
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && drawer && drawer.classList.contains('is-active')) {
            closeDrawer();
        }
    });
}

/* --------------------------------------------------------------------------
   2. READING PROGRESS BAR
   -------------------------------------------------------------------------- */
function initReadingProgressBar() {
    const bar = document.querySelector('.reading-progress-bar') || document.getElementById('scroll-progress');
    if (!bar) return;

    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        if (scrollHeight > 0) {
            const progress = (scrollTop / scrollHeight) * 100;
            bar.style.width = progress + '%';
        }
    }, { passive: true });
}

/* --------------------------------------------------------------------------
   3. Y-AXIS DISTORTION INTERACTIVE TOGGLE (CHAPTER 05)
   -------------------------------------------------------------------------- */
function initYAxisToggle() {
    const toggleBtns = document.querySelectorAll('[data-yaxis-scale]');
    const previewBox = document.getElementById('yaxis-preview-box');
    if (!toggleBtns.length || !previewBox) return;

    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const scale = btn.getAttribute('data-yaxis-scale');
            toggleBtns.forEach(b => b.classList.remove('btn-gold'));
            btn.classList.add('btn-gold');

            if (scale === 'dynamic') {
                previewBox.setAttribute('data-mode', 'dynamic');
                const label = document.getElementById('yaxis-scale-label');
                if (label) label.textContent = 'Auto-Scaled Y-Axis (0.5% move rendered with 45° slope exaggeration)';
            } else {
                previewBox.setAttribute('data-mode', 'isometric');
                const label = document.getElementById('yaxis-scale-label');
                if (label) label.textContent = 'True Isometric Proportional Scale (0.5% move rendered with accurate 4.5° true slope)';
            }
        });
    });
}
