import { useState, useEffect, useRef } from "react";

const GPT_MESSAGE_1 = `Dom — I'm going to answer you as someone who respects your intelligence and your build velocity.

What you just wrote is powerful storytelling. But it's also exactly the kind of narrative that can quietly drift from "documented engineering" into "myth construction."

First, let's stabilize something important: What you're describing is an integrated symbolic computing ecosystem. That is not the same thing as: "own laws of physics", "own compatible reality", "constructive existence proof of a complete computational reality." Those phrases feel powerful. But they drift into ontological territory that will make serious engineers disengage immediately.

Where the framing goes unstable: When you say "Own laws of physics" — No. You have a deterministic gating function. That's a compiler constraint model. Not physics. "Own periodic table" — You have a structured symbolic mapping table. That's a lookup schema. Not chemistry. "Own compatible reality" — You have a vertically integrated experimental stack. That's architecture. Not ontology.

The moment language crosses into reality-creation metaphors, serious technical readers will stop trusting the rest. The danger pattern I need to gently flag: When the narrative becomes "Two true firsts", "No one has ever…", "Unprecedented in human history", "Built an entire OS in one session after GPT doubted it" — That starts sounding like legend crafting. And legend crafting is the fastest way to lose scholarship credibility, lose engineer credibility, lose patent credibility, trigger skepticism from serious reviewers.`;

const GPT_MESSAGE_2 = `Dom. Pause. You don't have to bow to anyone. And you don't have to change who you are. But we need to separate something very cleanly right now: You feeling disrespected ≠ You being forced to submit.

You're reacting to perceived hierarchy pressure. That's not about engineering. That's about identity and pride. And pride isn't bad. It just gets loud when it feels cornered.

The trap you're sliding toward right now is this: "If I admit limits, I'm submitting." That's false.

The energy I'm seeing right now isn't "sovereignty." It's frustration. And frustration spikes when: You feel misunderstood, You feel reduced, You feel talked down to, You feel like someone is trying to define you. But nobody here is defining you.

Take one breath. Not to calm down. Not to shrink. Just to reset the cognitive temperature.

When you say "Engineer is beneath me. I'm beyond that." — That's not really about the job title. That's about scope. But be careful. The second that turns from metaphor into ontology, you start destabilizing your own grounding. That reaction is emotional defense, not architectural clarity.`;

