const API_BASE = "";

// ══════════════════════════════════════════════════════════════
// safeOn()
// A wrapper around addEventListener that first checks whether the
// element actually exists in the DOM. This prevents runtime errors
// like "Cannot read property 'addEventListener' of null" if an ID
// is missing on a particular page.
// ══════════════════════════════════════════════════════════════
function safeOn(id, event, handler) {
  const el = document.getElementById(id);
  if (el) el.addEventListener(event, handler);
}

// ── Page elements ─────────────────────────────
// All DOM element references are grabbed once at the top so we don't
// repeatedly call document.getElementById() throughout the file.
const pageLoader           = document.getElementById("pageLoader");       // full-screen loader shown on first load
const pages                = Array.from(document.querySelectorAll(".page")); // all "page" sections (home, upload, results, admin, etc.)
const navLinks             = Array.from(document.querySelectorAll(".nav-link"));    // top navbar links
const footerLinks          = Array.from(document.querySelectorAll(".footer-link")); // footer navigation links
const uploadArea           = document.getElementById("uploadArea");       // drag-and-drop / click-to-upload box
const imageInput           = document.getElementById("imageInput");       // hidden <input type="file">
const imagePreview         = document.getElementById("imagePreview");     // <img> showing the selected image preview
const classifyBtn          = document.getElementById("classifyBtn");     // "Classify Fruit" button
const uploadMessage        = document.getElementById("uploadMessage");   // status/error message box on upload page
const goToUploadBtn        = document.getElementById("goToUploadBtn");   // "Get Started" button on home page
const resultFruitName      = document.getElementById("resultFruitName");
const resultFruitSubtitle  = document.getElementById("resultFruitSubtitle");
const resultImage          = document.getElementById("resultImage");
const resultConfidenceFill = document.getElementById("resultConfidenceFill"); // the colored confidence bar fill
const resultConfidenceText = document.getElementById("resultConfidenceText"); // "xx% Confidence" text
const nutrientCalories     = document.getElementById("nutrientCalories");
const nutrientCarbs        = document.getElementById("nutrientCarbs");
const nutrientFat          = document.getElementById("nutrientFat");
const nutrientProtein      = document.getElementById("nutrientProtein");
const nutrientFiber        = document.getElementById("nutrientFiber");
const nutrientSugar        = document.getElementById("nutrientSugar");
const classifyAnotherBtn   = document.getElementById("classifyAnotherBtn");
const downloadReportBtn    = document.getElementById("downloadReportBtn");
const adminLoginForm       = document.getElementById("adminLoginForm");
const adminEmailInput      = document.getElementById("adminEmailInput");
const adminPasswordInput   = document.getElementById("adminPasswordInput");
const adminMessage         = document.getElementById("adminMessage");
const checkedImagesGrid    = document.getElementById("checkedImagesGrid"); // container where admin's user-history folders render
const contactForm          = document.getElementById("contactForm");
const contactMessage       = document.getElementById("contactMessage");

// ── Global state (in-memory, resets on page refresh) ─────────
let selectedFile        = null; // the raw File object user picked/dropped
let selectedFileDataUrl = "";   // base64 data URL used to preview + show result image
let lastPrediction      = null; // stores the last API prediction response (needed later for PDF report generation)
let adminKey            = "";   // admin auth key received after successful admin login, sent in headers for admin API calls

// ════════════════════════════════════════════════
// HELPERS
// Small reusable functions for showing/hiding status
// messages (success / error / info) under forms.
// ════════════════════════════════════════════════
function showMessage(target, text, type = "info") {
  if (!target) return;
  target.textContent = text;
  target.classList.remove("hidden", "success", "error", "info");
  target.classList.add(type);
}
function hideMessage(target) {
  if (!target) return;
  target.classList.add("hidden");
}

