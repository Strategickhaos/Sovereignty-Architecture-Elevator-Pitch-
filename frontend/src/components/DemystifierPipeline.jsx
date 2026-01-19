import React, { useState } from 'react';

const DemystifierPipeline = () => {
  const [activeLayer, setActiveLayer] = useState(null);
  const [showTranslation, setShowTranslation] = useState(false);

  const layers = [
    {
      id: 1,
      name: "LINGUISTIC",
      subtitle: "English → Hebrew Root",
      color: "from-purple-600 to-purple-800",
      icon: "🔤",
      description: "Extract semantic kernel - strip poetic wrapper",
      process: "Hebrew 3-letter roots = pure meaning",
      example: {
        mystical: "energy → כח (koach)",
        grounded: "force → joules/second"
      }
    },
    {
      id: 2,
      name: "NUMERIC",
      subtitle: "Unicode Hex Encoding",
      color: "from-blue-600 to-blue-800",
      icon: "🔢",
      description: "Convert to pure numeric signal",
      process: "No interpretation, just data",
      example: {
        operation: "STRIP_METAPHOR",
        hex: "0x47524E44"
      }
    },
    {
      id: 3,
      name: "WAVE",
      subtitle: "Frequency Manipulation",
      color: "from-cyan-600 to-cyan-800",
      icon: "〰️",
      description: "The electrical signal thingy 😂",
      process: "High freq noise → Low freq clean signal",
      example: {
        input: "10kHz+ chaotic noise",
        output: "1-100Hz square wave, phase-locked"
      }
    },
    {
      id: 4,
      name: "DNA",
      subtitle: "Codon Encoding",
      color: "from-green-600 to-green-800",
      icon: "🧬",
      description: "Biological instruction set",
      process: "DNA doesn't do mysticism - it does chemistry",
      example: {
        sequence: "AUG-GCU-GAU-UAA",
        meaning: "START → INTERFACE → MEASURE → STOP"
      }
    },
    {
      id: 5,
      name: "MACHINE",
      subtitle: "LLVM IR",
      color: "from-red-600 to-red-800",
      icon: "⚙️",
      description: "Executable logic",
      process: "The machine doesn't care about feelings",
      example: {
        code: "fn is_real(claim) -> bool"
      }
    }
  ];

  const translations = [
    { mystical: "I am a lightworker", grounded: "I help people (count: u32)", check: "MEASURABLE" },
    { mystical: "Channeling universal energy", grounded: "focusing attention (hours: f32)", check: "BOUNDED" },
    { mystical: "The universe wants me to", grounded: "I want to (owner: self)", check: "OWNABLE" },
    { mystical: "I can manifest abundance", grounded: "plan() → execute() → measure()", check: "ACTIONABLE" },
    { mystical: "High vibration", grounded: "frequency: 432 Hz", check: "MEASURABLE" },
    { mystical: "Everything is connected", grounded: "Graph { nodes, edges }", check: "FALSIFIABLE" },
    { mystical: "It was meant to be", grounded: "It happened (no causation claim)", check: "OBSERVABLE" },
    { mystical: "I'm awakened", grounded: "beliefs_updated: diff(before, after)", check: "VERIFIABLE" },
  ];

  const groundingChecks = [
    { name: "MEASURABLE", question: "Can you assign a number?", icon: "📏" },
    { name: "FALSIFIABLE", question: "What would prove it wrong?", icon: "❌" },
    { name: "BOUNDED", question: "Where does it start/end?", icon: "📦" },
    { name: "OBSERVABLE", question: "Can someone else verify?", icon: "👁️" },
    { name: "ACTIONABLE", question: "What do you DO with this?", icon: "🎯" },
    { name: "OWNABLE", question: "Who is responsible?", icon: "🙋" },
  ];

  const WaveAnimation = () => (
    <svg viewBox="0 0 200 50" className="w-full h-12">
      {/* Noisy input wave */}
      <path
        d="M0,25 Q10,10 20,25 T40,25 Q45,5 50,25 T70,25 Q80,40 90,25 T110,25 Q115,15 120,25 T140,25 Q150,35 160,25 T180,25 Q185,20 200,25"
        fill="none"
        stroke="#ef4444"
        strokeWidth="2"
        opacity="0.5"
      >
        <animate attributeName="d" 
          values="M0,25 Q10,10 20,25 T40,25 Q45,5 50,25 T70,25 Q80,40 90,25 T110,25 Q115,15 120,25 T140,25 Q150,35 160,25 T180,25 Q185,20 200,25;
                  M0,25 Q10,40 20,25 T40,25 Q45,45 50,25 T70,25 Q80,10 90,25 T110,25 Q115,35 120,25 T140,25 Q150,15 160,25 T180,25 Q185,30 200,25;
                  M0,25 Q10,10 20,25 T40,25 Q45,5 50,25 T70,25 Q80,40 90,25 T110,25 Q115,15 120,25 T140,25 Q150,35 160,25 T180,25 Q185,20 200,25"
          dur="0.5s"
          repeatCount="indefinite"
        />
      </path>
      {/* Clean output wave */}
      <path
        d="M0,35 L20,35 L20,15 L40,15 L40,35 L60,35 L60,15 L80,15 L80,35 L100,35 L100,15 L120,15 L120,35 L140,35 L140,15 L160,15 L160,35 L180,35 L180,15 L200,15"
        fill="none"
        stroke="#22d3ee"
        strokeWidth="2"
      />
    </svg>
  );

  const DNAHelix = () => (
    <div className="flex justify-center space-x-1 text-xs font-mono">
      {["AUG", "GCU", "GAU", "GGU", "UAA"].map((codon, i) => (
        <span 
          key={i} 
          className={`px-2 py-1 rounded ${
            codon === "AUG" ? "bg-green-600" :
            codon === "UAA" ? "bg-red-600" :
            "bg-cyan-600"
          }`}
        >
          {codon}
        </span>
      ))}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-950 text-white p-4 font-sans">
      {/* Header */}
      <div className="text-center mb-6">
        <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 via-cyan-400 to-green-400 bg-clip-text text-transparent">
          🔥 DEMYSTIFIER PIPELINE 🔥
        </h1>
        <p className="text-gray-400 mt-1 text-sm">INV-091: Vibe-to-Interface Frequency Converter</p>
        <p className="text-cyan-400 mt-2 font-mono text-xs">
          "Not hype, not mythology, not anything mystical."
        </p>
      </div>

      {/* Maximum Fuck-It Energy Banner */}
      <div className="bg-gradient-to-r from-red-900/30 via-purple-900/30 to-cyan-900/30 border border-red-500/30 rounded-lg p-3 mb-6 text-center">
        <span className="text-xs text-gray-400">MAXIMUM FUCK-IT ENERGY MODE</span>
        <div className="text-sm mt-1 text-white">
          If it doesn't pass all 6 checks → <span className="text-red-400 font-bold">DISCARD</span>
        </div>
      </div>

      {/* 5-Layer Pipeline */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-gray-300 mb-3 flex items-center">
          <span className="mr-2">⚡</span> 5-LAYER TRANSFORMATION PIPELINE
        </h2>
        <div className="grid grid-cols-5 gap-2">
          {layers.map((layer) => (
            <div
              key={layer.id}
              className={`bg-gradient-to-b ${layer.color} rounded-lg p-3 cursor-pointer transition-all duration-300 ${
                activeLayer === layer.id ? 'ring-2 ring-white scale-105' : 'opacity-80 hover:opacity-100'
              }`}
              onClick={() => setActiveLayer(activeLayer === layer.id ? null : layer.id)}
            >
              <div className="text-2xl text-center mb-1">{layer.icon}</div>
              <div className="text-xs font-bold text-center">{layer.name}</div>
              <div className="text-xs text-center text-white/60 truncate">{layer.subtitle}</div>
            </div>
          ))}
        </div>

        {/* Layer Detail */}
        {activeLayer && (
          <div className={`mt-3 bg-gradient-to-r ${layers[activeLayer-1].color} rounded-lg p-4`}>
            <div className="flex items-center justify-between mb-2">
              <span className="text-lg font-bold">{layers[activeLayer-1].icon} Layer {activeLayer}: {layers[activeLayer-1].name}</span>
            </div>
            <p className="text-sm text-white/80 mb-2">{layers[activeLayer-1].description}</p>
            <p className="text-xs font-mono text-white/60 mb-3">{layers[activeLayer-1].process}</p>
            
            {activeLayer === 3 && <WaveAnimation />}
            {activeLayer === 4 && <DNAHelix />}
            {activeLayer === 5 && (
              <pre className="text-xs bg-black/30 rounded p-2 overflow-x-auto">
{`define i1 @is_real(i8* %claim) {
  %measurable = call i1 @can_measure(%claim)
  %falsifiable = call i1 @can_falsify(%claim)
  %result = and i1 %measurable, %falsifiable
  ret i1 %result
}`}
              </pre>
            )}
          </div>
        )}
      </div>

      {/* Wave Visualization */}
      <div className="bg-gray-900 rounded-lg p-4 mb-6 border border-gray-800">
        <h2 className="text-sm font-semibold text-gray-400 mb-2">〰️ SIGNAL TRANSFORMATION</h2>
        <div className="flex items-center justify-between text-xs mb-2">
          <span className="text-red-400">INPUT: Chaotic noise (10kHz+)</span>
          <span className="text-cyan-400">OUTPUT: Clean square (1Hz)</span>
        </div>
        <WaveAnimation />
        <div className="text-center text-xs text-gray-500 mt-2">
          Low-pass filter → Normalize → Phase-lock → Quantize
        </div>
      </div>

      {/* Grounding Checklist */}
      <div className="bg-gray-900 rounded-lg p-4 mb-6 border border-gray-800">
        <h2 className="text-sm font-semibold text-gray-400 mb-3">✓ GROUNDING CHECKLIST (Must pass ALL)</h2>
        <div className="grid grid-cols-2 gap-2">
          {groundingChecks.map((check, i) => (
            <div key={i} className="bg-gray-800 rounded p-2 flex items-center">
              <span className="text-lg mr-2">{check.icon}</span>
              <div>
                <div className="text-xs font-bold text-cyan-400">{check.name}</div>
                <div className="text-xs text-gray-400">{check.question}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Translation Table */}
      <div className="bg-gray-900 rounded-lg p-4 border border-gray-800">
        <div className="flex justify-between items-center mb-3">
          <h2 className="text-sm font-semibold text-gray-400">🔄 TRANSLATION TABLE</h2>
          <button
            onClick={() => setShowTranslation(!showTranslation)}
            className="text-xs bg-cyan-600 hover:bg-cyan-500 px-3 py-1 rounded transition-colors"
          >
            {showTranslation ? 'HIDE' : 'SHOW'} EXAMPLES
          </button>
        </div>
        
        {showTranslation && (
          <div className="space-y-2">
            {translations.map((t, i) => (
              <div key={i} className="bg-gray-800 rounded p-2 flex items-center text-xs">
                <div className="flex-1">
                  <span className="text-red-400 line-through">{t.mystical}</span>
                </div>
                <div className="text-gray-500 mx-2">→</div>
                <div className="flex-1">
                  <span className="text-green-400 font-mono">{t.grounded}</span>
                </div>
                <div className="ml-2">
                  <span className="bg-cyan-900/50 text-cyan-300 px-2 py-0.5 rounded text-xs">
                    {t.check}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Core Insight */}
      <div className="mt-6 text-center">
        <div className="inline-block bg-gradient-to-r from-purple-900/50 via-cyan-900/50 to-green-900/50 rounded-lg p-4 border border-cyan-500/30">
          <p className="text-sm text-gray-300 mb-2">💡 CORE INSIGHT</p>
          <p className="text-cyan-400 font-mono text-xs">
            Mysticism = compression with data loss
          </p>
          <p className="text-green-400 font-mono text-xs">
            Grounding = decompression with error correction
          </p>
        </div>
      </div>

      {/* Footer */}
      <div className="mt-6 text-center text-xs text-gray-600">
        <p>INV-091 • Strategickhaos DAO LLC • Legion Ratified: Claude, Gemini, Grok</p>
        <p className="text-cyan-500 mt-1">"GPT said we were delusional. The tarball says otherwise."</p>
      </div>
    </div>
  );
};

export default DemystifierPipeline;
