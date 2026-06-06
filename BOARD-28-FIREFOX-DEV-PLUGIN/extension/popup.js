"use strict";

async function render() {
  const data   = await browser.storage.local.get("sagco_events");
  const events = data.sagco_events || [];

  document.getElementById("n-critical").textContent = events.filter(e => e.severity === "CRITICAL").length;
  document.getElementById("n-high").textContent     = events.filter(e => e.severity === "HIGH").length;
  document.getElementById("n-medium").textContent   = events.filter(e => e.severity === "MEDIUM").length;
  document.getElementById("n-low").textContent      = events.filter(e => e.severity === "LOW").length;

  const list = document.getElementById("event-list");
  list.innerHTML = "";
  [...events].reverse().slice(0, 30).forEach(e => {
    const div = document.createElement("div");
    div.className = "event";
    const t = new Date(e.ts).toLocaleTimeString();
    div.innerHTML = `<span class="ts">${t}</span> <span class="ab">${e.antibody || "?"}</span> [${e.district || "?"}]`;
    list.appendChild(div);
  });
}

document.getElementById("export").addEventListener("click", async () => {
  const data   = await browser.storage.local.get("sagco_events");
  const events = data.sagco_events || [];
  const doc = {
    exported_at:  new Date().toISOString(),
    board:        "BOARD-28-FIREFOX-DEV-PLUGIN",
    total_events: events.length,
    sagco_command: "python BOARD-28-FIREFOX-DEV-PLUGIN/src/firefox_event_ingester.py --file sagco-firefox-events.json --emit-cases --emit-citizens",
    events,
  };
  const blob = new Blob([JSON.stringify(doc, null, 2)], { type: "application/json" });
  const url  = URL.createObjectURL(blob);
  await browser.downloads.download({
    url,
    filename: `sagco-firefox-events-${Date.now()}.json`,
    saveAs: true,
  });
});

document.getElementById("clear").addEventListener("click", async () => {
  await browser.storage.local.set({ sagco_events: [] });
  render();
});

render();