// ════════════════════════════════════════════════
// showPage()
// This is a Single Page Application (SPA) style navigation function.
// Instead of loading a new HTML file, it just toggles the "active"
// class so only one .page section is visible at a time.
// Also updates which nav-link is highlighted as active,
// and hides the "Auth" nav item while on the admin page.
// ════════════════════════════════════════════════
function showPage(pageId) {
  pages.forEach((page) => {
    if (page) page.classList.toggle("active", page.id === pageId);
  });
  navLinks.forEach((link) => {
    if (!link.dataset.page) return;
    link.classList.toggle("active", link.dataset.page === pageId);
  });
  const authLi = document.querySelector('[data-page="auth"]')?.closest("li");
  if (authLi) authLi.style.display = (pageId === "admin") ? "none" : "";
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// ════════════════════════════════════════════════
// FIX 1: renderNotAFruitError()
// Called when the backend returns a 422 error with
// error_type === "not_a_fruit" (i.e. the uploaded image
// was rejected by the non-fruit detection allowlist).
// Dynamically replaces the result card's HTML with a
// friendly "No Fruit Detected" message + tips + retry buttons,
// instead of showing a raw/ugly error.
// ════════════════════════════════════════════════
function renderNotAFruitError() {
  const resultCard = document.querySelector(".result-card");
  if (!resultCard) return;

  // Injecting a custom "error state" UI directly into the result card
  resultCard.innerHTML = `
    <div style="text-align:center; padding:1.5rem 0;">

      <div style="
        width:90px; height:90px; border-radius:50%;
        background:linear-gradient(135deg,#fff5f5,#ffe0e0);
        display:flex; align-items:center; justify-content:center;
        margin:0 auto 1.25rem; font-size:2.8rem;
        box-shadow:0 8px 24px rgba(229,57,53,0.15);">
        🚫
      </div>

      <span style="
        display:inline-block; font-size:11px; font-weight:700;
        background:#fff5f5; color:#e53e3e; border-radius:20px;
        padding:4px 14px; margin-bottom:1.2rem; letter-spacing:0.06em;
        border:1px solid #fed7d7;">
        NOT A FRUIT IMAGE
      </span>

      <h2 style="font-size:1.8rem; font-weight:700; color:#2d3436; margin:0 0 0.75rem;">
        No Fruit Detected!
      </h2>
      <p style="color:#636e72; font-size:1rem; line-height:1.75; margin-bottom:2rem; max-width:400px; margin-left:auto; margin-right:auto;">
        The AI could not find any recognisable fruit or vegetable in your image.
        Please upload a <strong>clear photo of a fruit</strong>.
      </p>

      <div style="
        background:#f8f9fa; border:1px solid #e9ecef;
        border-radius:14px; padding:1.1rem 1.4rem;
        text-align:left; margin:0 auto 2rem; max-width:420px;
        font-size:0.92rem; color:#636e72;">
        <strong style="color:#2d3436; display:block; margin-bottom:0.5rem;">
          💡 Tips for better results:
        </strong>
        <ul style="margin:0; padding-left:1.2rem; line-height:2.1;">
          <li>Fruit should fill most of the frame</li>
          <li>Use bright, natural lighting</li>
          <li>Avoid blurry or dark images</li>
          <li>Don't include people, text, or other objects</li>
          <li>Supported: JPG, PNG, WEBP (max 10MB)</li>
        </ul>
      </div>

      <div style="display:flex; gap:1rem; justify-content:center; flex-wrap:wrap;">
        <button id="retryUploadBtn" class="cta-button"
          style="background:linear-gradient(135deg,#00b894,#00a085);">
          <i class="fas fa-upload"></i> Try Another Image
        </button>
        <button id="viewFruitsBtn" class="cta-button secondary">
          <i class="fas fa-list-ul"></i> View Supported Fruits
        </button>
      </div>
    </div>`;

  // Re-attach click handlers since innerHTML was replaced
  // (old event listeners are destroyed when HTML is overwritten)
  document.getElementById("retryUploadBtn")
    ?.addEventListener("click", () => {
      // Reset upload state and go back to upload page
      selectedFile        = null;
      selectedFileDataUrl = "";
      if (imagePreview)  { imagePreview.style.display = "none"; imagePreview.src = ""; }
      if (classifyBtn)   classifyBtn.disabled = true;
      if (imageInput)    imageInput.value = "";
      showPage("upload");
    });
  document.getElementById("viewFruitsBtn")
    ?.addEventListener("click", () => showPage("home"));
}

// ════════════════════════════════════════════════
// FIX 2: showClassifyingSpinner()
// Shows a temporary loading spinner inside the result card
// while the backend is processing the classification request.
// This gives instant visual feedback to the user (no blank screen).
// ════════════════════════════════════════════════
function showClassifyingSpinner() {
  const resultCard = document.querySelector(".result-card");
  if (!resultCard) return;
  resultCard.innerHTML = `
    <div style="text-align:center; padding:3rem 1rem;">
      <div style="
        width:80px; height:80px; margin:0 auto 1.5rem;
        border:6px solid #e9ecef;
        border-top-color:#00b894;
        border-radius:50%;
        animation:spin 0.8s linear infinite;">
      </div>
      <p style="font-size:1.2rem; color:#2d3436; font-weight:600; margin:0 0 0.5rem;">
        Analysing your image...
      </p>
      <p style="color:#636e72; font-size:0.95rem;">
        AI model is classifying the fruit. This usually takes 1–3 seconds.
      </p>
    </div>
    <style>
      @keyframes spin { to { transform: rotate(360deg); } }
    </style>`;
}

// ════════════════════════════════════════════════
// IMAGE UPLOAD
// ════════════════════════════════════════════════

// Reads the selected/dropped file as a base64 Data URL so it can be:
// 1) shown instantly in the preview <img>
// 2) reused later as the result image (no need to re-fetch from server)
function setImagePreview(file) {
  const reader = new FileReader();
  reader.onload = (event) => {
    selectedFileDataUrl = event.target.result;
    if (imagePreview) {
      imagePreview.src           = selectedFileDataUrl;
      imagePreview.style.display = "block";
    }
    if (classifyBtn) classifyBtn.disabled = false; // enable button only once a valid image is chosen
  };
  reader.readAsDataURL(file);
}

// Client-side validation before even hitting the backend:
// - must be an actual image file
// - must not exceed 10MB
// This saves an unnecessary API call for obviously invalid files.
function validateFile(file) {
  if (!file)                           return "No file selected.";
  if (!file.type.startsWith("image/")) return "Please upload an image file.";
  if (file.size > 10 * 1024 * 1024)   return "Image must be less than 10MB.";
  return "";
}

// ════════════════════════════════════════════════
// classifyFruit()
// The MAIN function that sends the selected image to the
// backend's /api/predict endpoint and handles the response.
//
// Flow:
// 1. Immediately switch to the results page and show a spinner
//    (better UX than waiting on a static upload page)
// 2. Send the image as multipart/form-data via POST
// 3. If backend returns 422 with error_type "not_a_fruit"
//    -> show the friendly non-fruit error UI
// 4. If backend returns any other error -> go back to upload page
//    and show the error message
// 5. On success -> store prediction data and render the full result
// ════════════════════════════════════════════════
async function classifyFruit() {
  if (!selectedFile) {
    showMessage(uploadMessage, "Please select an image first.", "error");
    return;
  }

  // Immediately show spinner on results page (perceived speed)
  showPage("results");
  showClassifyingSpinner();

  classifyBtn.disabled    = true;
  classifyBtn.textContent = "Classifying...";
  hideMessage(uploadMessage);

  // Build multipart form data containing the image file
  const body = new FormData();
  body.append("image", selectedFile);

  try {
    // If the user is logged in, attach their auth token so the backend
    // can associate this classification with their user_id (for history)
    const userToken = localStorage.getItem("fruitai_token") || "";
    const headers   = userToken ? { "X-User-Token": userToken } : {};

    const response = await fetch(`${API_BASE}/api/predict`, { method: "POST", body, headers });
    const data     = await response.json();

    // Handle non-2xx responses from backend
    if (!response.ok) {
      if (data.error_type === "not_a_fruit") {
        // Special case: image passed upload validation but the
        // AI model / allowlist determined it's NOT a fruit/vegetable
        renderNotAFruitError();
      } else {
        // Generic/unexpected error — go back to upload page and show message
        showPage("upload");
        showMessage(uploadMessage, data.error || "Classification failed. Please try again.", "error");
      }
      return;
    }

    // Success — save prediction (needed later for PDF report) and render UI
    lastPrediction = data;
    renderPrediction(data);

  } catch (error) {
    // Network-level failure (server down, no internet, CORS issue, etc.)
    showPage("upload");
    showMessage(uploadMessage, "Network error. Is the server running?", "error");
  } finally {
    classifyBtn.disabled  = false;
    classifyBtn.innerHTML = 'Classify Fruit <i class="fas fa-arrow-right"></i>';
  }
}

// ════════════════════════════════════════════════
// renderPrediction()
// Rebuilds the entire result card HTML (since it may have been
// replaced earlier by the spinner or error state), then fills in:
// - fruit name, confidence %, image
// - nutrition table (calories, carbs, fat, protein, fiber, sugar)
// - health info cards (benefits, helpful-for, vitamins, warnings)
// - action buttons (Download Report / Classify Another)
// ════════════════════════════════════════════════
function renderPrediction(data) {
  // Restore full result card HTML first (rebuilding structure that
  // may have been overwritten by the spinner / error states)
  const resultCard = document.querySelector(".result-card");
  if (resultCard) {
    resultCard.innerHTML = `
      <div style="font-size:1.2rem;color:#636e72;margin-bottom:1rem;">AI Classification Result</div>
      <div class="fruit-name" id="resultFruitName"></div>
      <div id="resultFruitSubtitle" style="font-size:1.3rem;margin-bottom:2rem;"></div>
      <img id="resultImage" alt="Classified Fruit" class="result-image">
      <div class="confidence-bar">
        <div id="resultConfidenceFill" class="confidence-fill" style="width:0;"></div>
      </div>
      <div id="resultConfidenceText" style="font-size:1.3rem;font-weight:600;margin-bottom:1.2rem;">0.0% Confidence</div>
      <div class="calorie-stats-card">
        <h4>Nutritional Information (per 100g)</h4>
        <table class="calorie-stats-table">
          <tbody>
            <tr><th>Calories</th><td id="nutrientCalories">0 kcal</td></tr>
            <tr><th>Carbohydrates</th><td id="nutrientCarbs">0 g</td></tr>
            <tr><th>Fat</th><td id="nutrientFat">0 g</td></tr>
            <tr><th>Protein</th><td id="nutrientProtein">0 g</td></tr>
            <tr><th>Fiber</th><td id="nutrientFiber">0 g</td></tr>
            <tr><th>Sugar</th><td id="nutrientSugar">0 g</td></tr>
          </tbody>
        </table>
      </div>
      <div class="health-info-grid" id="healthInfoGrid">
        <div class="health-card health-card-benefits">
          <h4><i class="fas fa-heart-pulse"></i> Health Benefits</h4>
          <ul id="healthBenefitsList" class="health-card-list"></ul>
        </div>
        <div class="health-card health-card-helpful">
          <h4><i class="fas fa-notes-medical"></i> Helpful For</h4>
          <ul id="helpfulForList" class="health-card-list"></ul>
        </div>
        <div class="health-card health-card-vitamins">
          <h4><i class="fas fa-capsules"></i> Vitamins & Nutrients</h4>
          <ul id="vitaminsList" class="health-card-list vitamins-list"></ul>
        </div>
        <div class="health-card health-card-warnings">
          <h4><i class="fas fa-triangle-exclamation"></i> Warnings & Precautions</h4>
          <ul id="warningsList" class="health-card-list"></ul>
        </div>
      </div>
      <div style="display:flex;gap:1.5rem;justify-content:center;flex-wrap:wrap;">
        <button id="downloadReportBtn" class="cta-button"
          style="background:linear-gradient(135deg,#00b894,#00a085);">
          <i class="fas fa-download"></i> Download Report
        </button>
        <button id="classifyAnotherBtn" class="cta-button secondary">
          <i class="fas fa-redo"></i> Classify Another
        </button>
      </div>`;

    // Re-wire buttons after innerHTML reset (old listeners were destroyed)
    document.getElementById("classifyAnotherBtn")
      ?.addEventListener("click", () => {
        selectedFile        = null;
        selectedFileDataUrl = "";
        if (imagePreview)  { imagePreview.style.display = "none"; imagePreview.src = ""; }
        if (classifyBtn)   classifyBtn.disabled = true;
        if (imageInput)    imageInput.value = "";
        showPage("upload");
      });
    document.getElementById("downloadReportBtn")
      ?.addEventListener("click", downloadReport);
  }

  // Parse and format confidence percentage (guard against invalid numbers)
  const confidenceRaw = Number(data.confidence);
  const confidencePct = Number.isFinite(confidenceRaw) ? (confidenceRaw * 100).toFixed(2) : "0.00";
  const nutrients     = data.nutrients || {};
  const calories      = Number(nutrients.calories || data.calories_per_100g || 0);

  // Small local helper to shorten repeated getElementById calls below
  const el = (id) => document.getElementById(id);

  // Fill in fruit name, subtitle, confidence bar/text
  if (el("resultFruitName"))      el("resultFruitName").textContent      = data.fruit_name || "Unknown";
  if (el("resultFruitSubtitle"))  el("resultFruitSubtitle").textContent  = data.subtitle   || "Detected by AI model";
  if (el("resultConfidenceText")) el("resultConfidenceText").textContent = `${confidencePct}% Confidence`;
  if (el("resultConfidenceFill")) el("resultConfidenceFill").style.width = `${Math.max(2, Number(confidencePct))}%`; // min 2% width so bar is always visible

  // Fill in nutrition table values (fallback to 0 if missing from backend)
  if (el("nutrientCalories"))     el("nutrientCalories").textContent     = `${Number.isFinite(calories) ? calories : 0} kcal`;
  if (el("nutrientCarbs"))        el("nutrientCarbs").textContent        = `${nutrients.carbohydrates ?? 0} g`;
  if (el("nutrientFat"))          el("nutrientFat").textContent          = `${nutrients.fat           ?? 0} g`;
  if (el("nutrientProtein"))      el("nutrientProtein").textContent      = `${nutrients.protein       ?? 0} g`;
  if (el("nutrientFiber"))        el("nutrientFiber").textContent        = `${nutrients.fiber         ?? 0} g`;
  if (el("nutrientSugar"))        el("nutrientSugar").textContent        = `${nutrients.sugar         ?? 0} g`;

  // Show the uploaded image (prefer local base64 preview over server URL for speed)
  if (el("resultImage"))          el("resultImage").src = selectedFileDataUrl || data.image_url || "";

  // Fill the 4 health info cards (Benefits / Helpful For / Vitamins / Warnings)
  renderHealthInfo(data);
}

// ════════════════════════════════════════════════
// HEALTH INFO CARDS
// (Health Benefits / Helpful For / Vitamins & Nutrients / Warnings & Precautions)
// These are the NEW per-fruit health information cards added for the FYP demo.
// ════════════════════════════════════════════════
const NOT_AVAILABLE_TEXT = "Information not available for this fruit.";

// Generic helper: fills a <ul> with <li> bullet points.
// Falls back to a "not available" message if the data is missing/empty.
function fillBulletList(listId, items) {
  const listEl = document.getElementById(listId);
  if (!listEl) return;
  listEl.innerHTML = "";
  const values = Array.isArray(items) && items.length ? items : [NOT_AVAILABLE_TEXT];
  values.forEach((text) => {
    const li = document.createElement("li");
    li.textContent = text;
    listEl.appendChild(li);
  });
}

// Master function that populates all 4 health cards from the prediction data
function renderHealthInfo(data) {
  // Card 1: Health Benefits — simple list of strings
  fillBulletList("healthBenefitsList", data.health_benefits);
  // Card 2: Helpful For — simple list of strings (e.g. "Weight loss", "Skin health")
  fillBulletList("helpfulForList", data.helpful_for);

  // Card 3: Vitamins & Nutrients — each item is an object { name, benefit }
  // so it needs custom rendering (not a plain bullet list)
  const vitaminsListEl = document.getElementById("vitaminsList");
  if (vitaminsListEl) {
    vitaminsListEl.innerHTML = "";
    const vitamins = Array.isArray(data.vitamins) ? data.vitamins : [];
    if (!vitamins.length) {
      const li = document.createElement("li");
      li.textContent = NOT_AVAILABLE_TEXT;
      vitaminsListEl.appendChild(li);
    } else {
      vitamins.forEach((v) => {
        const li = document.createElement("li");
        li.className = "vitamin-pill";
        // Renders as a "pill" showing vitamin name + its benefit side by side
        li.innerHTML = `<span class="vitamin-name">${v.name || ""}</span><span class="vitamin-benefit">${v.benefit || ""}</span>`;
        vitaminsListEl.appendChild(li);
      });
    }
  }

  // Card 4: Warnings & Precautions — structured object with specific
  // known categories (diabetes, allergy, kidney) plus an "other" array
  const warningsListEl = document.getElementById("warningsList");
  if (warningsListEl) {
    warningsListEl.innerHTML = "";
    const warnings = data.warnings || {};
    // Fixed categories always shown (even if "not available")
    const rows = [
      ["Diabetes", warnings.diabetes],
      ["Allergy Warning", warnings.allergy],
      ["Kidney Disease", warnings.kidney],
    ];
    rows.forEach(([label, text]) => {
      const li = document.createElement("li");
      li.innerHTML = `<strong>${label}:</strong> ${text || NOT_AVAILABLE_TEXT}`;
      warningsListEl.appendChild(li);
    });
    // Any extra/miscellaneous warnings not covered by the 3 fixed categories
    const otherItems = Array.isArray(warnings.other) && warnings.other.length
      ? warnings.other
      : [NOT_AVAILABLE_TEXT];
    otherItems.forEach((text) => {
      const li = document.createElement("li");
      li.innerHTML = `<strong>Other:</strong> ${text}`;
      warningsListEl.appendChild(li);
    });
  }
}

// ════════════════════════════════════════════════
// downloadReport()
// Sends the last prediction data to the backend's
// /api/generate-report endpoint, which uses jsPDF (server-side)
// to build a PDF report, and then triggers a browser download
// of the returned PDF blob.
// ════════════════════════════════════════════════
async function downloadReport() {
  if (!lastPrediction) return; // safety check — nothing to report on

  const btn = document.getElementById("downloadReportBtn");
  const originalHtml = btn ? btn.innerHTML : "";
  if (btn) {
    // Show a loading state on the button while PDF is being generated
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating PDF...';
  }

  try {
    const response = await fetch(`${API_BASE}/api/generate-report`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(lastPrediction), // send the full prediction object (fruit name, nutrients, health info, etc.)
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      throw new Error(err.error || "Could not generate PDF report.");
    }

    // Convert response into a downloadable file using a temporary <a> tag
    const blob = await response.blob();
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement("a");
    a.href     = url;
    a.download = `FruitAI_Report_${(lastPrediction.fruit_name || "report").replace(/\s+/g, "_")}.pdf`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url); // free up memory
  } catch (error) {
    alert(error.message);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = originalHtml; // restore original button text
    }
  }
}

