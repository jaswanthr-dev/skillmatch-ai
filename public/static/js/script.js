const navToggleButton = document.getElementById("nav-toggle");
const topNav = document.getElementById("top-nav");

if (navToggleButton && topNav) {
    navToggleButton.addEventListener("click", function () {
        const isOpen = topNav.classList.toggle("open");
        navToggleButton.setAttribute("aria-expanded", isOpen ? "true" : "false");
        navToggleButton.classList.toggle("open", isOpen);
    });

    topNav.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
            topNav.classList.remove("open");
            navToggleButton.setAttribute("aria-expanded", "false");
            navToggleButton.classList.remove("open");
        });
    });
}

const THEME_STORAGE_KEY = "skillmatch-theme";
const themeToggleButton = document.getElementById("theme-toggle");

function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
}

const savedTheme = localStorage.getItem(THEME_STORAGE_KEY);
const systemPrefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
applyTheme(savedTheme || (systemPrefersDark ? "dark" : "light"));

if (themeToggleButton) {
    themeToggleButton.addEventListener("click", function () {
        const currentTheme = document.documentElement.getAttribute("data-theme");
        const nextTheme = currentTheme === "dark" ? "light" : "dark";
        applyTheme(nextTheme);
        localStorage.setItem(THEME_STORAGE_KEY, nextTheme);
    });
}

// --- Confirm before a destructive action (custom modal, not window.confirm) ---

const modalOverlay = document.getElementById("confirm-modal-overlay");
const modalMessage = document.getElementById("modal-message");
const modalCancelBtn = document.getElementById("modal-cancel-btn");
const modalConfirmBtn = document.getElementById("modal-confirm-btn");

let pendingForm = null;

function showConfirmModal(message, form) {
    pendingForm = form;
    modalMessage.textContent = message;
    modalOverlay.classList.add("open");
}

function hideConfirmModal() {
    modalOverlay.classList.remove("open");
    pendingForm = null;
}

document.querySelectorAll("form[data-confirm]").forEach(function (form) {
    form.addEventListener("submit", function (event) {
        if (form.dataset.userConfirmed === "true") {
            return;
        }
        event.preventDefault();
        showConfirmModal(form.getAttribute("data-confirm"), form);
    });
});

if (modalConfirmBtn) {
    modalConfirmBtn.addEventListener("click", function () {
        if (pendingForm) {
            pendingForm.dataset.userConfirmed = "true";
            pendingForm.submit();
        }
        hideConfirmModal();
    });
}

if (modalCancelBtn) {
    modalCancelBtn.addEventListener("click", hideConfirmModal);
}

if (modalOverlay) {
    modalOverlay.addEventListener("click", function (event) {
        if (event.target === modalOverlay) {
            hideConfirmModal();
        }
    });
}

document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        hideConfirmModal();
    }
});

const skillsField = document.getElementById("student_skills");
const jobField = document.getElementById("job_description");
const submitButton = document.getElementById("submit-btn");

if (skillsField && jobField && submitButton) {
    function updateSubmitState() {
        const bothFilled = skillsField.value.trim().length > 0 && jobField.value.trim().length > 0;
        submitButton.disabled = !bothFilled;
    }
    updateSubmitState();
    skillsField.addEventListener("input", updateSubmitState);
    jobField.addEventListener("input", updateSubmitState);
}