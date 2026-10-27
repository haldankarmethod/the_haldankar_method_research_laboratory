/**
 * THE HALDANKAR METHOD - AMBIENT PROMOTION ENGINE
 * Controlled, non-intrusive author publication announcement.
 * 
 * Rules:
 * 1. 45-Second continuous engagement timer (or 50% scroll depth).
 * 2. 1 display per browser session.
 * 3. 7-Day dismissal cooldown in localStorage.
 * 4. Strict exclusions for deep research, evidence, and legal pages.
 * 5. WAI-ARIA compliant dismissal via close button or Escape key.
 */

(function () {
    'use strict';

    const COOLDOWN_DAYS = 7;
    const COOLDOWN_MS = COOLDOWN_DAYS * 24 * 60 * 60 * 1000;
    const TIMER_DELAY_MS = 45000; // 45 seconds

    const DISMISS_KEY = 'thm_toad_ad_dismissed';
    const SESSION_KEY = 'thm_toad_ad_session';

    // 1. PAGE EXCLUSION FILTER
    function isPageEligible() {
        if (window.THM_PROMO_ELIGIBLE !== undefined) {
            return window.THM_PROMO_ELIGIBLE;
        }
        const path = (window.location.pathname || '').toLowerCase();

        // Strict Exclusions
        if (path.includes('actual-profit') || path.includes('actual_profit')) return false;
        if (path.includes('decision-context-model') || path.includes('adaptivecommunicationmiddlewareapi')) return false;
        if (path.includes('evidence') || path.includes('hdfc-experiment')) return false;
        if (path.includes('legal') || path.includes('privacy-policy') || path.includes('terms-of-service')) return false;
        if (path.includes('the-architecture-of-a-decision')) return false;
        if (path.includes('legacy-routing')) return false;

        // Strict Inclusions (Hub pages only)
        const isHome = path === '/' || path.endsWith('/index.html') || path.endsWith('pages/index.html') || path.endsWith('research_lab/');
        const isResearchHub = path.endsWith('research/index.html') || path.endsWith('research/');
        const isLabHub = path.includes('laboratory');
        const isPubHub = path.includes('publications');

        return isHome || isResearchHub || isLabHub || isPubHub;
    }

    // 2. ROOT PREFIX RESOLVER
    function getRootPrefix() {
        if (window.PAGE_NAV_CONFIG && window.PAGE_NAV_CONFIG.rootPrefix !== undefined) {
            return window.PAGE_NAV_CONFIG.rootPrefix;
        }
        const scripts = document.querySelectorAll('script[src*="promo-engine.js"]');
        if (scripts.length > 0) {
            const src = scripts[scripts.length - 1].getAttribute('src');
            const idx = src.indexOf('components/promo/promo-engine.js');
            if (idx !== -1) {
                const beforeSrc = src.substring(0, idx);
                const srcIdx = beforeSrc.lastIndexOf('src/');
                if (srcIdx !== -1) return beforeSrc.substring(0, srcIdx);
                return beforeSrc;
            }
        }
        return './';
    }

    // 3. PERSISTENCE CHECK
    function isSuppressed() {
        try {
            if (sessionStorage.getItem(SESSION_KEY)) return true;
            const dismissedTime = localStorage.getItem(DISMISS_KEY);
            if (dismissedTime && (Date.now() - parseInt(dismissedTime, 10)) < COOLDOWN_MS) {
                return true;
            }
        } catch (e) {
            // In case of private browsing storage restrictions
        }
        return false;
    }

    // 4. DISMISSAL HANDLER
    function dismissCapsule(capsule) {
        if (!capsule) return;
        capsule.classList.remove('thm-promo--visible');
        try {
            localStorage.setItem(DISMISS_KEY, Date.now().toString());
        } catch (e) {}
        setTimeout(() => {
            if (capsule.parentNode) {
                capsule.parentNode.removeChild(capsule);
            }
        }, 400);
    }

    // 5. RENDER CAPSULE
    function renderCapsule() {
        if (isSuppressed()) return;

        let bookUrl, thumbUrl;
        if (window.THM_PROMO_CONFIG && window.THM_PROMO_CONFIG.bookUrl && window.THM_PROMO_CONFIG.thumbUrl) {
            bookUrl = window.THM_PROMO_CONFIG.bookUrl;
            thumbUrl = window.THM_PROMO_CONFIG.thumbUrl;
        } else {
            const root = getRootPrefix();
            bookUrl = `${root}books/the-architecture-of-a-decision/index.html`;
            thumbUrl = `${root}assets/images/books/the-architecture-of-a-decision-cover.png`;
        }

        const capsule = document.createElement('aside');
        capsule.className = 'thm-promo-capsule';
        capsule.setAttribute('role', 'region');
        capsule.setAttribute('aria-label', 'New Author Publication Announcement');

        capsule.innerHTML = `
            <div class="thm-promo-header">
                <span class="thm-promo-eyebrow">New Author Publication</span>
                <button type="button" class="thm-promo-close" aria-label="Dismiss announcement">&times;</button>
            </div>
            <div class="thm-promo-body">
                <img src="${thumbUrl}" alt="The Architecture of a Decision cover thumbnail" class="thm-promo-thumb" width="64" height="91" loading="lazy">
                <div class="thm-promo-content">
                    <h3 class="thm-promo-title">The Architecture of a Decision</h3>
                    <p class="thm-promo-desc">A framework for pre-emptive problem solving and consequence architecture by Suraj Rohit Haldankar.</p>
                    <div class="thm-promo-action">
                        <a href="${bookUrl}" class="thm-promo-btn">Investigate Publication &rarr;</a>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(capsule);

        // Record session display
        try {
            sessionStorage.setItem(SESSION_KEY, 'true');
        } catch (e) {}

        // Animate in
        requestAnimationFrame(() => {
            capsule.classList.add('thm-promo--visible');
        });

        // Event Listeners
        const closeBtn = capsule.querySelector('.thm-promo-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => dismissCapsule(capsule));
        }

        const handleKeydown = (e) => {
            if (e.key === 'Escape') {
                dismissCapsule(capsule);
                document.removeEventListener('keydown', handleKeydown);
            }
        };
        document.addEventListener('keydown', handleKeydown);
    }

    // 6. INITIALIZATION & TIMING
    function initPromoEngine() {
        if (!isPageEligible() || isSuppressed()) return;

        let triggered = false;
        const trigger = () => {
            if (triggered) return;
            triggered = true;
            renderCapsule();
        };

        // 45-Second Engagement Timer
        const timer = setTimeout(trigger, TIMER_DELAY_MS);

        // Optional 50% scroll depth trigger
        const handleScroll = () => {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            if (scrollHeight > 0 && (scrollTop / scrollHeight) >= 0.5) {
                clearTimeout(timer);
                window.removeEventListener('scroll', handleScroll);
                trigger();
            }
        };
        window.addEventListener('scroll', handleScroll, { passive: true });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initPromoEngine);
    } else {
        initPromoEngine();
    }
})();
