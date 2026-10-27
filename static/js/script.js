/**
 * THE HALDANKAR METHOD RESEARCH LABORATORY — CORE CLIENT SCRIPTS
 * Clean, lightweight vanilla JavaScript with zero modal dependencies.
 */

document.addEventListener('DOMContentLoaded', () => {
    initReadingProgress();
    initCollabForm();
    initCIRFForm();
});

/* --------------------------------------------------------------------------
   1. READING PROGRESS INDICATOR
   -------------------------------------------------------------------------- */
function initReadingProgress() {
    const progressBar = document.getElementById('scroll-progress') || document.querySelector('.reading-progress-bar');
    if (!progressBar) return;

    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        if (scrollHeight > 0) {
            const progress = (scrollTop / scrollHeight) * 100;
            progressBar.style.width = progress + '%';
        }
    }, { passive: true });
}

/* --------------------------------------------------------------------------
   2. INSTITUTIONAL INQUIRY FORM DISPATCH
   -------------------------------------------------------------------------- */
function initCollabForm() {
    const form = document.getElementById('collab-inquiry-form');
    const feedback = document.getElementById('collab-form-feedback');
    if (!form || !feedback) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;

        const botCheck = form.querySelector('input[name="botcheck"]');
        if (botCheck && botCheck.checked) return;

        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Transmitting Inquiry...';
        feedback.className = 'form-feedback';
        feedback.style.display = 'none';

        try {
            const formData = new FormData(form);

            const response = await fetch('/contact/submit/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json'
                },
                body: formData
            });

            const result = await response.json();

            if (response.ok && result.success) {
                feedback.className = 'form-feedback success';
                feedback.innerHTML = '<strong>Inquiry Transmitted.</strong><br>Thank you for reaching out. Your message has been routed to the research lab.';
                form.reset();
            } else {
                feedback.className = 'form-feedback error';
                feedback.innerHTML = result.message || 'Submission could not be processed. Please email directly at contact@haldankarmethod.com.';
            }
        } catch (err) {
            feedback.className = 'form-feedback error';
            feedback.innerHTML = 'Network transmission error. Please verify your connection or email directly at contact@haldankarmethod.com.';
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
}

/* --------------------------------------------------------------------------
   3. SERVICE 03 — CIRF INQUIRY FORM DISPATCH
   -------------------------------------------------------------------------- */
function initCIRFForm() {
    const form = document.getElementById('cirf-inquiry-form');
    const feedback = document.getElementById('cirf-form-feedback');
    if (!form || !feedback) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = form.querySelector('button[type="submit"]') || document.getElementById('cirf-submit-btn');
        const originalText = submitBtn.innerHTML;

        const honeypot = form.querySelector('input[name="honeypot"]');
        if (honeypot && honeypot.value) return;

        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span>Transmitting CIRF Inquiry...</span>';
        feedback.className = 'cirf-feedback';
        feedback.style.display = 'none';

        try {
            const formData = new FormData(form);

            const response = await fetch('/contact/cirf/submit/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json'
                },
                body: formData
            });

            const result = await response.json();

            if (response.ok && result.success) {
                feedback.className = 'cirf-feedback success';
                feedback.innerHTML = '<strong>CIRF Inquiry Transmitted Successfully.</strong><br>' + (result.message || 'Our research team will review your organizational environment and contact you.');
                form.reset();
            } else {
                feedback.className = 'cirf-feedback error';
                feedback.innerHTML = result.message || 'Submission could not be processed. Please verify inputs or email contact@haldankarmethod.com.';
            }
        } catch (err) {
            feedback.className = 'cirf-feedback error';
            feedback.innerHTML = 'Network transmission error. Please verify your connection or email directly at contact@haldankarmethod.com.';
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
}
