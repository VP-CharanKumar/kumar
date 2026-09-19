import React from "react";
import { Sparkles, Sprout, Bug, Trees, Sun, HelpCircle } from "lucide-react";

interface ScenarioPresetsProps {
  onSelectScenario: (prompt: string, title: string) => void;
  isLoading: boolean;
}

export const ScenarioPresets: React.FC<ScenarioPresetsProps> = ({
  onSelectScenario,
  isLoading
}) => {
  const presets = [
    {
      id: "preset-semi-arid",
      title: "Semi-Arid Wheat Monoculture",
      badge: "Core Multi-Metric",
      icon: Sprout,
      prompt: "I am managing farmland in a semi-arid biome with 420mm annual rainfall. My soil organic carbon tested at 0.3% and we cultivate continuous wheat as a monoculture. What interventions should we take?"
    },
    {
      id: "preset-pollinators",
      title: "Agrochemical Pollinator Crisis",
      badge: "Trophic Loop",
      icon: Bug,
      prompt: "We have frequent intensive pesticide spraying on our fields and we have noticed severe pollinator decline and fewer solitary bees. How can we restore ecological balance?"
    },
    {
      id: "preset-fragmentation",
      title: "Woodland Fragmentation",
      badge: "Connectivity",
      icon: Trees,
      prompt: "Our region has fragmented forest patches with disconnected woodland corridors and severe edge drying. What ecological restoration strategy is recommended?"
    },
    {
      id: "preset-sparse",
      title: "Sparse Input (Clarification Test)",
      badge: "Clarification Mode",
      icon: HelpCircle,
      prompt: "Crop yield and biological vitality have been deteriorating across my land."
    }
  ];

  return (
    <div id="scenario-presets-bar" className="bg-stone-900 border border-stone-800 rounded-xl p-4 text-stone-200">
      <div className="flex items-center gap-2 mb-3">
        <Sparkles className="w-4 h-4 text-emerald-400" />
        <span className="text-xs font-semibold text-stone-300 uppercase tracking-wide font-mono">
          Reviewer Evaluation Scenarios (One-Click Test)
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
        {presets.map((preset) => {
          const Icon = preset.icon;
          return (
            <button
              key={preset.id}
              id={preset.id}
              disabled={isLoading}
              onClick={() => onSelectScenario(preset.prompt, preset.title)}
              className="text-left bg-stone-950/60 hover:bg-stone-800/80 border border-stone-800 hover:border-emerald-700/60 rounded-lg p-3 transition group disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <div className="flex items-center justify-between gap-1 mb-1">
                <span className="text-[10px] font-mono uppercase px-1.5 py-0.2 rounded bg-stone-800 text-stone-400 border border-stone-700">
                  {preset.badge}
                </span>
                <Icon className="w-3.5 h-3.5 text-stone-400 group-hover:text-emerald-400 transition" />
              </div>
              <div className="text-xs font-semibold text-stone-100 group-hover:text-emerald-300 transition line-clamp-1">
                {preset.title}
              </div>
              <p className="text-[11px] text-stone-400 line-clamp-2 mt-1">
                {preset.prompt}
              </p>
            </button>
          );
        })}
      </div>
    </div>
  );
};
