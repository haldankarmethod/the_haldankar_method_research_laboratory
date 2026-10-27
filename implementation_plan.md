# Implementation Plan — Fix CIRF Inquiry Template Location Error

This document provides the diagnosis and fix plan for resolving the `TemplateDoesNotExist: haldankar_contact/cirf_inquiry.html` error when accessing `http://127.0.0.1:8000/contact/cirf/`.

> [!IMPORTANT]
> **Constraint**: Pre-implementation design specification. No source code, HTML, or Django template files will be modified until explicit user review and approval of this plan.

---

## 1. Diagnosis & Root Cause

### Root Cause Analysis
1. **Uncached App Template Directory in Running `runserver`**:
   - Django's `APP_DIRS: True` setting scans `INSTALLED_APPS` for `templates/` directories when the server process initializes or reloads.
   - When the `python manage.py runserver` process was started 6+ hours ago, `haldankar_contact` contained **no** `templates/` directory (only `views.py`, `forms.py`, `urls.py`).
   - When the new directory `haldankar_contact/templates/haldankar_contact/cirf_inquiry.html` was created, the running `runserver` process did not auto-register the newly created `templates/` directory into its active template loader memory.
2. **Project-Level `DIRS` Fallback**:
   - The project settings (`settings.py`) explicitly define `DIRS: [BASE_DIR / 'templates']`.
   - Creating a copy of `cirf_inquiry.html` inside `templates/haldankar_contact/cirf_inquiry.html` ensures Django's `DIRS` loader finds the template immediately, even if `APP_DIRS` cache has not re-scanned.

---

## 2. Configuration Analysis

| Aspect | Current State | Target Correct State |
| :--- | :--- | :--- |
| **View Template String** | `'haldankar_contact/cirf_inquiry.html'` in `views.py` | **Keep `'haldankar_contact/cirf_inquiry.html'`** (100% correct). |
| **App-Level Template** | `haldankar_contact/templates/haldankar_contact/cirf_inquiry.html` | **Retain on disk** (Standard Django app structure). |
| **Project-Level Template** | *Missing in `templates/haldankar_contact/`* | **Add to `templates/haldankar_contact/cirf_inquiry.html`** (Matches `DIRS: [BASE_DIR / 'templates']`). |

---

## 3. Structural Relationship Check (All Other CIRF Files)

All other CIRF component files were inspected and verified to be structurally aligned:
* `haldankar_contact/forms.py` $\rightarrow$ `CIRFInquiryForm` clean.
* `haldankar_contact/views.py` $\rightarrow$ `cirf_inquiry` & `submit_cirf_inquiry` clean.
* `haldankar_contact/urls.py` $\rightarrow$ `/contact/cirf/` and `/contact/cirf/submit/` mapped.
* `static/css/components/cirf_form.css` $\rightarrow$ Form styling present.
* `static/js/script.js` $\rightarrow$ `initCIRFForm()` AJAX handler configured.
* `HumanInformationLiteracy/.../foundation.html` $\rightarrow$ Embedded form card present.

---

## 4. Proposed Solution

### A. Template Placement Strategy
* **Do NOT change the view**: The view path `'haldankar_contact/cirf_inquiry.html'` is standard and correct.
* **Dual Location Guarantee**:
  1. Keep `haldankar_contact/templates/haldankar_contact/cirf_inquiry.html` (App-level).
  2. Create `templates/haldankar_contact/cirf_inquiry.html` (Project-level under `DIRS`).
* **Touch View File**: Touch `haldankar_contact/views.py` to trigger Django's `runserver` reloader to re-scan `APP_DIRS`.

---

## 5. File Changes Required

### Files to Create / Copy:
1. `templates/haldankar_contact/cirf_inquiry.html`: Copy template into project-level `templates/haldankar_contact/` directory.

### Files to Touch:
1. `haldankar_contact/views.py`: Touch file timestamp so `runserver` reloader updates template directory cache.

---

## 6. Verification Steps After Approval

1. **Django Template Loader Verification**:
   - Run python template resolution script: `get_template('haldankar_contact/cirf_inquiry.html')`.
2. **HTTP GET Verification**:
   - Execute GET request to `http://127.0.0.1:8000/contact/cirf/` $\rightarrow$ Confirm `200 OK`.
3. **HTTP POST Verification**:
   - Execute POST request to `http://127.0.0.1:8000/contact/cirf/submit/` $\rightarrow$ Confirm JSON success.

---

> [!IMPORTANT]
> **Awaiting User Approval**: No files will be modified until you review and approve this diagnosis and fix plan.
