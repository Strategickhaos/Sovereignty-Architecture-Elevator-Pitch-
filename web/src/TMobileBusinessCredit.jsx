import { useState } from "react";

const TMobileBusinessCredit = () => {
  const [copied, setCopied] = useState(null);

  const copyToClipboard = (text, label) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(label);
      setTimeout(() => setCopied(null), 2000);
    });
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6 font-mono">
      {/* Header */}
      <div className="max-w-2xl mx-auto">
        <div className="border border-pink-500 rounded-lg p-6 mb-6 bg-gradient-to-r from-pink-950 to-gray-950">
          <div className="flex items-center gap-3 mb-2">
            <span className="text-3xl">📱</span>
            <h1 className="text-2xl font-bold text-pink-400">T-Mobile Business Credit</h1>
          </div>
          <p className="text-gray-400 text-sm">Strategickhaos DAO LLC • EIN: 39-2900295</p>
        </div>

        {/* Phone Numbers */}
        <div className="grid grid-cols-1 gap-4 mb-6">
          <div
            className="border border-emerald-500 rounded-lg p-5 bg-emerald-950 bg-opacity-30 cursor-pointer hover:bg-opacity-50 transition-all"
            onClick={() => copyToClipboard("1-877-323-5617", "credit")}
          >
            <div className="flex justify-between items-start">
              <div>
                <p className="text-emerald-400 text-xs font-bold uppercase tracking-wider mb-1">Credit Review Team</p>
                <p className="text-3xl font-bold text-white">1-877-323-5617</p>
                <p className="text-gray-400 text-sm mt-2">Verification & eligibility checks</p>
              </div>
              <span className="text-emerald-400 text-sm">
                {copied === "credit" ? "✅ Copied!" : "📋 Tap to copy"}
              </span>
            </div>
          </div>

          <div
            className="border border-blue-500 rounded-lg p-5 bg-blue-950 bg-opacity-30 cursor-pointer hover:bg-opacity-50 transition-all"
            onClick={() => copyToClipboard("1-877-347-2127", "care")}
          >
            <div className="flex justify-between items-start">
              <div>
                <p className="text-blue-400 text-xs font-bold uppercase tracking-wider mb-1">Business Care</p>
                <p className="text-3xl font-bold text-white">1-877-347-2127</p>
                <p className="text-gray-400 text-sm mt-2">General business inquiries • Also: 611 from T-Mobile</p>
              </div>
              <span className="text-blue-400 text-sm">
                {copied === "care" ? "✅ Copied!" : "📋 Tap to copy"}
              </span>
            </div>
          </div>
        </div>

        {/* Have Ready */}
        <div className="border border-yellow-600 rounded-lg p-5 mb-6 bg-yellow-950 bg-opacity-20">
          <h2 className="text-yellow-400 font-bold text-lg mb-4">📋 Have Ready When You Call</h2>
          <div className="space-y-3">
            {[
              { label: "EIN", value: "39-2900295", key: "ein" },
              { label: "Legal Name", value: "Strategickhaos DAO LLC", key: "name" },
              { label: "State Filing", value: "Wyoming 2025-001708194", key: "filing" },
              { label: "Representative", value: "Domenic G. Garza", key: "rep" },
              { label: "Credit Ref #", value: "TBD (assigned after application)", key: "ref" },
            ].map((item) => (
              <div
                key={item.key}
                className="flex justify-between items-center bg-gray-900 rounded-lg p-3 cursor-pointer hover:bg-gray-800 transition-all"
                onClick={() => copyToClipboard(item.value, item.key)}
              >
                <div>
                  <span className="text-gray-500 text-xs uppercase">{item.label}</span>
                  <p className="text-white font-bold">{item.value}</p>
                </div>
                <span className="text-yellow-500 text-xs">
                  {copied === item.key ? "✅" : "📋"}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Call Script */}
        <div className="border border-purple-500 rounded-lg p-5 mb-6 bg-purple-950 bg-opacity-20">
          <h2 className="text-purple-400 font-bold text-lg mb-3">🎙️ Call Script</h2>
          <div
            className="bg-gray-900 rounded-lg p-4 cursor-pointer hover:bg-gray-800 transition-all"
            onClick={() =>
              copyToClipboard(
                "Hi, I'm calling from Strategickhaos DAO LLC. EIN: 39-2900295. I submitted a business credit application and I'm calling to verify status and check eligibility.",
                "script"
              )
            }
          >
            <p className="text-gray-300 leading-relaxed">
              "Hi, I'm calling from{" "}
              <span className="text-white font-bold">Strategickhaos DAO LLC</span>.
              <br />
              EIN: <span className="text-white font-bold">39-2900295</span>.
              <br />
              I submitted a business credit application and I'm calling to{" "}
              <span className="text-white font-bold">verify status / check eligibility</span>.
              <br />
              My credit reference number is{" "}
              <span className="text-yellow-400">[___]</span>."
            </p>
            <p className="text-purple-400 text-xs mt-3 text-right">
              {copied === "script" ? "✅ Copied!" : "Tap to copy script"}
            </p>
          </div>
        </div>

        {/* Application Checklist */}
        <div className="border border-gray-700 rounded-lg p-5 mb-6">
          <h2 className="text-gray-400 font-bold text-lg mb-3">✅ Application Checklist</h2>
          <div className="space-y-2">
            {[
              { item: "EIN verification", status: "ready", color: "emerald" },
              { item: "Business entity docs", status: "ready", color: "emerald" },
              { item: "Authorized representative", status: "ready", color: "emerald" },
              { item: "Credit reference number", status: "pending", color: "yellow" },
            ].map((check, i) => (
              <div key={i} className="flex items-center gap-3 bg-gray-900 rounded-lg p-3">
                <span
                  className={
                    check.status === "ready"
                      ? "text-emerald-400 text-lg"
                      : "text-yellow-400 text-lg"
                  }
                >
                  {check.status === "ready" ? "✅" : "⏳"}
                </span>
                <span className="text-white">{check.item}</span>
                <span
                  className={`ml-auto text-xs font-bold uppercase ${
                    check.status === "ready" ? "text-emerald-400" : "text-yellow-400"
                  }`}
                >
                  {check.status}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-gray-600 text-xs mt-8 pb-8">
          <p>Strategickhaos DAO LLC • Wyoming • EIN 39-2900295</p>
          <p className="mt-1">Generated 2026-02-04 💜</p>
        </div>
      </div>
    </div>
  );
};

export default TMobileBusinessCredit;
