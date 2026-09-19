import React from "react";
import { MultiMetricInteraction } from "../types";
import { Network, ArrowRight, BookOpen, AlertTriangle } from "lucide-react";

interface InteractionsPanelProps {
  interactions: MultiMetricInteraction[];
  variablesUsed: string[];
  uncertainties: string[];
}

export const InteractionsPanel: React.FC<InteractionsPanelProps> = ({
  interactions,
  variablesUsed,
  uncertainties
}) => {
  if (interactions.length === 0 && uncertainties.length === 0) {
    return null;
  }

  return (
    <div id="multi-metric-interactions-panel" className="bg-stone-900 border border-stone-800 rounded-xl p-5 shadow-sm text-stone-200">
      
      {/* Title */}
      <div className="flex items-center justify-between pb-3 border-b border-stone-800">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded bg-emerald-950 border border-emerald-700/50 flex items-center justify-center text-emerald-400">
            <Network className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-stone-100 uppercase tracking-wide font-mono">
              MULTI-METRIC INTERACTIONS
            </h3>
            <p className="text-xs text-stone-400">
              Mechanistic physiological couplings across ≥ 3 environmental variables
            </p>
          </div>
        </div>

        <div className="text-xs font-mono text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded border border-emerald-800/40">
          Coupled: {variablesUsed.length} Variables
        </div>
      </div>

      {/* Variables List Tag Cloud */}
      <div className="my-3.5 flex flex-wrap items-center gap-1.5">
        <span className="text-xs text-stone-400 mr-1 font-medium">Variables in Active Loop:</span>
        {variablesUsed.map((v, i) => (
          <span
            key={i}
            className="px-2 py-0.5 text-[11px] font-mono rounded bg-stone-800 text-stone-200 border border-stone-700"
          >
            {v}
          </span>
        ))}
      </div>

      {/* Interaction Cards */}
      <div className="space-y-3 mt-2">
        {interactions.map((interaction, idx) => (
          <div
            key={idx}
            className="bg-stone-950/80 border border-stone-800 rounded-lg p-3.5 hover:border-stone-700 transition"
          >
            {/* Header: Type and Coupled Variables */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1.5 mb-2">
              <span className="text-xs font-semibold text-amber-300 flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
                {interaction.interaction_type}
              </span>
              <div className="flex items-center flex-wrap gap-1 text-[11px] font-mono text-stone-400">
                {interaction.variables.map((varName, vi) => (
                  <React.Fragment key={vi}>
                    <span className="text-stone-300">{varName}</span>
                    {vi < interaction.variables.length - 1 && (
                      <ArrowRight className="w-3 h-3 text-stone-500 inline" />
                    )}
                  </React.Fragment>
                ))}
              </div>
            </div>

            {/* Description / Mechanisms */}
            <p className="text-xs text-stone-300 leading-relaxed">
              {interaction.description}
            </p>

            {/* Evidence support */}
            {interaction.evidence_support && (
              <div className="mt-2.5 pt-2 border-t border-stone-900 flex items-center gap-1.5 text-[11px] text-stone-400">
                <BookOpen className="w-3 h-3 text-emerald-400 shrink-0" />
                <span className="font-mono text-stone-400">Grounding: {interaction.evidence_support}</span>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Uncertainties & Limitations if any */}
      {uncertainties.length > 0 && (
        <div className="mt-3.5 bg-amber-950/40 border border-amber-900/50 rounded-lg p-3 text-xs text-amber-300 flex items-start gap-2">
          <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
          <div>
            <div className="font-semibold mb-0.5">Ecological Uncertainty & Constraints:</div>
            {uncertainties.map((u, i) => (
              <p key={i} className="text-amber-200/90 leading-relaxed">{u}</p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