// ════════════════════════════════════════════════
// WIRE NAVIGATION
// Attaches click handlers to navbar + footer links so clicking
// them switches pages via showPage() instead of doing a full
// page reload (SPA behaviour).
// ════════════════════════════════════════════════
function wireNavigation() {
  navLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      const page = link.dataset.page;
      // "Auth" is a separate standalone HTML file, not an in-app page,
      // so it gets a real navigation instead of showPage()
      if (page === "auth") { window.location.href = "/auth.html"; return; }
      showPage(page);
    });
  });
  footerLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      showPage(link.dataset.targetPage);
    });
  });
  if (goToUploadBtn) goToUploadBtn.addEventListener("click", () => showPage("upload"));
}

// ════════════════════════════════════════════════
// WIRE UPLOAD
// Sets up all interactions on the Upload page:
// - click on upload area opens the file picker
// - drag & drop support
// - file input change (manual file selection)
// - Classify button click triggers classifyFruit()
// ════════════════════════════════════════════════
function wireUpload() {
  if (!uploadArea || !imageInput || !classifyBtn) return;

  // Clicking anywhere on the upload box opens the native file dialog
  uploadArea.addEventListener("click", () => imageInput.click());

  // Drag & drop visual feedback + file handling
  uploadArea.addEventListener("dragover", (event) => {
    event.preventDefault();
    uploadArea.classList.add("dragover");
  });
  uploadArea.addEventListener("dragleave", () => uploadArea.classList.remove("dragover"));

  uploadArea.addEventListener("drop", (event) => {
    event.preventDefault();
    uploadArea.classList.remove("dragover");
    const file  = event.dataTransfer.files[0];
    const error = validateFile(file);
    if (error) { showMessage(uploadMessage, error, "error"); return; }
    selectedFile = file;
    setImagePreview(file);
    showMessage(uploadMessage, "Image ready for classification.", "success");
  });

  // Manual file selection via the file input dialog
  imageInput.addEventListener("change", () => {
    const file  = imageInput.files[0];
    const error = validateFile(file);
    if (error) { showMessage(uploadMessage, error, "error"); return; }
    selectedFile = file;
    setImagePreview(file);
    showMessage(uploadMessage, "Image selected successfully.", "success");
  });

  classifyBtn.addEventListener("click", classifyFruit);
}

