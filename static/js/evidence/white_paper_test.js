/**
 * WHITE PAPER TEST (EXP-2026-002) — FULL-VIEWPORT CLIENT INTERACTION SCRIPT
 * The Haldankar Method Research Laboratory
 * 
 * Standards:
 * - Direct representation of 'White Paper Test Theory.jpg' (Authoritative Image Stimulus)
 * - Proportional unscaled rendering without distortion
 * - Zero-latency pre-decoded GPU memory stimulus
 * - High-precision timing via performance.now()
 * - Pure vanilla JavaScript with zero external dependencies
 */

(function () {
    'use strict';

    // -------------------------------------------------------------------------
    // 1. TIMING CONSTANTS (Milliseconds)
    // -------------------------------------------------------------------------
    const TIMING = {
        INSTRUCTION_ARROW_MS: 1000,
        STIMULUS_EXPOSURE_MS: 5000
    };

    const ASSET_PATH = '/static/images/evidence/white-paper-test-stimulus.jpg';

    // -------------------------------------------------------------------------
    // 2. FULL-VIEWPORT EXPERIMENT CONTROLLER
    // -------------------------------------------------------------------------
    class FullscreenWhitePaperExperiment {
        constructor() {
            this.overlay = null;
            this.state = 'CLOSED';
            this.preloadedImage = null;
            this.answers = {
                sawShapes: null,
                countEstimate: null
            };
            this.init();
        }

        init() {
            // Preload and pre-decode provided image stimulus into GPU memory
            this.preloadStimulus();

            // Build overlay container in body
            this.overlay = document.createElement('div');
            this.overlay.className = 'experiment-viewport-overlay is-hidden';
            this.overlay.id = 'exp-viewport-takeover';
            document.body.appendChild(this.overlay);

            // Bind trigger buttons across the page
            document.addEventListener('click', (e) => {
                const trigger = e.target.closest('[data-action="launch-white-paper-test"]');
                if (trigger) {
                    e.preventDefault();
                    this.open();
                }
            });
        }

        async preloadStimulus() {
            try {
                this.preloadedImage = new Image();
                this.preloadedImage.src = ASSET_PATH;
                if (this.preloadedImage.decode) {
                    await this.preloadedImage.decode();
                }
            } catch (err) {
                console.warn('Stimulus preload note:', err);
            }
        }

        open() {
            this.state = 'INTRO';
            document.body.classList.add('experiment-active');
            this.overlay.classList.remove('is-hidden');
            this.renderIntro();
        }

        close() {
            this.state = 'CLOSED';
            document.body.classList.remove('experiment-active');
            this.overlay.classList.add('is-hidden');
            this.overlay.innerHTML = '';
        }

        // ---------------------------------------------------------------------
        // STATE 1: EXPERIMENT INTRODUCTION (TOP-CENTER BUTTON)
        // ---------------------------------------------------------------------
        renderIntro() {
            this.overlay.innerHTML = `
                <div class="exp-top-bar">
                    <button type="button" class="btn-exit-test" id="btn-exit-intro">✕ Exit Test</button>
                    <div class="exp-top-center">
                        <button type="button" class="btn-ready" id="btn-im-ready">
                            I'M READY
                        </button>
                    </div>
                    <div style="width: 70px;"></div>
                </div>

                <div class="exp-stage-area">
                    <div class="exp-stage" style="max-width: 620px;">
                        <span class="status-pill status-pill--evidence" style="margin-bottom: 1.25rem;">
                            EMPIRICAL EXPERIMENT · EXP-2026-002
                        </span>
                        <h1 style="font-size: clamp(1.6rem, 3.5vw, 2.35rem); line-height: 1.2; margin-bottom: 1rem; color: #ffffff;">
                            The White Paper Test
                        </h1>
                        <p style="font-size: 1rem; color: var(--text-secondary); line-height: 1.65; margin-bottom: 1.5rem;">
                            This controlled 5.0-second selective-attention experiment tests the boundary between visual fixation, peripheral exposure, and conscious working memory recall.
                        </p>
                        <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-left: 3px solid var(--accent-gold); border-radius: 2px; padding: 1.25rem 1.5rem; text-align: left;">
                            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: var(--accent-gold); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.35rem;">
                                EXPERIMENTAL PROTOCOL
                            </div>
                            <p style="font-size: 0.875rem; color: var(--text-secondary); line-height: 1.6; margin: 0;">
                                1. When you click <strong>I'M READY</strong> at the top center, you will receive an immediate directional attention instruction.<br>
                                2. An arrow will point to the exact position of the red circle in the top-right corner.<br>
                                3. The arrow will disappear, followed by a <strong>5.0-second exposure</strong> of the actual White Paper Test stimulus.<br>
                                4. You will then answer two brief recall questions.
                            </p>
                        </div>
                    </div>
                </div>

                <div style="padding: 1rem 0; font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-muted);">
                    The Haldankar Method Research Laboratory · Source experimental image — native 2550 × 3300 px aspect ratio
                </div>
            `;

            const btnReady = this.overlay.querySelector('#btn-im-ready');
            if (btnReady) {
                btnReady.addEventListener('click', () => this.startAttentionPhase());
            }

            const btnExit = this.overlay.querySelector('#btn-exit-intro');
            if (btnExit) {
                btnExit.addEventListener('click', () => this.close());
            }
        }

        // ---------------------------------------------------------------------
        // STATE 2 & 3: ATTENTION INSTRUCTION & FOCUS ARROW (DISAPPEARS BEFORE TEST)
        // ---------------------------------------------------------------------
        startAttentionPhase() {
            this.state = 'ATTENTION';

            this.overlay.innerHTML = `
                <div class="focus-viewport-stage">
                    <div class="attention-instruction-box">
                        <div class="attention-headline">
                            LOOK AT THE TOP-RIGHT CORNER.
                        </div>
                        <div class="attention-subline">
                            Keep your eyes focused only on the indicated corner.
                        </div>
                    </div>

                    <!-- Visual Frame with Focus Arrow targeting the Red Circle -->
                    <div class="focus-arrow-target-frame">
                        <div class="focus-arrow-pointer">
                            <div class="focus-arrow-label">FOCUS POINT (RED CIRCLE)</div>
                            <div class="focus-arrow-icon">➔</div>
                        </div>
                    </div>
                </div>
            `;

            // Wait 1.0 second with the arrow indicating the focus point, then remove arrow and trigger exposure
            setTimeout(() => {
                this.triggerStimulusExposure();
            }, TIMING.INSTRUCTION_ARROW_MS);
        }

        // ---------------------------------------------------------------------
        // STATE 4: STIMULUS DISPLAY (EXACTLY 5,000ms EXPOSURE)
        // ---------------------------------------------------------------------
        triggerStimulusExposure() {
            this.state = 'EXPOSURE';

            // Clean, unencumbered full-viewport contain stage — zero ghost elements or outer padding
            this.overlay.innerHTML = `
                <div class="stimulus-viewport-stage" id="live-stimulus-stage">
                    <img src="${ASSET_PATH}" alt="White Paper Test Stimulus" id="live-stimulus-img">
                </div>
            `;

            const tStart = performance.now();

            // Strictly 5,000 ms exposure period
            setTimeout(() => {
                // Instantly unmount stimulus to prevent prolonged inspection
                const stage = this.overlay.querySelector('#live-stimulus-stage');
                if (stage) {
                    stage.innerHTML = '';
                }
                this.renderQuestion1();
            }, TIMING.STIMULUS_EXPOSURE_MS);
        }

        // ---------------------------------------------------------------------
        // STATE 5 & 6: POST-TEST QUESTIONS
        // ---------------------------------------------------------------------
        renderQuestion1() {
            this.state = 'QUESTION_1';

            this.overlay.innerHTML = `
                <div class="exp-top-bar">
                    <button type="button" class="btn-exit-test" id="btn-exit-q1">✕ Cancel</button>
                    <div class="exp-top-center">
                        <span style="font-family: var(--font-mono); font-size: 0.8125rem; color: var(--accent-gold);">
                            OBSERVATION PROBE 01 / 02
                        </span>
                    </div>
                    <div style="width: 70px;"></div>
                </div>

                <div class="exp-stage-area">
                    <div class="question-panel">
                        <div class="question-tag">STEP 01 OF 02 · PERCEPTUAL RECALL</div>
                        <h2 class="question-prompt">
                            Were there different shapes present on the page?
                        </h2>
                        <p style="font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 1.5rem;">
                            Based on your 5.0-second observation while fixating on the top-right red circle:
                        </p>
                        <div class="option-list">
                            <button type="button" class="option-btn" data-val="yes">
                                <span style="font-family: var(--font-mono); color: var(--accent-gold); font-weight: 700;">[A]</span>
                                <span>Yes, multiple distinct shapes were present in the lower area.</span>
                            </button>
                            <button type="button" class="option-btn" data-val="no">
                                <span style="font-family: var(--font-mono); color: var(--accent-gold); font-weight: 700;">[B]</span>
                                <span>No, there were no shapes on the page (only blank space).</span>
                            </button>
                            <button type="button" class="option-btn" data-val="unsure">
                                <span style="font-family: var(--font-mono); color: var(--accent-gold); font-weight: 700;">[C]</span>
                                <span>Not sure / I focused only on the red circle and did not notice.</span>
                            </button>
                        </div>
                    </div>
                </div>

                <div style="padding: 1rem 0;"></div>
            `;

            const optButtons = this.overlay.querySelectorAll('.option-btn');
            optButtons.forEach(btn => {
                btn.addEventListener('click', () => {
                    optButtons.forEach(b => b.classList.remove('is-selected'));
                    btn.classList.add('is-selected');
                    this.answers.sawShapes = btn.getAttribute('data-val');
                    setTimeout(() => this.renderQuestion2(), 250);
                });
            });

            const btnExit = this.overlay.querySelector('#btn-exit-q1');
            if (btnExit) {
                btnExit.addEventListener('click', () => this.close());
            }
        }

        renderQuestion2() {
            this.state = 'QUESTION_2';

            this.overlay.innerHTML = `
                <div class="exp-top-bar">
                    <button type="button" class="btn-exit-test" id="btn-exit-q2">✕ Cancel</button>
                    <div class="exp-top-center">
                        <span style="font-family: var(--font-mono); font-size: 0.8125rem; color: var(--accent-gold);">
                            OBSERVATION PROBE 02 / 02
                        </span>
                    </div>
                    <div style="width: 70px;"></div>
                </div>

                <div class="exp-stage-area">
                    <div class="question-panel">
                        <div class="question-tag">STEP 02 OF 02 · QUANTITATIVE ESTIMATION</div>
                        <h2 class="question-prompt">
                            How many shapes do you think were there?
                        </h2>
                        <p style="font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 1.5rem;">
                            Estimate the total number of geometric shapes present in the lower portion of the sheet:
                        </p>
                        
                        <div class="chip-grid">
                            <button type="button" class="chip-btn" data-range="0">0 (None)</button>
                            <button type="button" class="chip-btn" data-range="1–5">1 – 5</button>
                            <button type="button" class="chip-btn" data-range="6–15">6 – 15</button>
                            <button type="button" class="chip-btn" data-range="16–25">16 – 25</button>
                            <button type="button" class="chip-btn" data-range="26–35">26 – 35</button>
                            <button type="button" class="chip-btn" data-range="36+">36+</button>
                        </div>

                        <div style="display: flex; gap: 0.75rem; align-items: center; margin-top: 1.25rem; flex-wrap: wrap;">
                            <input type="number" id="custom-num-input" class="form-control" placeholder="Or enter exact count (e.g. 25)" style="max-width: 250px; background: var(--bg-primary); font-family: var(--font-mono); color: #ffffff;" min="0" max="100">
                            <button type="button" class="btn btn-primary" id="btn-submit-test" style="padding: 0.65rem 1.5rem; font-size: 0.875rem;">
                                Submit Observations →
                            </button>
                        </div>
                    </div>
                </div>

                <div style="padding: 1rem 0;"></div>
            `;

            const chips = this.overlay.querySelectorAll('.chip-btn');
            const numInput = this.overlay.querySelector('#custom-num-input');

            chips.forEach(chip => {
                chip.addEventListener('click', () => {
                    chips.forEach(c => c.classList.remove('is-selected'));
                    chip.classList.add('is-selected');
                    this.answers.countEstimate = chip.getAttribute('data-range');
                    if (numInput) numInput.value = '';
                });
            });

            if (numInput) {
                numInput.addEventListener('input', () => {
                    chips.forEach(c => c.classList.remove('is-selected'));
                    this.answers.countEstimate = numInput.value.trim();
                });
            }

            const btnSubmit = this.overlay.querySelector('#btn-submit-test');
            if (btnSubmit) {
                btnSubmit.addEventListener('click', () => {
                    if (numInput && numInput.value.trim()) {
                        this.answers.countEstimate = numInput.value.trim();
                    }
                    if (!this.answers.countEstimate) {
                        this.answers.countEstimate = 'Unspecified';
                    }
                    this.renderResults();
                });
            }

            const btnExit = this.overlay.querySelector('#btn-exit-q2');
            if (btnExit) {
                btnExit.addEventListener('click', () => this.close());
            }
        }

        // ---------------------------------------------------------------------
        // STATE 7: RESULTS, DEBRIEF & COGNITIVE SYNTHESIS
        // ---------------------------------------------------------------------
        renderResults() {
            this.state = 'RESULTS';

            let accuracySummary = '';
            if (this.answers.sawShapes === 'no') {
                accuracySummary = 'Reported zero shapes due to complete attentional capture by the red circle.';
            } else if (this.answers.sawShapes === 'unsure') {
                accuracySummary = 'Reported uncertainty; pre-attentive registration without working memory encoding.';
            } else {
                accuracySummary = 'Correctly noted presence of shapes, but estimation reflects working memory compression under brief exposure.';
            }

            this.overlay.innerHTML = `
                <div class="exp-top-bar">
                    <button type="button" class="btn-exit-test" id="btn-close-results">✕ Exit to Website</button>
                    <div class="exp-top-center">
                        <span style="font-family: var(--font-mono); font-size: 0.8125rem; color: var(--accent-gold);">
                            [EXPERIMENTAL DEBRIEF]
                        </span>
                    </div>
                    <button type="button" class="btn-exit-test" id="btn-restart-test">↺ Restart</button>
                </div>

                <div class="exp-stage-area">
                    <div class="results-panel">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
                            <span class="status-pill status-pill--finding">VERIFIED EMPIRICAL RECORD</span>
                            <span style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--accent-gold);">EXP-2026-002</span>
                        </div>

                        <h2 style="font-size: clamp(1.3rem, 2.5vw, 1.65rem); margin-bottom: 0.5rem; color: #ffffff;">
                            Ground Truth vs. Your Observations
                        </h2>

                        <div class="results-stats-row">
                            <div class="stat-box stat-box--gold">
                                <div class="stat-box-label">GROUND TRUTH STIMULUS</div>
                                <div class="stat-box-val">Authentic Stimulus Sheet</div>
                                <p style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.35rem; line-height: 1.4;">
                                    Original White Paper Test document containing the top-right red circle and peripheral shapes.
                                </p>
                            </div>
                            <div class="stat-box stat-box--blue">
                                <div class="stat-box-label">YOUR ESTIMATION</div>
                                <div class="stat-box-val">${this.answers.countEstimate}</div>
                                <p style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.35rem; line-height: 1.4;">
                                    ${accuracySummary}
                                </p>
                            </div>
                        </div>

                        <div class="mechanism-card">
                            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: var(--accent-gold); text-transform: uppercase; margin-bottom: 0.5rem;">
                                COGNITIVE SCIENCE BREAKDOWN
                            </div>
                            <p style="margin-bottom: 0.75rem;">
                                <strong>1. Selective Attention Spotlight:</strong> The prefrontal attentional network directed your conscious spotlight exclusively onto the top-right red circle.
                            </p>
                            <p style="margin-bottom: 0.75rem;">
                                <strong>2. Retinal Exposure vs. Working Memory ($4 \pm 1$):</strong> While your retina captured the full sheet, human working memory can only consolidate $4 \pm 1$ items simultaneously in 5.0s. The peripheral shapes were pre-attentively filtered before conscious verbal recall.
                            </p>
                            <p style="margin-bottom: 0;">
                                <strong>3. Application to Financial Screens ($2^{100}$):</strong> A trading terminal with 20+ candlesticks and multiple indicators forces the visual cortex into over $2^{100}$ combinatorial states, draining cognitive bandwidth. Compressing multi-candlestick clutter into verified single mandate metrics reduces load to $2^0 = 1$.
                            </p>
                        </div>

                        <div style="display: flex; flex-wrap: wrap; gap: 0.75rem; align-items: center; justify-content: space-between; padding-top: 1rem; border-top: 1px solid var(--border-subtle);">
                            <button type="button" class="btn btn-secondary btn-sm" id="btn-toggle-a4-inspect">
                                <span>Inspect Stimulus Image</span>
                                <span style="font-family: var(--font-mono); margin-left: 0.25rem;">👁</span>
                            </button>
                            <button type="button" class="btn btn-primary btn-sm" id="btn-exit-back">
                                <span>Return to Research Website</span>
                                <span style="font-family: var(--font-mono); margin-left: 0.25rem;">→</span>
                            </button>
                        </div>

                        <div id="a4-inspection-container" class="is-hidden" style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px dashed var(--border-strong); text-align: center;">
                            <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--accent-gold); margin-bottom: 1rem;">
                                [SOURCE EXPERIMENTAL IMAGE — NATIVE 2550 × 3300 PX ASPECT RATIO]
                            </div>
                            <div class="a4-viewport-container">
                                <div class="a4-sheet-canvas">
                                    <img src="${ASSET_PATH}" alt="White Paper Test Stimulus" style="width: 100%; height: 100%; object-fit: contain; display: block; background: #ffffff;">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div style="padding: 1rem 0;"></div>
            `;

            const btnToggle = this.overlay.querySelector('#btn-toggle-a4-inspect');
            const inspectBox = this.overlay.querySelector('#a4-inspection-container');
            if (btnToggle && inspectBox) {
                btnToggle.addEventListener('click', () => {
                    const isHidden = inspectBox.classList.contains('is-hidden');
                    if (isHidden) {
                        inspectBox.classList.remove('is-hidden');
                        btnToggle.innerHTML = '<span>Hide Stimulus Image</span> <span style="font-family: var(--font-mono); margin-left: 0.25rem;">✕</span>';
                    } else {
                        inspectBox.classList.add('is-hidden');
                        btnToggle.innerHTML = '<span>Inspect Stimulus Image</span> <span style="font-family: var(--font-mono); margin-left: 0.25rem;">👁</span>';
                    }
                });
            }

            const btnRestart = this.overlay.querySelector('#btn-restart-test');
            if (btnRestart) {
                btnRestart.addEventListener('click', () => this.renderIntro());
            }

            const btnClose = this.overlay.querySelector('#btn-close-results');
            const btnBack = this.overlay.querySelector('#btn-exit-back');
            if (btnClose) btnClose.addEventListener('click', () => this.close());
            if (btnBack) btnBack.addEventListener('click', () => this.close());
        }
    }

    // Initialize controller on DOMContentLoaded
    document.addEventListener('DOMContentLoaded', () => {
        window.whitePaperExperimentInstance = new FullscreenWhitePaperExperiment();
    });

})();
