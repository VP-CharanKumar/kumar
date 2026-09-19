import React, { useState, useRef, useEffect } from "react";
import {
  Bot,
  MessageSquare,
  X,
  Send,
  Sparkles,
  RotateCcw,
  Maximize2,
  Minimize2,
  HelpCircle,
  Check,
  Copy,
  ExternalLink,
  ChevronDown,
  Layers,
  Leaf
} from "lucide-react";
import { EnvironmentalProfile } from "../types";

interface ChatBotWidgetProps {
  onProfileUpdate?: (profile: EnvironmentalProfile) => void;
  currentProfile: EnvironmentalProfile;
}

interface BotMessage {
  id: string;
  sender: "user" | "bot";
  text: string;
  timestamp: string;
  sources?: { id: string; title: string; category: string; snippet: string }[];
  clarifyingQuestions?: string[];
}

export const ChatBotWidget: React.FC<ChatBotWidgetProps> = ({
  onProfileUpdate,
  currentProfile
}) => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [isExpanded, setIsExpanded] = useState<boolean>(false);
  const [input, setInput] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [mode, setMode] = useState<"qa" | "diagnose">("qa");

  const [messages, setMessages] = useState<BotMessage[]>([
    {
      id: "bot-init",
      sender: "bot",
      text: "Hello! I am the **Darukaa.Earth AI ChatBot**.\n\nYou can ask me any question about biodiversity, soil carbon, agroforestry, or pollinators—or share your site's parameters for an evidence-grounded multi-metric assessment!",
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    }
  ]);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isOpen]);

  const quickPrompts = [
    { label: "What is glomalin?", query: "What is glomalin and how does it stabilize soil aggregates?" },
    { label: "Faidherbia hydraulic lift", query: "Explain hydraulic lift and reverse phenology in Faidherbia albida agroforestry." },
    { label: "3-Variable Rule", query: "Explain the 3-variable validation rule in ecological reasoning." },
    { label: "Pesticides & Pollinators", query: "How do synthetic pesticides and pyrethroids impact wild pollinator colonies?" },
    { label: "FAO Recarbonization", query: "What are the FAO targets and mechanisms for soil organic carbon recarbonization?" }
  ];

  const handleSend = async (textToSend?: string) => {
    const query = textToSend || input.trim();
    if (!query || isLoading) return;

    const userMsg: BotMessage = {
      id: `u-${Date.now()}`,
      sender: "user",
      text: query,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInput("");
    setIsLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: query,
          conversation_id: `bot_widget_${Date.now()}`
        })
      });

      if (!res.ok) throw new Error("API error");
      const data = await res.json();

      if (data.environmental_profile && onProfileUpdate) {
        onProfileUpdate(data.environmental_profile);
      }

      const botMsg: BotMessage = {
        id: `b-${Date.now()}`,
        sender: "bot",
        text: data.message,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        sources: data.retrieved_evidence || (data.analysis ? data.analysis.sources : undefined),
        clarifyingQuestions: data.clarifying_questions
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        {
          id: `err-${Date.now()}`,
          sender: "bot",
          text: "I encountered an issue retrieving that information. Please verify the backend connection and try again.",
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleClear = () => {
    setMessages([
      {
        id: `bot-reset-${Date.now()}`,
        sender: "bot",
        text: "Chat cleared. What ecological inquiry would you like to explore?",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
      }
    ]);
  };

  return (
    <>
      {/* Floating Launcher Button */}
      {!isOpen && (
        <div className="fixed bottom-5 right-5 z-40">
          <button
            id="btn-open-chatbot"
            onClick={() => setIsOpen(true)}
            className="group relative flex items-center gap-2.5 px-4 py-3 rounded-full bg-emerald-700 hover:bg-emerald-600 text-white shadow-xl hover:shadow-emerald-900/40 transition duration-200 border border-emerald-500/50"
          >
            <div className="relative">
              <Bot className="w-5 h-5 text-white transition-transform group-hover:scale-110" />
              <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-400 rounded-full animate-ping" />
              <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-300 rounded-full" />
            </div>
            <div className="flex flex-col text-left">
              <span className="text-xs font-bold leading-tight tracking-wide">
                Darukaa AI Bot
              </span>
              <span className="text-[10px] text-emerald-200 leading-tight">
                Ask Ecological Assistant
              </span>
            </div>
          </button>
        </div>
      )}

      {/* Floating Chat Window */}
      {isOpen && (
        <div
          className={`fixed z-50 transition-all duration-200 flex flex-col bg-stone-900 border border-stone-700 shadow-2xl rounded-2xl overflow-hidden ${
            isExpanded
              ? "inset-4 sm:inset-10"
              : "bottom-5 right-5 w-[92vw] sm:w-[440px] h-[600px] max-h-[85vh]"
          }`}
        >
          {/* Header */}
          <div className="p-3.5 bg-stone-950 border-b border-stone-800 flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-emerald-950 border border-emerald-600/40 flex items-center justify-center text-emerald-400">
                <Bot className="w-4 h-4" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-sm font-semibold text-stone-100">
                    Darukaa.Earth AI ChatBot
                  </h3>
                  <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800/60">
                    Online
                  </span>
                </div>
                <p className="text-[11px] text-stone-400">
                  Evidence-Grounded Ecological Q&A & Site Assessment
                </p>
              </div>
            </div>

            <div className="flex items-center gap-1">
              <button
                onClick={handleClear}
                title="Reset conversation"
                className="p-1.5 text-stone-400 hover:text-stone-200 hover:bg-stone-800 rounded transition"
              >
                <RotateCcw className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                title={isExpanded ? "Minimize size" : "Expand window"}
                className="p-1.5 text-stone-400 hover:text-stone-200 hover:bg-stone-800 rounded transition hidden sm:inline-flex"
              >
                {isExpanded ? (
                  <Minimize2 className="w-3.5 h-3.5" />
                ) : (
                  <Maximize2 className="w-3.5 h-3.5" />
                )}
              </button>
              <button
                onClick={() => setIsOpen(false)}
                title="Close chat"
                className="p-1.5 text-stone-400 hover:text-stone-200 hover:bg-stone-800 rounded transition"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Quick Questions Strip */}
          <div className="px-3 py-2 bg-stone-950/60 border-b border-stone-800 flex items-center gap-1.5 overflow-x-auto text-[11px]">
            <span className="text-stone-400 text-[10px] uppercase font-semibold shrink-0">
              Suggestions:
            </span>
            {quickPrompts.map((qp, i) => (
              <button
                key={i}
                onClick={() => handleSend(qp.query)}
                className="px-2 py-0.5 rounded-full bg-stone-800 hover:bg-stone-700 text-stone-300 whitespace-nowrap border border-stone-700/60 transition text-[11px]"
              >
                {qp.label}
              </button>
            ))}
          </div>

          {/* Messages Feed */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3.5 text-xs">
            {messages.map((m) => (
              <div
                key={m.id}
                className={`flex flex-col ${
                  m.sender === "user" ? "items-end" : "items-start"
                }`}
              >
                <div
                  className={`max-w-[88%] p-3 rounded-xl leading-relaxed whitespace-pre-wrap ${
                    m.sender === "user"
                      ? "bg-emerald-700 text-white rounded-br-none shadow-sm"
                      : "bg-stone-850 bg-stone-800/80 text-stone-200 border border-stone-700/60 rounded-bl-none shadow-sm"
                  }`}
                >
                  <div>{m.text}</div>

                  {/* Clarifying Questions Quick-Answer Chips */}
                  {m.clarifyingQuestions && m.clarifyingQuestions.length > 0 && (
                    <div className="mt-3 pt-2.5 border-t border-stone-700/60 space-y-1.5">
                      <div className="text-[11px] font-semibold text-amber-300 flex items-center gap-1">
                        <HelpCircle className="w-3.5 h-3.5" /> Please specify:
                      </div>
                      {m.clarifyingQuestions.map((q, idx) => (
                        <button
                          key={idx}
                          onClick={() => {
                            setInput(`Regarding: "${q}" -> `);
                          }}
                          className="block text-left w-full p-1.5 rounded bg-stone-900/90 hover:bg-stone-900 text-[11px] text-stone-300 border border-stone-700/80 transition"
                        >
                          • {q}
                        </button>
                      ))}
                    </div>
                  )}

                  {/* Evidence Sources Badges */}
                  {m.sources && m.sources.length > 0 && (
                    <div className="mt-2.5 pt-2 border-t border-stone-700/50">
                      <span className="text-[10px] text-stone-400 block mb-1">
                        Scientific Grounding Sources:
                      </span>
                      <div className="flex flex-wrap gap-1">
                        {m.sources.map((s, idx) => (
                          <span
                            key={idx}
                            className="text-[10px] px-1.5 py-0.5 rounded bg-stone-950 text-emerald-400 border border-stone-800"
                          >
                            {s.title}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-2 mt-1 px-1 text-[10px] text-stone-400">
                  <span>{m.timestamp}</span>
                  {m.sender === "bot" && (
                    <button
                      onClick={() => handleCopy(m.text, m.id)}
                      className="hover:text-stone-300 transition"
                      title="Copy response"
                    >
                      {copiedId === m.id ? (
                        <Check className="w-3 h-3 text-emerald-400" />
                      ) : (
                        <Copy className="w-3 h-3" />
                      )}
                    </button>
                  )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex items-center gap-2 p-3 bg-stone-800/50 rounded-xl max-w-[70%] border border-stone-700/50 text-stone-400 text-xs">
                <Bot className="w-4 h-4 text-emerald-400 animate-pulse" />
                <span>Darukaa Bot is synthesizing evidence...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Box */}
          <div className="p-3 bg-stone-950 border-t border-stone-800">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSend();
              }}
              className="flex items-center gap-2"
            >
              <input
                id="chatbot-input"
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about soil carbon, agroforestry, pollinators..."
                disabled={isLoading}
                className="flex-1 bg-stone-900 border border-stone-700 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 rounded-lg px-3 py-2 text-xs text-stone-100 placeholder-stone-500 focus:outline-none transition"
              />
              <button
                id="btn-send-chatbot"
                type="submit"
                disabled={!input.trim() || isLoading}
                className="p-2 rounded-lg bg-emerald-700 hover:bg-emerald-600 disabled:opacity-40 text-white transition shadow-sm"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
            <div className="mt-1 text-[10px] text-stone-400 flex items-center justify-between">
              <span>Grounded in FAO, IPCC, IPBES, UNEP, USDA literature</span>
              <span className="font-mono">Press Enter to send</span>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