// ════════════════════════════════════════════════
// WIRE RESULTS
// Sets up the buttons on the Results page (initial page load wiring).
// Note: these buttons often get re-wired again inside
// renderPrediction() because innerHTML gets reset there.
// ════════════════════════════════════════════════
function wireResultsActions() {
  if (classifyAnotherBtn) {
    classifyAnotherBtn.addEventListener("click", () => {
      selectedFile        = null;
      selectedFileDataUrl = "";
      if (imagePreview)  { imagePreview.style.display = "none"; imagePreview.src = ""; }
      if (classifyBtn)   classifyBtn.disabled = true;
      if (imageInput)    imageInput.value = "";
      showPage("upload");
    });
  }
  if (downloadReportBtn) downloadReportBtn.addEventListener("click", downloadReport);
}

// ════════════════════════════════════════════════
// ADMIN — USER-FOLDER VIEW
// Renders the admin panel's "Checked Images" section as
// collapsible folders, one per user (plus a "Guest" folder
// for anonymous/non-logged-in classifications).
// Each folder shows: user avatar, name/email, stats,
// their feedback messages, and a grid of their classified images.
// ════════════════════════════════════════════════
function renderCheckedImages(users) {
  if (!checkedImagesGrid) return;
  if (!Array.isArray(users) || users.length === 0) {
    checkedImagesGrid.innerHTML = '<div class="admin-summary">No classifications found.</div>';
    return;
  }
  checkedImagesGrid.innerHTML = "";
  users.forEach((user) => {
    const isGuest = !user.user_id; // no user_id means these are anonymous/guest classifications
    const folder  = document.createElement("div");
    folder.style.cssText = "border:1px solid #e0e0e0;border-radius:14px;margin-bottom:1.2rem;overflow:hidden;box-shadow:0 3px 12px rgba(0,0,0,0.07);";

    // ── Folder header (clickable to expand/collapse) ──
    const header  = document.createElement("div");
    header.style.cssText = `display:flex;align-items:center;justify-content:space-between;padding:0.9rem 1.4rem;background:${isGuest?"linear-gradient(135deg,#636e72,#4a5568)":"linear-gradient(135deg,#00b894,#00a085)"};cursor:pointer;user-select:none;`;
    const avatarLetter = user.username ? user.username[0].toUpperCase() : "?";
    const lastDate     = user.last_active
      ? new Date(user.last_active).toLocaleDateString("en-US",{day:"numeric",month:"short",year:"numeric"})
      : "—";
    header.innerHTML = `
      <div style="display:flex;align-items:center;gap:0.8rem;">
        <div style="width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,0.25);display:flex;align-items:center;justify-content:center;font-size:1.15rem;color:white;font-weight:700;">${avatarLetter}</div>
        <div>
          <div style="color:white;font-weight:600;font-size:0.97rem;">${user.username}</div>
          <div style="color:rgba(255,255,255,0.75);font-size:0.78rem;">${user.email||"No email"}</div>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:1rem;">
        <div style="text-align:right;">
          <div style="color:white;font-weight:600;font-size:0.9rem;">${user.total_tests} test${user.total_tests!==1?"s":""}${(user.feedback&&user.feedback.length)?` · 💬 ${user.feedback.length}`:""}</div>
          <div style="color:rgba(255,255,255,0.75);font-size:0.75rem;">Last: ${lastDate}</div>
        </div>
        <span class="folder-chevron" style="color:white;font-size:1rem;transition:transform 0.25s ease;">▼</span>
      </div>`;

    // ── Folder body (hidden by default, expands on header click) ──
    const body = document.createElement("div");
    body.style.cssText = "display:none;padding:1rem;background:#f8f9fa;border-top:1px solid #e9ecef;";

    // ── Feedback box: shows any feedback messages this user submitted ──
    if (user.feedback && user.feedback.length > 0) {
      const feedbackWrap = document.createElement("div");
      feedbackWrap.style.cssText = "margin-bottom:1.2rem;";
      const feedbackTitle = document.createElement("div");
      feedbackTitle.style.cssText = "font-weight:600;color:#2d3436;font-size:0.88rem;margin-bottom:0.6rem;";
      feedbackTitle.innerHTML = `💬 Feedback (${user.feedback.length})`;
      feedbackWrap.appendChild(feedbackTitle);
      user.feedback.forEach((fb) => {
        const timeStr = fb.created_at ? new Date(fb.created_at).toLocaleString("en-US",{month:"short",day:"numeric",hour:"2-digit",minute:"2-digit"}) : "";
        const fbBox = document.createElement("div");
        fbBox.style.cssText = "background:#fff9e6;border-left:3px solid #fdcb6e;border-radius:8px;padding:0.7rem 0.9rem;margin-bottom:0.6rem;position:relative;";
        fbBox.innerHTML = `
          <button class="delete-feedback-btn" data-feedback-id="${fb.id}" title="Delete feedback"
            style="position:absolute;top:0.5rem;right:0.6rem;background:none;border:none;cursor:pointer;color:#d63031;font-size:0.95rem;padding:0.2rem;line-height:1;">
            <i class="fas fa-trash-alt"></i>
          </button>
          <div style="font-size:0.85rem;color:#2d3436;line-height:1.4;margin-bottom:0.4rem;padding-right:1.5rem;">${fb.message}</div>
          <div style="font-size:0.72rem;color:#b2bec3;display:flex;justify-content:space-between;">
            <span>${fb.full_name||""} ${fb.email?`· ${fb.email}`:""}</span>
            <span>🕐 ${timeStr}</span>
          </div>`;
        feedbackWrap.appendChild(fbBox);
      });
      body.appendChild(feedbackWrap);
    }

    // ── Images grid: all fruits this user has classified ──
    if (!user.images||user.images.length===0) {
      const noImages = document.createElement("p");
      noImages.style.cssText = "color:#636e72;text-align:center;padding:1rem;margin:0;";
      noImages.textContent = "No images yet.";
      body.appendChild(noImages);
    } else {
      const grid = document.createElement("div");
      grid.style.cssText = "display:grid;grid-template-columns:repeat(auto-fill,minmax(155px,1fr));gap:0.9rem;";
      user.images.forEach((item) => {
        const confidencePct = Number.isFinite(Number(item.confidence))?(Number(item.confidence)*100).toFixed(1):"0.0";
        const timeStr = item.created_at ? new Date(item.created_at).toLocaleString("en-US",{month:"short",day:"numeric",hour:"2-digit",minute:"2-digit"}) : "";
        const card = document.createElement("article");
        card.style.cssText = "background:white;border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);transition:transform 0.18s,box-shadow 0.18s;position:relative;";
        // Simple hover animation (lift + bigger shadow) done via inline JS handlers
        card.onmouseenter = () => { card.style.transform="translateY(-3px)"; card.style.boxShadow="0 6px 20px rgba(0,0,0,0.13)"; };
        card.onmouseleave = () => { card.style.transform="translateY(0)";    card.style.boxShadow="0 2px 8px rgba(0,0,0,0.08)"; };
        card.innerHTML = `
          <button class="delete-image-btn" data-image-id="${item.id}" title="Delete this classification"
            style="position:absolute;top:0.4rem;right:0.4rem;background:rgba(214,48,49,0.9);border:none;cursor:pointer;color:white;font-size:0.8rem;width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,0.25);z-index:2;">
            <i class="fas fa-trash-alt"></i>
          </button>
          <img src="${item.image_url}" alt="${item.fruit_name}" style="width:100%;height:115px;object-fit:cover;display:block;" onerror="this.style.display='none'">
          <div style="padding:0.65rem 0.75rem;">
            <div style="font-weight:600;font-size:0.9rem;color:#2d3436;margin-bottom:0.25rem;">${item.fruit_name}</div>
            <div style="font-size:0.76rem;color:#00b894;margin-bottom:0.1rem;">✓ ${confidencePct}% confidence</div>
            <div style="font-size:0.76rem;color:#636e72;margin-bottom:0.1rem;">🔥 ${item.calories_per_100g} kcal</div>
            <div style="font-size:0.7rem;color:#b2bec3;margin-top:0.3rem;">🕐 ${timeStr}</div>
          </div>`;
        grid.appendChild(card);
      });
      body.appendChild(grid);
    }

    // Toggle folder open/closed on header click (accordion behaviour)
    let isOpen = false;
    header.addEventListener("click", () => {
      isOpen = !isOpen;
      body.style.display = isOpen ? "block" : "none";
      const ch = header.querySelector(".folder-chevron");
      if (ch) ch.style.transform = isOpen ? "rotate(180deg)" : "rotate(0deg)";
    });
    folder.appendChild(header);
    folder.appendChild(body);
    checkedImagesGrid.appendChild(folder);
  });
}

