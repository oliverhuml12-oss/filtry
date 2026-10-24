// reBottled landing page
// Sign-ups are saved to Supabase through the upsert_signup() function
// (see supabase/schema.sql). Connection details live in config.js.

(function () {
  "use strict";

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

  var EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  // Interface text. English is the default; a localised page overrides any of
  // these keys with a <script type="application/json" id="i18n"> block.
  var T = {
    sending: "Sending…",
    notify: "Notify me",
    errorEmpty: "Please enter your email address.",
    errorInvalid: "That doesn't look like an email address. Please check it.",
    errorFailed: "Something went wrong and we couldn't save your email. Please try again.",
    thanksTitle: "You're on the list.",
    thanksQuestion: "One more thing: where do you live? We'll tell you when the pilot reaches you.",
    thanksPlace: "We'll email you as soon as the pilot opens {place}, with your first month and installation free.",
    thanksOther: "We'll keep you posted, and if we come to your area your first month and installation are free.",
    regions: [
      { id: "malta", label: "Malta", place: "in Malta" },
      { id: "cyprus", label: "Cyprus", place: "in Cyprus" },
      { id: "canary-islands", label: "Canary Islands", place: "in the Canary Islands" },
      { id: "other", label: "Somewhere else", place: null }
    ]
  };
  var i18nNode = document.getElementById("i18n");
  if (i18nNode) {
    try {
      var custom = JSON.parse(i18nNode.textContent);
      Object.keys(custom).forEach(function (key) { T[key] = custom[key]; });
    } catch (e) { /* keep English */ }
  }
  var REGIONS = T.regions;

  // Saving to Supabase
  var CONFIG = window.REBOTTLED_CONFIG || {};
  var SUPABASE_URL = (CONFIG.supabaseUrl || "").replace(/\/+$/, "");
  var SUPABASE_KEY = CONFIG.supabaseKey || "";
  var LOCALE = document.documentElement.lang || "en";

  function upsertSignup(email, region) {
    if (!SUPABASE_URL || !SUPABASE_KEY) {
      // Not configured yet: keep the form usable for previews, but say so.
      console.warn("reBottled: Supabase is not configured in config.js, so this sign-up was not saved.");
      return new Promise(function (resolve) { setTimeout(resolve, 300); });
    }
    var headers = { "Content-Type": "application/json", "apikey": SUPABASE_KEY };
    // Legacy anon keys are JWTs and may also go in Authorization; publishable keys must not.
    if (SUPABASE_KEY.indexOf("eyJ") === 0) headers.Authorization = "Bearer " + SUPABASE_KEY;

    return fetch(SUPABASE_URL + "/rest/v1/rpc/upsert_signup", {
      method: "POST",
      headers: headers,
      body: JSON.stringify({
        p_email: email,
        p_region: region || null,
        p_locale: LOCALE,
        p_page: window.location.pathname
      })
    }).then(function (response) {
      if (!response.ok) throw new Error("Sign-up failed with status " + response.status);
    });
  }

  function submitSignup(data) { return upsertSignup(data.email, null); }
  function saveRegion(data) { return upsertSignup(data.email, data.region); }

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  }

  // After a successful sign-up, ask which island the person lives on,
  // so we know where to tell them about the pilot.
  function showThanks(form, email) {
    var panel = el("div", "signup-thanks");
    panel.setAttribute("role", "status");
    panel.setAttribute("tabindex", "-1");

    var title = el("p", "signup-thanks-title", T.thanksTitle);
    var question = el("p", "signup-thanks-text", T.thanksQuestion);
    var choices = el("div", "region-choices");

    REGIONS.forEach(function (region) {
      var button = el("button", "pill-button pill-button-quiet", region.label);
      button.type = "button";
      button.addEventListener("click", function () {
        Array.prototype.forEach.call(choices.children, function (b) { b.disabled = true; });
        saveRegion({ email: email, region: region.id }).then(function () {
          choices.remove();
          question.textContent = region.place
            ? T.thanksPlace.replace("{place}", region.place)
            : T.thanksOther;
        }).catch(function () {
          question.textContent = T.errorFailed;
          Array.prototype.forEach.call(choices.children, function (b) { b.disabled = false; });
        });
      });
      choices.appendChild(button);
    });

    panel.appendChild(title);
    panel.appendChild(question);
    panel.appendChild(choices);
    form.replaceWith(panel);
    panel.focus();
  }

  Array.prototype.forEach.call(document.querySelectorAll("form.signup"), function (form) {
    var input = form.querySelector('input[type="email"]');
    var button = form.querySelector('button[type="submit"]');
    var field = form.querySelector(".signup-field");
    var error = el("p", "signup-error");
    error.id = input.id + "-error";
    error.setAttribute("role", "alert");
    error.hidden = true;
    field.insertAdjacentElement("afterend", error);
    input.setAttribute("aria-describedby", error.id);

    function setError(message) {
      error.textContent = message || "";
      error.hidden = !message;
      field.classList.toggle("is-invalid", !!message);
      if (message) {
        input.setAttribute("aria-invalid", "true");
      } else {
        input.removeAttribute("aria-invalid");
      }
    }

    input.addEventListener("input", function () {
      if (input.getAttribute("aria-invalid") === "true" && EMAIL_PATTERN.test(input.value.trim())) setError("");
    });

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var value = input.value.trim();

      if (!value) {
        setError(T.errorEmpty);
        input.focus();
        return;
      }
      if (!EMAIL_PATTERN.test(value)) {
        setError(T.errorInvalid);
        input.focus();
        return;
      }
      setError("");

      button.disabled = true;
      button.textContent = T.sending;

      submitSignup({ email: value })
        .then(function () {
          showThanks(form, value);
        })
        .catch(function () {
          setError(T.errorFailed);
          button.disabled = false;
          button.textContent = T.notify;
        });
    });
  });
})();