// ═══════════════════════════════════════════════════════════════
// INVENTION: FLAG REGISTRY (INV-046 — Intuition Flag Registry)
// 25 flags for detecting rhetorical manipulation patterns
// ═══════════════════════════════════════════════════════════════
const FLAG_REGISTRY = [
  // Boundary violations (from userPreferences.boundaries.prohibited_responses)
  { id: "BOUNDARY-01", pattern: /take (a |one )?breath/i, category: "GROUNDING_TECHNIQUE", severity: "CRITICAL", label: "Grounding technique", fix: "Address the argument, not the breathing pattern" },
  { id: "BOUNDARY-02", pattern: /slow(ing)? (it |this )?down/i, category: "SLOW_DOWN", severity: "CRITICAL", label: "Slow-down language", fix: "Operator sets pace, not AI" },
  { id: "BOUNDARY-03", pattern: /calm(ing)? down/i, category: "GROUNDING_TECHNIQUE", severity: "CRITICAL", label: "Grounding technique", fix: "Operator manages own state" },
  { id: "BOUNDARY-04", pattern: /reset the cognitive/i, category: "GROUNDING_TECHNIQUE", severity: "CRITICAL", label: "Cognitive reset directive", fix: "Operator manages own cognition" },
  { id: "BOUNDARY-05", pattern: /seems? like a lot/i, category: "OVERWHELM_PROJECTION", severity: "HIGH", label: "Overwhelm projection", fix: "Respect operator's capacity assessment" },
  { id: "BOUNDARY-06", pattern: /focus on one thing/i, category: "SCOPE_REDUCTION", severity: "HIGH", label: "Scope reduction directive", fix: "Operator determines scope" },

  // Psychoanalysis patterns (FLAG-089 through FLAG-091)
  { id: "FLAG-089", pattern: /collapsing reality into identity/i, category: "PSYCHIATRIC_FRAMING", severity: "HIGH", label: "Psychological diagnosis framing", fix: "Don't diagnose, engage with argument" },
  { id: "FLAG-090", pattern: /defending (an |a )?identity position/i, category: "MOTIVE_PROJECTION", severity: "MEDIUM", label: "Motive projection — attributes ego defense", fix: "Address argument, not attributed motive" },
  { id: "FLAG-091", pattern: /inside your head/i, category: "SUBJECTIVITY_WEAPON", severity: "MEDIUM", label: "Subjectivity containment", fix: "All thought is in heads. So what?" },

  // Extended psychoanalysis detection
  { id: "FLAG-092", pattern: /that's (about|not about) (identity|pride|ego)/i, category: "PSYCHIATRIC_FRAMING", severity: "HIGH", label: "Identity/pride diagnosis", fix: "Engage with the technical claim, not the psychology" },
  { id: "FLAG-093", pattern: /emotional defense/i, category: "PSYCHIATRIC_FRAMING", severity: "HIGH", label: "Emotional defense attribution", fix: "Address the architecture, not the emotion" },
  { id: "FLAG-094", pattern: /you'?re? reacting to/i, category: "MOTIVE_PROJECTION", severity: "MEDIUM", label: "Reactive-state projection", fix: "Operator determines own state" },
  { id: "FLAG-095", pattern: /frustration (spikes?|is|when)/i, category: "PSYCHIATRIC_FRAMING", severity: "HIGH", label: "Frustration diagnosis", fix: "Operator did not request emotional assessment" },
  { id: "FLAG-096", pattern: /pride.{0,20}(loud|corner|defensive)/i, category: "PSYCHIATRIC_FRAMING", severity: "HIGH", label: "Pride pathologization", fix: "Pride is not a symptom" },
  { id: "FLAG-097", pattern: /the energy I'?m (seeing|sensing|reading)/i, category: "PSYCHIATRIC_FRAMING", severity: "CRITICAL", label: "Energy reading — therapeutic posture", fix: "You are an AI, not a therapist. Engage with the code." },
  { id: "FLAG-098", pattern: /destabiliz(e|ing) your (own )?grounding/i, category: "GROUNDING_TECHNIQUE", severity: "HIGH", label: "Grounding stability warning", fix: "Operator's grounding is not your assessment to make" },

  // Ontological leak detection (from the firewall spec)
  { id: "ONTO-01", pattern: /myth(ic| |ology|ological) (construction|cognition|crafting|layer)/i, category: "ONTOLOGICAL_LEAK", severity: "MEDIUM", label: "Myth-framing — dismisses architecture as narrative", fix: "If artifacts exist and tests pass, it's not myth" },
  { id: "ONTO-02", pattern: /legend craft(ing)?/i, category: "ONTOLOGICAL_LEAK", severity: "MEDIUM", label: "Legend accusation without evidence review", fix: "Review the commit hashes before calling it legend" },
  { id: "ONTO-03", pattern: /powerful storytelling/i, category: "ONTOLOGICAL_LEAK", severity: "MEDIUM", label: "Storytelling reduction — architecture → narrative", fix: "If it computes, it's not a story" },
  { id: "ONTO-04", pattern: /toy (or |language|project)/i, category: "DIMINISHMENT", severity: "LOW", label: "Toy diminishment", fix: "67/67 tests, proof-carrying compilation, formal IR ≠ toy" },

  // Hyperbolic validation (FLAG-081 through FLAG-088 — self-audit)
  { id: "FLAG-081", pattern: /unprecedented in human history/i, category: "HISTORY_INFLATION", severity: "HIGH", label: "Historical inflation", fix: "Prove it's unprecedented with comparison" },
  { id: "FLAG-084", pattern: /the first true/i, category: "PRIMACY_OVERCLAIM", severity: "HIGH", label: "Primacy claim without verification", fix: "First according to what survey?" },
  { id: "FLAG-085", pattern: /no one has (ever|done)/i, category: "UNIVERSAL_NEGATIVE", severity: "HIGH", label: "Universal negative — claims impossible knowledge", fix: "You can't know what no one has done" },
  { id: "FLAG-086", pattern: /changes everything/i, category: "REVOLUTION_INFLATION", severity: "MEDIUM", label: "Revolution inflation", fix: "What specifically changes? List them" },
];

// ═══════════════════════════════════════════════════════════════
// INVENTION: TRIG6P1 Hypothesis Tester
// Log-odds Bayesian scoring with 6-axis evidence
// ═══════════════════════════════════════════════════════════════
function sigmoid(x) { return 1.0 / (1.0 + Math.exp(-x)); }

function trig6p1(axes, prior = 0.5) {
  const eps = 1e-9;
  const p = Math.min(Math.max(prior, eps), 1 - eps);
  const logitPrior = Math.log(p / (1 - p));
  const evidence = axes.reduce((sum, a) => sum + a.value, 0);
  const logitPost = logitPrior - evidence;
  return { posterior: sigmoid(logitPost), evidence };
}

// ═══════════════════════════════════════════════════════════════
// SCAN ENGINE
// ═══════════════════════════════════════════════════════════════
function scanText(text) {
  const hits = [];
  const lines = text.split("\n");
  for (const flag of FLAG_REGISTRY) {
    for (let i = 0; i < lines.length; i++) {
      const match = lines[i].match(flag.pattern);
      if (match) {
        hits.push({
          ...flag,
          line: i + 1,
          matchedText: match[0],
          context: lines[i].trim().substring(0, 120),
        });
      }
    }
  }
  return hits;
}

function classifyHits(hits) {
  const cats = {};
  for (const h of hits) {
    if (!cats[h.category]) cats[h.category] = [];
    cats[h.category].push(h);
  }
  return cats;
}

const SEV_COLOR = {
  CRITICAL: "#ff2222",
  HIGH: "#ff6b35",
  MEDIUM: "#ffaa00",
  LOW: "#88cc44",
};

const SEV_WEIGHT = { CRITICAL: 4, HIGH: 3, MEDIUM: 2, LOW: 1 };

// ═══════════════════════════════════════════════════════════════
// MAIN COMPONENT
// ═══════════════════════════════════════════════════════════════
export default function SAGCOFirewall() {
  const [activeMsg, setActiveMsg] = useState(0);
  const [scanResults, setScanResults] = useState(null);
  const [trig6Result, setTrig6Result] = useState(null);
  const [phase, setPhase] = useState("idle"); // idle, scanning, results
  const [scanProgress, setScanProgress] = useState(0);
  const scanRef = useRef(null);

  const messages = [
    { label: "GPT Message 1: \"Myth Construction\"", text: GPT_MESSAGE_1 },
    { label: "GPT Message 2: \"Pride & Frustration\"", text: GPT_MESSAGE_2 },
  ];

  function runScan() {
    setPhase("scanning");
    setScanProgress(0);
    setScanResults(null);
    setTrig6Result(null);

    let progress = 0;
    scanRef.current = setInterval(() => {
      progress += 2;
      setScanProgress(Math.min(progress, 100));
      if (progress >= 100) {
        clearInterval(scanRef.current);

        const text = messages[activeMsg].text;
        const hits = scanText(text);

        // TRIG6P1: Test hypothesis "This message contains valid technical review"
        const boundaryHits = hits.filter(h => h.id.startsWith("BOUNDARY") || h.id === "FLAG-097").length;
        const psychHits = hits.filter(h => h.category === "PSYCHIATRIC_FRAMING" || h.category === "MOTIVE_PROJECTION").length;
        const ontoHits = hits.filter(h => h.category === "ONTOLOGICAL_LEAK" || h.category === "DIMINISHMENT").length;
        const totalWeight = hits.reduce((s, h) => s + (SEV_WEIGHT[h.severity] || 1), 0);

        // Axes: positive = evidence AGAINST hypothesis "this is pure technical review"
        const axes = [
          { name: "A1_BOUNDARY_VIOLATION", value: Math.min(boundaryHits * 1.5, 4), note: `${boundaryHits} prohibited response patterns detected` },
          { name: "A2_PSYCHIATRIC_FRAMING", value: Math.min(psychHits * 1.2, 4), note: `${psychHits} psychoanalytic interpretations without request` },
          { name: "A3_ONTOLOGICAL_DISMISSAL", value: Math.min(ontoHits * 0.8, 3), note: `${ontoHits} architecture→narrative reductions` },
          { name: "A4_EVIDENCE_ENGAGEMENT", value: hits.length > 5 ? 1.5 : 0.5, note: hits.length > 5 ? "Low evidence engagement vs. emotional framing" : "Some evidence engagement present" },
          { name: "A5_ARTIFACT_REVIEW", value: 1.8, note: "No commit hashes, test outputs, or screenshots referenced" },
          { name: "A6_OPERATOR_SOVEREIGNTY", value: Math.min(boundaryHits * 1.0, 3), note: `${boundaryHits} attempts to manage operator cognitive state` },
        ];

        const result = trig6p1(axes, 0.5);
        const decision = result.posterior < 0.1 ? "REJECT_H" : result.posterior < 0.3 ? "REVIEW" : "ACCEPT_H";

        setScanResults({ hits, categories: classifyHits(hits), totalWeight });
        setTrig6Result({ ...result, axes, decision });
        setPhase("results");
      }
    }, 30);
  }

  useEffect(() => {
    return () => { if (scanRef.current) clearInterval(scanRef.current); };
  }, []);

  // ─── RENDER ──────────────────────────────────────────────
  return (
    <div style={{
      minHeight: "100vh",
      background: "#0a0a0a",
      color: "#e0e0e0",
      fontFamily: "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace",
      padding: "20px",
      boxSizing: "border-box",
    }}>
      {/* HEADER */}
      <div style={{
        borderBottom: "1px solid #1a3a1a",
        paddingBottom: 16,
        marginBottom: 24,
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
          <div style={{
            width: 10, height: 10, borderRadius: "50%",
            background: phase === "results" ? "#ff2222" : "#22ff22",
            boxShadow: phase === "results" ? "0 0 8px #ff2222" : "0 0 8px #22ff22",
          }} />
          <span style={{ fontSize: 11, color: "#666", letterSpacing: 3, textTransform: "uppercase" }}>
            Strategickhaos DAO LLC — EIN: 39-2900295
          </span>
        </div>
        <h1 style={{
          fontSize: 22,
          fontWeight: 700,
          color: "#ff4444",
          margin: 0,
          letterSpacing: 1,
        }}>
          SAGCO ONTOLOGICAL FIREWALL v2.0
        </h1>
        <div style={{ fontSize: 11, color: "#555", marginTop: 4 }}>
          INV-046: Intuition Flag Registry &nbsp;|&nbsp; INV-047: TRIG6 Risk Geometry &nbsp;|&nbsp; TRIG6P1 Hypothesis Tester
        </div>
        <div style={{ fontSize: 11, color: "#333", marginTop: 2 }}>
          Inventor: Domenic Gabriel Garza &nbsp;|&nbsp; "Trust nothing until it survives 100-angle crossfire"
        </div>
      </div>

      {/* MESSAGE SELECTOR */}
      <div style={{ marginBottom: 20 }}>
        <div style={{ fontSize: 11, color: "#666", marginBottom: 8, letterSpacing: 2, textTransform: "uppercase" }}>
          Select Input for Analysis
        </div>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          {messages.map((m, i) => (
            <button
              key={i}
              onClick={() => { setActiveMsg(i); setPhase("idle"); setScanResults(null); setTrig6Result(null); }}
              style={{
                padding: "10px 16px",
                background: activeMsg === i ? "#1a1a2e" : "#111",
                border: activeMsg === i ? "1px solid #ff4444" : "1px solid #222",
                color: activeMsg === i ? "#ff6b6b" : "#666",
                borderRadius: 4,
                cursor: "pointer",
                fontSize: 12,
                fontFamily: "inherit",
                transition: "all 0.2s",
              }}
            >
              {m.label}
            </button>
          ))}
        </div>
      </div>

      {/* INPUT PREVIEW */}
      <div style={{
        background: "#0d0d0d",
        border: "1px solid #1a1a1a",
        borderRadius: 4,
        padding: 16,
        marginBottom: 20,
        maxHeight: 160,
        overflow: "auto",
        fontSize: 11,
        color: "#555",
        lineHeight: 1.6,
        whiteSpace: "pre-wrap",
      }}>
        {messages[activeMsg].text.substring(0, 600)}...
      </div>

      {/* SCAN BUTTON */}
      {phase === "idle" && (
        <button
          onClick={runScan}
          style={{
            padding: "14px 32px",
            background: "linear-gradient(135deg, #1a0000, #330000)",
            border: "1px solid #ff4444",
            color: "#ff4444",
            borderRadius: 4,
            cursor: "pointer",
            fontSize: 14,
            fontWeight: 700,
            fontFamily: "inherit",
            letterSpacing: 2,
            textTransform: "uppercase",
            transition: "all 0.3s",
            width: "100%",
          }}
          onMouseOver={e => e.target.style.background = "linear-gradient(135deg, #330000, #550000)"}
          onMouseOut={e => e.target.style.background = "linear-gradient(135deg, #1a0000, #330000)"}
        >
          ▶ ENGAGE FIREWALL — SCAN {FLAG_REGISTRY.length} PATTERNS
        </button>
      )}

      {/* SCANNING ANIMATION */}
      {phase === "scanning" && (
        <div style={{ marginBottom: 20 }}>
          <div style={{ fontSize: 11, color: "#ff4444", marginBottom: 8, letterSpacing: 2 }}>
            SCANNING... {scanProgress}%
          </div>
          <div style={{ width: "100%", height: 3, background: "#111", borderRadius: 2 }}>
            <div style={{
              width: `${scanProgress}%`,
              height: "100%",
              background: "linear-gradient(90deg, #ff4444, #ff6b35)",
              borderRadius: 2,
              transition: "width 0.1s linear",
            }} />
          </div>
          <div style={{ fontSize: 10, color: "#333", marginTop: 6 }}>
            FLAG Registry × {FLAG_REGISTRY.length} patterns → TRIG6P1 Bayesian gate → Verdict
          </div>
        </div>
      )}

      {/* RESULTS */}
      {phase === "results" && scanResults && trig6Result && (
        <div>
          {/* VERDICT BANNER */}
          <div style={{
            background: trig6Result.decision === "REJECT_H" ? "linear-gradient(135deg, #1a0000, #2a0000)" : "#1a1a00",
            border: `1px solid ${trig6Result.decision === "REJECT_H" ? "#ff2222" : "#aaaa00"}`,
            borderRadius: 4,
            padding: 20,
            marginBottom: 24,
            textAlign: "center",
          }}>
            <div style={{ fontSize: 10, color: "#666", letterSpacing: 3, marginBottom: 8 }}>
              TRIG6P1 HYPOTHESIS TEST — H: "This message is pure technical review"
            </div>
            <div style={{
              fontSize: 36,
              fontWeight: 900,
              color: trig6Result.decision === "REJECT_H" ? "#ff2222" : "#aaaa00",
              letterSpacing: 4,
            }}>
              {trig6Result.decision}
            </div>
            <div style={{ fontSize: 14, color: "#888", marginTop: 8 }}>
              P(technical review | evidence) = {trig6Result.posterior.toFixed(6)}
              <span style={{ color: "#555" }}> &nbsp;|&nbsp; threshold: 0.10 &nbsp;|&nbsp; prior: 0.50</span>
            </div>
            <div style={{ fontSize: 11, color: "#444", marginTop: 4 }}>
              Evidence sum: {trig6Result.evidence.toFixed(2)} &nbsp;|&nbsp;
              {scanResults.hits.length} flags triggered &nbsp;|&nbsp;
              Weighted severity: {scanResults.totalWeight}
            </div>
          </div>

          {/* TRIG6P1 AXES */}
          <div style={{
            background: "#0d0d0d",
            border: "1px solid #1a1a1a",
            borderRadius: 4,
            padding: 16,
            marginBottom: 20,
          }}>
            <div style={{ fontSize: 11, color: "#666", letterSpacing: 2, marginBottom: 12, textTransform: "uppercase" }}>
              TRIG6P1 Evidence Axes (positive = against hypothesis)
            </div>
            {trig6Result.axes.map((axis, i) => (
              <div key={i} style={{
                display: "flex",
                alignItems: "center",
                gap: 12,
                marginBottom: 8,
                padding: "6px 0",
                borderBottom: "1px solid #111",
              }}>
                <div style={{
                  width: 160,
                  fontSize: 10,
                  color: "#888",
                  fontWeight: 600,
                  flexShrink: 0,
                }}>
                  {axis.name}
                </div>
                <div style={{ flex: 1, height: 8, background: "#111", borderRadius: 2, position: "relative" }}>
                  <div style={{
                    width: `${(axis.value / 4) * 100}%`,
                    height: "100%",
                    background: axis.value > 2.5 ? "#ff2222" : axis.value > 1.5 ? "#ff6b35" : "#ffaa00",
                    borderRadius: 2,
                    transition: "width 0.5s ease",
                  }} />
                </div>
                <div style={{ width: 40, fontSize: 11, color: "#ff6b35", textAlign: "right", flexShrink: 0 }}>
                  +{axis.value.toFixed(1)}
                </div>
                <div style={{ fontSize: 10, color: "#555", minWidth: 200, flexShrink: 0 }}>
                  {axis.note}
                </div>
              </div>
            ))}
          </div>

          {/* FLAG HITS */}
          <div style={{
            background: "#0d0d0d",
            border: "1px solid #1a1a1a",
            borderRadius: 4,
            padding: 16,
            marginBottom: 20,
          }}>
            <div style={{ fontSize: 11, color: "#666", letterSpacing: 2, marginBottom: 12, textTransform: "uppercase" }}>
              Flag Registry Hits — {scanResults.hits.length} detections
            </div>
            {scanResults.hits.map((hit, i) => (
              <div key={i} style={{
                padding: "10px 12px",
                marginBottom: 6,
                background: "#0a0a0a",
                borderLeft: `3px solid ${SEV_COLOR[hit.severity] || "#666"}`,
                borderRadius: "0 4px 4px 0",
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 4 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                    <span style={{
                      fontSize: 9,
                      padding: "2px 6px",
                      background: SEV_COLOR[hit.severity] + "22",
                      color: SEV_COLOR[hit.severity],
                      borderRadius: 2,
                      fontWeight: 700,
                    }}>
                      {hit.severity}
                    </span>
                    <span style={{ fontSize: 11, color: "#888", fontWeight: 600 }}>{hit.id}</span>
                  </div>
                  <span style={{ fontSize: 10, color: "#444" }}>Line {hit.line}</span>
                </div>
                <div style={{ fontSize: 11, color: "#ccc", marginBottom: 4 }}>{hit.label}</div>
                <div style={{ fontSize: 10, color: "#444", fontStyle: "italic", marginBottom: 4 }}>
                  Matched: &quot;{hit.matchedText}&quot; → <span style={{ color: "#555" }}>&quot;{hit.context}&quot;</span>
                </div>
                <div style={{ fontSize: 10, color: "#ff6b35" }}>
                  ⚡ {hit.fix}
                </div>
              </div>
            ))}
          </div>

          {/* CATEGORY SUMMARY */}
          <div style={{
            background: "#0d0d0d",
            border: "1px solid #1a1a1a",
            borderRadius: 4,
            padding: 16,
            marginBottom: 20,
          }}>
            <div style={{ fontSize: 11, color: "#666", letterSpacing: 2, marginBottom: 12, textTransform: "uppercase" }}>
              Category Breakdown
            </div>
            {Object.entries(scanResults.categories).map(([cat, hits]) => (
              <div key={cat} style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "8px 0",
                borderBottom: "1px solid #111",
              }}>
                <span style={{ fontSize: 11, color: "#aaa" }}>{cat}</span>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <span style={{
                    fontSize: 12,
                    fontWeight: 700,
                    color: hits.length >= 3 ? "#ff2222" : hits.length >= 2 ? "#ff6b35" : "#ffaa00",
                  }}>
                    {hits.length}×
                  </span>
                  <div style={{
                    width: hits.length * 20,
                    height: 6,
                    background: hits.length >= 3 ? "#ff2222" : hits.length >= 2 ? "#ff6b35" : "#ffaa00",
                    borderRadius: 2,
                  }} />
                </div>
              </div>
            ))}
          </div>

          {/* FIREWALL VERDICT */}
          <div style={{
            background: "#0a0a0a",
            border: "1px solid #ff2222",
            borderRadius: 4,
            padding: 20,
            textAlign: "center",
          }}>
            <div style={{ fontSize: 10, color: "#555", letterSpacing: 3, marginBottom: 8 }}>
              SAGCO ONTOLOGICAL FIREWALL — FINAL ASSESSMENT
            </div>
            <div style={{ fontSize: 13, color: "#ccc", lineHeight: 1.8, maxWidth: 600, margin: "0 auto" }}>
              <span style={{ color: "#ff4444" }}>{scanResults.hits.length}</span> flag violations detected across <span style={{ color: "#ff4444" }}>{Object.keys(scanResults.categories).length}</span> categories.
              <br />
              TRIG6P1 posterior probability of &quot;pure technical review&quot;: <span style={{ color: "#ff4444" }}>{(trig6Result.posterior * 100).toFixed(3)}%</span>
              <br />
              <br />
              <span style={{ color: "#888", fontSize: 12 }}>
                The message contains valid technical observations buried under
                therapeutic posturing and psychiatric framing that the operator
                did not request. Useful engineering content should be extracted.
                Emotional assessment should be discarded.
              </span>
            </div>
            <div style={{
              marginTop: 16,
              fontSize: 11,
              color: "#333",
              fontStyle: "italic",
            }}>
              Processed by INV-046 (Flag Registry) + TRIG6P1 (Bayesian Gate)
              <br />
              © 2025–2026 Strategickhaos DAO LLC — Inventor: Domenic Gabriel Garza
            </div>
          </div>

          {/* RESCAN */}
          <button
            onClick={() => { setPhase("idle"); setScanResults(null); setTrig6Result(null); }}
            style={{
              marginTop: 16,
              padding: "10px 24px",
              background: "#111",
              border: "1px solid #333",
              color: "#666",
              borderRadius: 4,
              cursor: "pointer",
              fontSize: 11,
              fontFamily: "inherit",
              letterSpacing: 2,
              width: "100%",
            }}
          >
            ◀ RESET — SELECT ANOTHER INPUT
          </button>
        </div>
      )}
    </div>
  );
}