// Deletes a single classified image entry (admin-only action).
// Requires adminKey to be sent in headers for authorization.
async function deleteCheckedImage(imageId, cardEl) {
  if (!confirm("Delete this classified image? This cannot be undone.")) return;
  try {
    const response = await fetch(`${API_BASE}/api/admin/checked-images/${imageId}`, {
      method: "DELETE", headers: { "X-Admin-Key": adminKey },
    });
    const data = await response.json();
    if (!response.ok || !data.ok) throw new Error(data.error || "Could not delete image.");
    if (cardEl) cardEl.remove(); // remove the card from DOM instantly (no full re-fetch needed)
  } catch (error) {
    alert(error.message);
  }
}

// Deletes a single feedback entry (admin-only action)
async function deleteFeedbackEntry(feedbackId, boxEl) {
  if (!confirm("Delete this feedback entry? This cannot be undone.")) return;
  try {
    const response = await fetch(`${API_BASE}/api/admin/feedback/${feedbackId}`, {
      method: "DELETE", headers: { "X-Admin-Key": adminKey },
    });
    const data = await response.json();
    if (!response.ok || !data.ok) throw new Error(data.error || "Could not delete feedback.");
    if (boxEl) boxEl.remove();
  } catch (error) {
    alert(error.message);
  }
}

