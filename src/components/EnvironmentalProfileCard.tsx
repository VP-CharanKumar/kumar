import React from "react";
import { EnvironmentalProfile } from "../types";
import { ShieldCheck, AlertCircle, Droplets, Mountain, Sprout, Wind, Gauge, Layers } from "lucide-react";

interface ProfileCardProps {
  profile: EnvironmentalProfile;
  missingVariables: string[];
  variablesUsed: string[];
  onUpdateVariable: (key: keyof EnvironmentalProfile, value: any) => void;
}

export const EnvironmentalProfileCard: React.FC<ProfileCardProps> = ({
  profile,
  missingVariables,
  variablesUsed,
  onUpdateVariable
}) => {
  const is3VarSatisfied = variablesUsed.length >= 3;

  return (
    <div id="environmental-profile-card" className="bg-stone-900 border border-stone-800 rounded-xl p-5 shadow-sm text-stone-200">
      
      {/* Header & Validation Status */}
      <div className="flex items-center justify-between gap-2 pb-4 border-b border-stone-800">
        <div>
          <h2 className="text-sm font-semibold text-stone-100 flex items-center gap-2">
            <Layers className="w-4 h-4 text-emerald-400" />
            Environmental Profile Memory
          </h2>
          <p className="text-xs text-stone-400 mt-0.5">
            Active parameter state extracted across multi-turn conversation
          </p>
        </div>

        {/* 3-Variable Validator Indicator */}
        <div
          id="badge-three-variable-validator"
          className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border ${
            is3VarSatisfied
              ? "bg-emerald-950 text-emerald-300 border-emerald-700/60"
              : "bg-amber-950/70 text-amber-300 border-amber-800/60"
          }`}
        >
          {is3VarSatisfied ? (
            <>
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              <span>3-Variable Rule: PASSED ({variablesUsed.length} coupled)</span>
            </>
          ) : (
            <>
              <AlertCircle className="w-3.5 h-3.5 text-amber-400" />
              <span>3-Variable Rule: CONSTRAINED ({variablesUsed.length}/3)</span>
            </>
          )}
        </div>
      </div>

      {/* Primary Key Variables Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3.5 my-4">
        
        {/* SOC */}
        <div className="bg-stone-950/60 border border-stone-800/80 rounded-lg p-3">
          <div className="flex items-center justify-between text-xs text-stone-400 mb-1">
            <span className="flex items-center gap-1">
              <Mountain className="w-3.5 h-3.5 text-amber-400" /> SOC %
            </span>
          </div>
          <div className="text-lg font-mono font-semibold text-stone-100">
            {profile.soil_organic_carbon !== undefined ? `${profile.soil_organic_carbon}%` : "—"}
          </div>
          <div className="text-[11px] text-stone-500 mt-0.5">
            {profile.soil_organic_carbon !== undefined && profile.soil_organic_carbon < 0.8 ? "Critical Depletion" : "Carbon status"}
          </div>
        </div>

        {/* Rainfall */}
        <div className="bg-stone-950/60 border border-stone-800/80 rounded-lg p-3">
          <div className="flex items-center justify-between text-xs text-stone-400 mb-1">
            <span className="flex items-center gap-1">
              <Droplets className="w-3.5 h-3.5 text-blue-400" /> Rainfall
            </span>
          </div>
          <div className="text-lg font-mono font-semibold text-stone-100">
            {profile.annual_rainfall_mm !== undefined ? `${profile.annual_rainfall_mm} mm` : "—"}
          </div>
          <div className="text-[11px] text-stone-500 mt-0.5">
            {profile.annual_rainfall_mm !== undefined && profile.annual_rainfall_mm < 500 ? "Semi-Arid Deficit" : "Annual regime"}
          </div>
        </div>

        {/* Region */}
        <div className="bg-stone-950/60 border border-stone-800/80 rounded-lg p-3">
          <div className="flex items-center justify-between text-xs text-stone-400 mb-1">
            <span className="flex items-center gap-1">
              <Wind className="w-3.5 h-3.5 text-emerald-400" /> Region / Biome
            </span>
          </div>
          <div className="text-sm font-medium text-stone-200 truncate capitalize mt-1">
            {profile.region || "Unspecified"}
          </div>
          <div className="text-[11px] text-stone-500 mt-1">Bioclimatic zone</div>
        </div>

        {/* Crop / Regime */}
        <div className="bg-stone-950/60 border border-stone-800/80 rounded-lg p-3">
          <div className="flex items-center justify-between text-xs text-stone-400 mb-1">
            <span className="flex items-center gap-1">
              <Sprout className="w-3.5 h-3.5 text-teal-400" /> Crop Regime
            </span>
          </div>
          <div className="text-sm font-medium text-stone-200 truncate capitalize mt-1">
            {profile.crop_type || profile.land_use || "Unspecified"}
          </div>
          <div className="text-[11px] text-stone-500 mt-1">Agronomic practice</div>
        </div>
      </div>

      {/* Missing Variables Warning Banner if any */}
      {missingVariables.length > 0 && (
        <div className="bg-stone-950 border border-stone-800 rounded-lg p-3 text-xs">
          <div className="text-stone-400 font-medium mb-1.5 flex items-center gap-1.5">
            <AlertCircle className="w-3.5 h-3.5 text-amber-400" />
            <span>Identified Data Gaps ({missingVariables.length} critical parameters unmeasured):</span>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {missingVariables.map((v, i) => (
              <span
                key={i}
                className="px-2 py-0.5 rounded bg-stone-800/90 text-stone-300 font-mono text-[11px] border border-stone-700/60"
              >
                {v}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
