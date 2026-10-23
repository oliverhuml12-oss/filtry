// reBottled landing page
// The sign-up form is front-end only for now: nothing is sent or stored.
// When a backend exists, replace submitSignup() below with a real request.

(function () {
  "use strict";

  // Header border once the page is scrolled
  var header = document.querySelector(".site-header");
  function onScroll() {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 8);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Current year in the footer
  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());

  // Grow the comparison bars when they come into view
  var bars = document.querySelector(".bars");
  if (bars) {
    if ("IntersectionObserver" in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            bars.classList.add("is-visible");
            observer.disconnect();
          }
        });
      }, { threshold: 0.35 });
      observer.observe(bars);
    } else {
      bars.classList.add("is-visible");
    }
  }

  // Sign-up form
  var form = document.getElementById("join-form");
  if (!form) return;

  var email = form.elements.email;
  var region = form.elements.region;
  var consent = form.elements.consent;
  var status = document.getElementById("form-status");
  var submitButton = form.querySelector('button[type="submit"]');

  var EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  var regionNames = {
    "malta": "Malta",
    "cyprus": "Cyprus",
    "canary-islands": "the Canary Islands",
    "other": "your area"
  };

  function setError(input, message) {
    var error = document.getElementById(input.id + "-error");
    if (error) error.textContent = message || "";
    if (message) {
      input.setAttribute("aria-invalid", "true");
    } else {
      input.removeAttribute("aria-invalid");
    }
  }

  function validate() {
    var firstInvalid = null;
    var value = email.value.trim();

    if (!value) {
      setError(email, "Please enter your email address.");
      firstInvalid = firstInvalid || email;
    } else if (!EMAIL_PATTERN.test(value)) {
      setError(email, "That doesn't look like an email address. Please check it.");
      firstInvalid = firstInvalid || email;
    } else {
      setError(email, "");
    }

    if (!region.value) {
      setError(region, "Please choose where you live.");
      firstInvalid = firstInvalid || region;
    } else {
      setError(region, "");
    }

    if (!consent.checked) {
      setError(consent, "Please tick the box so we are allowed to email you.");
      firstInvalid = firstInvalid || consent;
    } else {
      setError(consent, "");
    }

    return firstInvalid;
  }

  // Placeholder for the real submission. Returns a promise so the UI flow
  // already matches what a network request will need.
  function submitSignup(data) {
    // TODO: send `data` ({ email, region, consent, signedUpAt }) to the sign-up backend.
    return new Promise(function (resolve) {
      setTimeout(resolve, 400);
    });
  }

  // Clear an error as soon as the person fixes the field
  [email, region, consent].forEach(function (input) {
    var eventName = input.type === "checkbox" || input.tagName === "SELECT" ? "change" : "input";
    input.addEventListener(eventName, function () {
      if (input.getAttribute("aria-invalid") === "true") validate();
    });
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    status.hidden = true;
    status.classList.remove("is-success");

    var firstInvalid = validate();
    if (firstInvalid) {
      firstInvalid.focus();
      return;
    }

    var chosenRegion = region.value;
    submitButton.disabled = true;
    submitButton.textContent = "Sending…";

    submitSignup({
      email: email.value.trim(),
      region: chosenRegion,
      consent: true,
      signedUpAt: new Date().toISOString()
    }).then(function () {
      status.textContent = chosenRegion === "other"
        ? "Thank you, you're on the list. We'll email you with news, and if we come to your area you'll get the first month and installation free."
        : "Thank you, you're on the list. We'll email you as soon as the pilot opens in " + regionNames[chosenRegion] + ", with your first month and installation free.";
      status.classList.add("is-success");
      status.hidden = false;
      form.reset();
    }).catch(function () {
      status.textContent = "Something went wrong and we couldn't save your email. Please try again in a moment.";
      status.hidden = false;
    }).then(function () {
      submitButton.disabled = false;
      submitButton.textContent = "Notify me";
    });
  });
})();