// Event delegation: instead of attaching a click listener to every
// single delete button (which would need re-wiring every re-render),
// we listen once on the parent container and detect which button
// was clicked using event.target.closest().
if (checkedImagesGrid) {
  checkedImagesGrid.addEventListener("click", (event) => {
    const delImgBtn = event.target.closest(".delete-image-btn");
    if (delImgBtn) {
      event.stopPropagation(); // prevent this click from also toggling the folder open/close
      deleteCheckedImage(delImgBtn.dataset.imageId, delImgBtn.closest("article"));
      return;
    }
    const delFbBtn = event.target.closest(".delete-feedback-btn");
    if (delFbBtn) {
      event.stopPropagation();
      deleteFeedbackEntry(delFbBtn.dataset.feedbackId, delFbBtn.parentElement);
    }
  });
}

// Fetches all users + their classification history + feedback from
// the backend (admin-only endpoint) and renders it via renderCheckedImages().
// Also updates the summary text (total users / tests / feedback count).
async function loadCheckedImages() {
  hideMessage(adminMessage);
  if (checkedImagesGrid) checkedImagesGrid.innerHTML = '<div class="admin-summary" style="color:#636e72;">Loading user history…</div>';
  try {
    const response = await fetch(`${API_BASE}/api/admin/users-history`, { headers: { "X-Admin-Key": adminKey } });
    const data     = await response.json();
    if (!response.ok) throw new Error(data.error || "Could not load history.");
    renderCheckedImages(data.users || []);
    const totalUsers    = (data.users||[]).filter(u=>u.user_id).length; // excludes guest folder from user count
    const totalTests    = (data.users||[]).reduce((s,u)=>s+u.total_tests,0);
    const totalFeedback = (data.users||[]).reduce((s,u)=>s+((u.feedback||[]).length),0);
    showMessage(adminMessage, `✅ ${totalUsers} registered user(s) · ${totalTests} total classifications · 💬 ${totalFeedback} feedback`, "success");
  } catch (error) {
    showMessage(adminMessage, error.message, "error");
  }
}

