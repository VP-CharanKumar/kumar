import React from "react";
import { RecommendationItem, MonitoringItem } from "../types";
import { CheckCircle2, Clock, ShieldCheck, AlertOctagon, LineChart, BookOpen, ChevronRight } from "lucide-react";

interface RecommendationsListProps {
  recommendations: RecommendationItem[];
  monitoringPlan: MonitoringItem[];
}

export const RecommendationsList: React.FC<RecommendationsListProps> = ({
  recommendations,
  monitoringPlan
}) => {
  if (recommendations.length === 0) {
    return null;
  }

  return (
    <div id="evidence-based-recommendations" className="space-y-4 text-stone-200">
      
      {/* Title */}
      <div className="flex items-center justify-between pb-2">
        <div>
          <h3 className="text-sm font-semibold text-stone-100 uppercase tracking-wide font-mono flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            Evidence-Based Interventions ({recommendations.length})
          </h3>
          <p className="text-xs text-stone-400 mt-0.5">
            Peer-reviewed scientific prescriptions with biological mechanisms and tradeoffs
          </p>
        </div>
      </div>

      {/* Recommendations Cards */}
      <div className="space-y-4">
        {recommendations.map((rec, idx) => (
          <div
            key={idx}
            className="bg-stone-900 border border-stone-800 rounded-xl p-5 shadow-sm space-y-3.5 hover:border-stone-700 transition"
          >
            {/* Header: Action & Badges */}
            <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-2.5 pb-2 border-b border-stone-800">
              <h4 className="text-sm font-semibold text-stone-100 leading-snug">
                {rec.action}
              </h4>
              
              <div className="flex items-center gap-2 shrink-0">
                {/* Time horizon badge */}
                <span className="inline-flex items-center gap-1 text-[11px] font-mono px-2 py-0.5 rounded bg-stone-800 text-stone-300 border border-stone-700">
                  <Clock className="w-3 h-3 text-stone-400" />
                  {rec.time_horizon}
                </span>

                {/* Confidence badge */}
                <span
                  className={`inline-flex items-center gap-1 text-[11px] font-mono px-2 py-0.5 rounded font-semibold border ${
                    rec.confidence === "HIGH"
                      ? "bg-emerald-950 text-emerald-300 border-emerald-800"
                      : rec.confidence === "MEDIUM"
                      ? "bg-amber-950 text-amber-300 border-amber-800"
                      : "bg-stone-800 text-stone-400 border-stone-700"
                  }`}
                >
                  <ShieldCheck className="w-3 h-3" />
                  {rec.confidence} Confidence
                </span>
              </div>
            </div>

            {/* Scientific Mechanism */}
            <div>
              <span className="text-xs font-semibold text-stone-300 uppercase tracking-wide font-mono block mb-1">
                Scientific Mechanism (Why it works):
              </span>
              <p className="text-xs text-stone-300 leading-relaxed bg-stone-950/60 p-3 rounded-lg border border-stone-800/80">
                {rec.why_it_works}
              </p>
            </div>

            {/* Impacted Metrics & Direction */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
              <div className="bg-stone-950/40 p-3 rounded-lg border border-stone-800/60">
                <span className="text-[11px] font-semibold text-stone-400 uppercase tracking-wider font-mono block mb-1.5 flex items-center gap-1">
                  <LineChart className="w-3.5 h-3.5 text-blue-400" />
                  Impacted Metrics & Improvement:
                </span>
                <ul className="space-y-1 text-xs text-stone-300">
                  {rec.impacted_metrics.map((m, i) => (
                    <li key={i} className="flex items-start gap-1.5">
                      <ChevronRight className="w-3 h-3 text-emerald-400 shrink-0 mt-0.5" />
                      <span>{m}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Tradeoffs */}
              <div className="bg-stone-950/40 p-3 rounded-lg border border-stone-800/60">
                <span className="text-[11px] font-semibold text-amber-400/90 uppercase tracking-wider font-mono block mb-1.5 flex items-center gap-1">
                  <AlertOctagon className="w-3.5 h-3.5 text-amber-400" />
                  Known Tradeoffs & Agronomic Limits:
                </span>
                <ul className="space-y-1 text-xs text-stone-300">
                  {rec.tradeoffs.map((t, i) => (
                    <li key={i} className="flex items-start gap-1.5 text-amber-200/90">
                      <ChevronRight className="w-3 h-3 text-amber-500 shrink-0 mt-0.5" />
                      <span>{t}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Verified Sources */}
            {rec.evidence.length > 0 && (
              <div className="pt-2 border-t border-stone-800/80 flex items-center flex-wrap gap-2 text-xs">
                <span className="text-stone-400 font-mono text-[11px] flex items-center gap-1">
                  <BookOpen className="w-3 h-3 text-emerald-400" />
                  Peer-Reviewed Citations:
                </span>
                {rec.evidence.map((src, i) => (
                  <span
                    key={i}
                    className="px-2 py-0.5 rounded bg-stone-950 text-emerald-400 font-mono text-[11px] border border-stone-800"
                  >
                    {src}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Monitoring Protocol Section */}
      {monitoringPlan.length > 0 && (
        <div className="bg-stone-900 border border-stone-800 rounded-xl p-5 shadow-sm space-y-3">
          <div className="flex items-center gap-2 pb-2 border-b border-stone-800">
            <LineChart className="w-4 h-4 text-emerald-400" />
            <h4 className="text-xs font-semibold text-stone-100 uppercase tracking-wide font-mono">
              Quantitative Monitoring Protocol
            </h4>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-stone-800 text-stone-400 font-mono text-[11px]">
                  <th className="pb-2 pr-3">Indicator</th>
                  <th className="pb-2 px-3">Sampling Frequency</th>
                  <th className="pb-2 px-3">Measurement Protocol</th>
                  <th className="pb-2 pl-3">Target Threshold</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-stone-800/60 font-sans">
                {monitoringPlan.map((m, idx) => (
                  <tr key={idx} className="hover:bg-stone-950/40">
                    <td className="py-2.5 pr-3 font-semibold text-stone-200">{m.indicator}</td>
                    <td className="py-2.5 px-3 text-stone-300">{m.frequency}</td>
                    <td className="py-2.5 px-3 text-stone-400 font-mono text-[11px]">{m.method}</td>
                    <td className="py-2.5 pl-3 font-semibold text-emerald-400">{m.target}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
