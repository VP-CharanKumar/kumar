import React, { useState, useEffect } from "react";
import { Search, BookOpen, X, ExternalLink, Filter, Database } from "lucide-react";

interface KnowledgeExplorerProps {
  isOpen: boolean;
  onClose: () => void;
}

export const KnowledgeExplorer: React.FC<KnowledgeExplorerProps> = ({ isOpen, onClose }) => {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("all");
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!isOpen) return;
    fetchResults();
  }, [isOpen, category]);

  const fetchResults = async (q = query) => {
    setLoading(true);
    try {
      const url = new URL("/api/knowledge/search", window.location.origin);
      if (q) url.searchParams.set("query", q);
      if (category !== "all") url.searchParams.set("category", category);

      const res = await fetch(url.toString());
      if (res.ok) {
        const data = await res.json();
        setResults(data);
      }
    } catch (e) {
      console.error("Knowledge search error:", e);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchResults(query);
  };

  if (!isOpen) return null;

  const categories = [
    { id: "all", label: "All Modules (10)" },
    { id: "soil_health", label: "Soil Science" },
    { id: "biodiversity", label: "Biodiversity & Trophic" },
    { id: "climate", label: "Climate & Moisture" },
    { id: "agroforestry", label: "Agroforestry (ICRAF)" },
    { id: "restoration", label: "Dryland Restoration" },
    { id: "pollinators", label: "Pollinator Ecology (IPBES)" },
    { id: "water_catchment", label: "Hydrology & Watershed" },
    { id: "pesticide_impacts", label: "Ecotoxicology (UNEP)" },
    { id: "native_flora", label: "Native Flora" },
    { id: "monitoring_framework", label: "Monitoring Standards" }
  ];

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4 sm:p-6">
      <div className="bg-stone-900 border border-stone-800 rounded-2xl w-full max-w-4xl max-h-[88vh] flex flex-col shadow-2xl text-stone-100 overflow-hidden">
        
        {/* Header */}
        <div className="p-5 border-b border-stone-800 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-emerald-950 border border-emerald-700/50 flex items-center justify-center text-emerald-400">
              <Database className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-semibold text-stone-100 font-mono">
                Peer-Reviewed Scientific Knowledge Corpus
              </h2>
              <p className="text-xs text-stone-400">
                Indexed from FAO, IPCC, IPBES, UNEP, USDA, and ICRAF canonical treatises
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-stone-400 hover:text-stone-100 hover:bg-stone-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Search & Filter Controls */}
        <div className="p-4 border-b border-stone-800 bg-stone-950/40 flex flex-col sm:flex-row gap-3">
          <form onSubmit={handleSearch} className="flex-1 relative">
            <Search className="w-4 h-4 text-stone-400 absolute left-3 top-3" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search across 56 semantic chunks (e.g. glomalin,Faiderbia, SOC, trophic)..."
              className="w-full bg-stone-900 border border-stone-700 rounded-lg pl-9 pr-4 py-2 text-xs text-stone-100 placeholder-stone-500 focus:outline-hidden focus:border-emerald-500 font-mono"
            />
          </form>

          <div className="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0">
            <Filter className="w-3.5 h-3.5 text-stone-400 shrink-0" />
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="bg-stone-900 border border-stone-700 rounded-lg px-3 py-2 text-xs text-stone-200 focus:outline-hidden focus:border-emerald-500 font-mono"
            >
              {categories.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Results List */}
        <div className="flex-1 overflow-y-auto p-5 space-y-3.5">
          {loading ? (
            <div className="py-12 text-center text-xs text-stone-400 font-mono">
              Querying vectorized knowledge repository...
            </div>
          ) : results.length === 0 ? (
            <div className="py-12 text-center text-xs text-stone-400 font-mono">
              No matching knowledge chunks found. Try broader ecological terms.
            </div>
          ) : (
            results.map((chunk) => (
              <div
                key={chunk.id}
                className="bg-stone-950/70 border border-stone-800/90 rounded-xl p-4 hover:border-stone-700 transition"
              >
                <div className="flex items-center justify-between gap-2 mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">
                      {chunk.category}
                    </span>
                    <h3 className="text-xs font-semibold text-stone-100 font-mono">
                      {chunk.title}
                    </h3>
                  </div>
                  <span className="text-[10px] font-mono text-stone-500">
                    {chunk.sourceDoc}
                  </span>
                </div>

                <div className="text-xs text-stone-300 leading-relaxed font-sans whitespace-pre-line bg-stone-900/50 p-3 rounded-lg border border-stone-800/60 max-h-48 overflow-y-auto">
                  {chunk.content}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <div className="p-3.5 border-t border-stone-800 bg-stone-950 text-stone-400 text-xs flex items-center justify-between font-mono">
          <span>Source verification: sources.json ground-truthed</span>
          <button
            onClick={onClose}
            className="px-3 py-1 bg-stone-800 hover:bg-stone-700 text-stone-200 rounded text-xs transition"
          >
            Close Explorer
          </button>
        </div>
      </div>
    </div>
  );
};
