/**
 * HDFC BANK CONTROLLED EXPERIMENT — CLIENT INTERACTION SCRIPT
 * Manages institutional mandate matrix switching.
 */

document.addEventListener('DOMContentLoaded', () => {
    initMandateTabs();
});

function initMandateTabs() {
    const tabButtons = document.querySelectorAll('.mandate-tab-btn');
    const tabPanels = document.querySelectorAll('.mandate-panel');

    if (!tabButtons.length || !tabPanels.length) return;

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-mandate-target');

            tabButtons.forEach(b => b.classList.remove('is-active'));
            tabPanels.forEach(p => p.classList.remove('is-active'));

            btn.classList.add('is-active');
            const targetPanel = document.getElementById(targetId);
            if (targetPanel) {
                targetPanel.classList.add('is-active');
            }
        });
    });
}
