/**
 * SAGCO content script — intercepts console.warn on every page.
 * Captures Statsig gate failures, Grafana Faro sampling, partitioned-cookie
 * warnings, and Intercom/Frill disabled notices.
 */

"use strict";

const SAGCO_PATTERNS = [
  "[Statsig]",
  "[Intercom]",
  "isSampled",
  "partitioning is enabled",
  "third-party context",
  "Content-Security-Policy",
  "grafana",
  "faro",
];

const originalWarn  = console.warn.bind(console);
const originalError = console.error.bind(console);

function intercept(level, args) {
  const text = args.map(a => {
    try { return typeof a === "object" ? JSON.stringify(a) : String(a); }
    catch { return "[circular]"; }
  }).join(" ");

  if (SAGCO_PATTERNS.some(p => text.toLowerCase().includes(p.toLowerCase()))) {
    browser.runtime.sendMessage({
      type:   "sagco_console_event",
      source: level,
      text:   text.slice(0, 300),
      url:    window.location.href,
    }).catch(() => {});
  }
}

console.warn = (...args) => {
  intercept("warn", args);
  originalWarn(...args);
};

console.error = (...args) => {
  intercept("error", args);
  originalError(...args);
};