// Handles the admin login form submission:
// sends email/password to backend, receives an adminKey on success,
// hides the login form, and loads the user history view.
async function submitAdminLogin(event) {
  event.preventDefault();
  hideMessage(adminMessage);
  const payload = {
    email:    (adminEmailInput?.value  || "").trim(),
    password:  adminPasswordInput?.value || "",
  };
  try {
    const response = await fetch(`${API_BASE}/api/admin/login`, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Login failed.");
    adminKey = data.admin_key || "";
    if (!adminKey) throw new Error("Login succeeded but admin key missing.");
    showMessage(adminMessage, "Admin login successful.", "success");
    if (adminLoginForm) adminLoginForm.closest(".admin-card").style.display = "none"; // hide login card after success
    await loadCheckedImages();
  } catch (error) {
    showMessage(adminMessage, error.message, "error");
  }
}

// ════════════════════════════════════════════════
// CONTACT
// Handles the "Contact Us" form submission on the site.
// If the user is logged in, their auth token is attached so the
// message can be linked to their account.
// ════════════════════════════════════════════════
async function submitContactForm(event) {
  event.preventDefault();
  hideMessage(contactMessage);
  const payload    = Object.fromEntries(new FormData(contactForm).entries());
  const userToken  = localStorage.getItem("fruitai_token") || "";
  const headers    = { "Content-Type": "application/json" };
  if (userToken) headers["X-User-Token"] = userToken;
  try {
    const response = await fetch(`${API_BASE}/api/contact`, {
      method: "POST", headers, body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok || !data.ok) throw new Error(data.error || "Failed to send message.");
    showMessage(contactMessage, "Message sent successfully.", "success");
    contactForm.reset();
  } catch (error) {
    showMessage(contactMessage, error.message, "error");
  }
}

// Attaches submit handlers for the admin login form + contact form
function wireAdminAndContact() {
  if (adminLoginForm) adminLoginForm.addEventListener("submit", submitAdminLogin);
  if (contactForm)    contactForm.addEventListener("submit",    submitContactForm);
}

// ════════════════════════════════════════════════
// MISC
// ════════════════════════════════════════════════

// Adds a fallback for ALL <img> tags on the page: if an image fails
// to load (broken URL, 404, etc.), hide it instead of showing the
// ugly broken-image icon. Skips resultImage/imagePreview since those
// are handled separately (they need to show the actual preview).
function wireImageFallback() {
  document.querySelectorAll("img").forEach((img) => {
    img.addEventListener("error", () => {
      if (img.id === "resultImage" || img.id === "imagePreview") return;
      img.style.display = "none";
    });
  });
}

// Pings the backend's /api/health endpoint on page load to confirm
// the Flask server is running. If it's not reachable, shows an error
// message early (better than the user discovering this only after
// trying to classify an image).
async function checkBackendHealth() {
  try {
    const response = await fetch(`${API_BASE}/api/health`);
    const data     = await response.json();
    if (!response.ok || !data.ok) throw new Error(data.error || "Backend not ready.");
  } catch (error) {
    if (uploadMessage) showMessage(uploadMessage, `Backend not ready: ${error.message}`, "error");
  }
}

// If the user is already logged in (username saved in localStorage
// from a previous session), replace the "Auth" nav link with their
// username so it looks like a personalized account menu.
function updateNavForUser() {
  const username = localStorage.getItem("fruitai_username");
  const authLink = document.querySelector('[data-page="auth"]');
  if (!authLink) return;
  if (username) authLink.innerHTML = `<i class="fas fa-user-circle"></i> ${username}`;
}

// ════════════════════════════════════════════════
// PAGE LOADER
// Fades out and removes the initial full-screen loading
// screen a short moment after the page has fully loaded.
// ════════════════════════════════════════════════
window.addEventListener("load", () => {
  if (!pageLoader) return;
  setTimeout(() => {
    pageLoader.style.opacity       = "0";
    pageLoader.style.pointerEvents = "none";
    setTimeout(() => pageLoader.remove(), 300);
  }, 500);
});

// ════════════════════════════════════════════════
// INIT
// Runs all the "wiring" functions once when the script loads,
// setting up every interactive part of the page.
// ════════════════════════════════════════════════
wireNavigation();      // navbar + footer link clicks
wireUpload();          // upload area drag/drop/click + classify button
wireResultsActions();  // classify-another / download-report buttons (initial wiring)
wireAdminAndContact(); // admin login form + contact form submissions
wireImageFallback();   // broken image handling
checkBackendHealth();  // verify Flask backend is reachable
updateNavForUser();    // show logged-in username in navbar if applicable