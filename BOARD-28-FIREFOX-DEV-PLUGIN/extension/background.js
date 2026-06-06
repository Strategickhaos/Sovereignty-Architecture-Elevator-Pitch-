/**
 * SAGCO Firefox Dev Recon — background.js
 * Captures: webRequest errors, PII in URLs, token exposure, sampling flags
 * Classifies every event into a SAGCO district + antibody
 * Export: toolbar button → JSON download
 */

"use strict";

const MAX_EVENTS = 500;

// ── SAGCO district + antibody classifier ─────────────────────────────────────

const ANTIBODY_RULES = [
  // Token exposure — CRITICAL
  { patterns: ["access_token=", "id_token=", "bearer=", "auth_token="],
    severity: "CRITICAL", antibody: "BROWSER_TOKEN_IN_REFERRER",
    district: "trinity", sensitive: true },

  // PII in pixel — HIGH
  { patterns: ["phone_number=", "hashed_phone=", "hashed_email=", "em_hash="],
    severity: "HIGH", antibody: "BROWSER_PII_IN_TRACKING_PIXEL",
    district: "trinity", sensitive: true },

  // Known tracking pixels — LOW
  { patterns: ["t.co/i/adsct", "doubleclick.net", "google-analytics.com",
               "facebook.com/tr", "segment.io", "mixpanel.com",
               "amplitude.com", "hotjar.com", "intercom.io", "fullstory.com"],
    severity: "LOW", antibody: "BROWSER_TRACKING_PIXEL_FAILURE",
    district: "memory_palace", sensitive: false },

  // Third-party widgets — LOW
  { patterns: ["statsig", "stripe.com", "intercom", "frill.co",
               "widget.frill", "sentry.io", "grafana"],
    severity: "LOW", antibody: "BROWSER_THIRD_PARTY_WIDGET_EVENT",
    district: "memory_palace", sensitive: false },

  // Analytics sampling — LOW
  { patterns: ["grafana-faro", "faro", "isSampled", "opentelemetry"],
    severity: "LOW", antibody: "BROWSER_ANALYTICS_SAMPLING",
    district: "memory_palace", sensitive: false },
];

function classify(url, errorCode) {
  const lower = (url || "").toLowerCase();

  for (const rule of ANTIBODY_RULES) {
    if (rule.patterns.some(p => lower.includes(p.toLowerCase()))) {
      return {
        severity:  rule.severity,
        antibody:  rule.antibody,
        district:  rule.district,
        sensitive: rule.sensitive,
      };
    }
  }

  // Unknown error — contradiction_forest
  if (errorCode && errorCode.includes("ERR_")) {
    return {
      severity: "MEDIUM",
      antibody: "BROWSER_UNKNOWN_WEBREQUEST",
      district: "contradiction_forest",
      sensitive: false,
    };
  }

  return {
    severity: "LOW",
    antibody: "BROWSER_BENIGN_EVENT",
    district: "memory_palace",
    sensitive: false,
  };
}

// ── Event store ───────────────────────────────────────────────────────────────

let events = [];

async function loadEvents() {
  const data = await browser.storage.local.get("sagco_events");
  events = data.sagco_events || [];
}

async function saveEvent(evt) {
  events.push(evt);
  if (events.length > MAX_EVENTS) events = events.slice(-MAX_EVENTS);
  await browser.storage.local.set({ sagco_events: events });
}

// ── webRequest error listener ─────────────────────────────────────────────────

browser.webRequest.onErrorOccurred.addListener(
  (details) => {
    const c = classify(details.url, details.error);
    saveEvent({
      ts:       new Date().toISOString(),
      type:     "webrequest_error",
      url:      c.sensitive ? "[REDACTED]" : details.url,
      error:    details.error,
      tabId:    details.tabId,
      severity: c.severity,
      antibody: c.antibody,
      district: c.district,
    });
  },
  { urls: ["<all_urls>"] }
);

// ── Navigation listener — catches URL-level token exposure ────────────────────

browser.webNavigation.onCommitted.addListener((details) => {
  const c = classify(details.url, null);
  if (c.severity === "CRITICAL" || c.severity === "HIGH") {
    saveEvent({
      ts:       new Date().toISOString(),
      type:     "navigation_pii_or_token",
      url:      "[REDACTED — sensitive]",
      severity: c.severity,
      antibody: c.antibody,
      district: c.district,
      note:     "URL contained sensitive parameter — value redacted",
    });
  }
});

// ── Messages from content script ──────────────────────────────────────────────

browser.runtime.onMessage.addListener((msg) => {
  if (msg.type === "sagco_console_event") {
    const c = classify(msg.url || "", null);
    saveEvent({
      ts:       new Date().toISOString(),
      type:     "console_event",
      text:     msg.text ? msg.text.slice(0, 200) : "",
      source:   msg.source,
      url:      msg.url,
      severity: c.severity,
      antibody: c.antibody,
      district: c.district,
    });
  }
});

// ── Toolbar button — export JSON ──────────────────────────────────────────────

browser.browserAction.onClicked && browser.browserAction.onClicked.addListener(async () => {
  const data = await browser.storage.local.get("sagco_events");
  const allEvents = data.sagco_events || [];

  const export_doc = {
    exported_at:   new Date().toISOString(),
    board:         "BOARD-28-FIREFOX-DEV-PLUGIN",
    total_events:  allEvents.length,
    by_severity: {
      CRITICAL: allEvents.filter(e => e.severity === "CRITICAL").length,
      HIGH:     allEvents.filter(e => e.severity === "HIGH").length,
      MEDIUM:   allEvents.filter(e => e.severity === "MEDIUM").length,
      LOW:      allEvents.filter(e => e.severity === "LOW").length,
    },
    sagco_command: "python BOARD-28-FIREFOX-DEV-PLUGIN/src/firefox_event_ingester.py --file firefox-events.json --emit-cases",
    events: allEvents,
  };

  const payload = JSON.stringify(export_doc, null, 2);
  const blob    = new Blob([payload], { type: "application/json" });
  const url     = URL.createObjectURL(blob);

  await browser.downloads.download({
    url,
    filename: `sagco-firefox-events-${Date.now()}.json`,
    saveAs: true,
  });
});

loadEvents();
