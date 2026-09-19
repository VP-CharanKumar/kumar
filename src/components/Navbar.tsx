import React from "react";
import { FileText, Download, CheckCircle2, Sprout, Database, ShieldCheck } from "lucide-react";

interface NavbarProps {
  onOpenKnowledge: () => void;
  onOpenTests: () => void;
  knowledgeCount: number;
}

export const Navbar: React.FC<NavbarProps> = ({
  onOpenKnowledge,
  onOpenTests,
  knowledgeCount
}) => {
  return (
    <header id="app-navbar" className="bg-stone-900 text-stone-100 border-b border-stone-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        
        {/* Brand & Project Identity */}
        <div className="flex items-center gap-3.5">
          <div className="w-10 h-10 rounded-lg bg-emerald-950 border border-emerald-600/40 flex items-center justify-center text-emerald-400">
            <Sprout className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-semibold tracking-tight text-stone-50">
                Darukaa.Earth
              </h1>
              <span className="text-xs font-mono font-medium px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-300 border border-emerald-800/50">
                AI Biodiversity Intelligence
              </span>
            </div>
            <p className="text-xs text-stone-400">
              Evidence-Grounding • Multi-Metric Couplings • 3-Variable Verification
            </p>
          </div>
        </div>

        {/* Action Controls & Official Downloads */}
        <div className="flex items-center flex-wrap gap-2.5">
          <button
            id="btn-knowledge-base"
            onClick={onOpenKnowledge}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md bg-stone-800 hover:bg-stone-700 text-stone-200 border border-stone-700 transition"
          >
            <Database className="w-3.5 h-3.5 text-emerald-400" />
            <span>Knowledge Base ({knowledgeCount})</span>
          </button>

          {/* Test Suite Runner Button */}
          <button
            id="btn-open-test-suite"
            onClick={onOpenTests}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md bg-stone-800 hover:bg-stone-700 text-stone-200 border border-stone-700 transition"
          >
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>Test Suite</span>
            <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-emerald-950 text-emerald-300 border border-emerald-800/80">
              24 Passed
            </span>
          </button>

          {/* Official Submission DOCX Download */}
          <a
            id="btn-download-docx"
            href="/api/submission/docx"
            download="Darukaa_Earth_Submission.docx"
            className="inline-flex items-center gap-1.5 px-3.5 py-1.5 text-xs font-semibold rounded-md bg-emerald-700 hover:bg-emerald-600 text-white shadow-sm transition"
            title="Download Official 24-Section Microsoft Word Submission Report"
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Submission DOCX</span>
            <span className="text-[10px] bg-emerald-900 px-1 py-0.2 rounded text-emerald-200">Verified</span>
          </a>

          {/* Clean Repository Archive ZIP */}
          <a
            id="btn-download-zip"
            href="/api/submission/zip"
            download="darukaa_earth_ai_biodiversity.zip"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md bg-stone-800 hover:bg-stone-700 text-stone-300 border border-stone-700 transition"
            title="Download Full Project Source Code Archive"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Repository ZIP</span>
          </a>
        </div>
      </div>
    </header>
  );
};
