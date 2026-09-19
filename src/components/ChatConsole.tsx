import React, { useState, useRef, useEffect } from "react";
import { ChatMessage } from "../types";
import { Send, Bot, User, RefreshCw, HelpCircle, ArrowUpRight } from "lucide-react";

interface ChatConsoleProps {
  messages: ChatMessage[];
  onSendMessage: (text: string) => void;
  isLoading: boolean;
  onResetConversation: () => void;
}

export const ChatConsole: React.FC<ChatConsoleProps> = ({
  messages,
  onSendMessage,
  isLoading,
  onResetConversation
}) => {
  const [input, setInput] = useState("");
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    onSendMessage(input.trim());
    setInput("");
  };

  const handleChipClick = (question: string) => {
    setInput(`Regarding ${question.toLowerCase().replace("?", "")}: `);
  };

  return (
    <div id="chat-console" className="bg-stone-900 border border-stone-800 rounded-xl flex flex-col h-[560px] shadow-sm text-stone-200 overflow-hidden">
      
      {/* Console Header */}
      <div className="p-3.5 border-b border-stone-800 flex items-center justify-between bg-stone-950/50">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-xs font-mono font-semibold text-stone-200 uppercase tracking-wider">
            Conversational Reasoning Console
          </span>
        </div>

        <button
          onClick={onResetConversation}
          disabled={isLoading || messages.length <= 1}
          className="inline-flex items-center gap-1 text-[11px] font-mono text-stone-400 hover:text-stone-200 transition disabled:opacity-30 disabled:cursor-not-allowed"
          title="Reset conversation and clear environmental profile"
        >
          <RefreshCw className="w-3 h-3" />
          <span>Reset Session</span>
        </button>
      </div>

      {/* Message Stream */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => {
          const isUser = msg.sender === "user";
          return (
            <div
              key={msg.id}
              className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}
            >
              {!isUser && (
                <div className="w-7 h-7 rounded-lg bg-emerald-950 border border-emerald-700/60 flex items-center justify-center text-emerald-400 shrink-0 mt-0.5">
                  <Bot className="w-4 h-4" />
                </div>
              )}

              <div
                className={`max-w-[85%] rounded-xl p-3.5 text-xs leading-relaxed ${
                  isUser
                    ? "bg-emerald-900/40 text-emerald-100 border border-emerald-700/50 font-sans"
                    : "bg-stone-950/80 text-stone-200 border border-stone-800/80 font-sans"
                }`}
              >
                <div className="whitespace-pre-line">{msg.content}</div>

                {/* Clarifying Questions Prompt Chips */}
                {msg.clarifyingQuestions && msg.clarifyingQuestions.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-stone-800 space-y-1.5">
                    <div className="text-[11px] font-mono text-amber-300 font-semibold flex items-center gap-1">
                      <HelpCircle className="w-3.5 h-3.5" />
                      <span>Clarification Prompts (Click to answer):</span>
                    </div>
                    <div className="space-y-1">
                      {msg.clarifyingQuestions.map((q, qi) => (
                        <button
                          key={qi}
                          onClick={() => handleChipClick(q)}
                          className="w-full text-left p-2 rounded bg-stone-900 hover:bg-stone-800 border border-stone-700/70 text-[11px] text-stone-300 transition flex items-center justify-between group"
                        >
                          <span>{q}</span>
                          <ArrowUpRight className="w-3 h-3 text-stone-500 group-hover:text-emerald-400 shrink-0 ml-1" />
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {isUser && (
                <div className="w-7 h-7 rounded-lg bg-stone-800 border border-stone-700 flex items-center justify-center text-stone-300 shrink-0 mt-0.5">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          );
        })}

        {isLoading && (
          <div className="flex items-center gap-2.5 text-xs font-mono text-stone-400 py-2">
            <div className="w-4 h-4 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
            <span>Executing RAG retrieval and multi-metric reasoning...</span>
          </div>
        )}

        <div ref={endRef} />
      </div>

      {/* Input Field */}
      <form onSubmit={handleSubmit} className="p-3 border-t border-stone-800 bg-stone-950/60">
        <div className="flex gap-2">
          <input
            id="chat-input-field"
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe your ecosystem, crop rotation, soil SOC %, rainfall, or pesticide use..."
            disabled={isLoading}
            className="flex-1 bg-stone-900 border border-stone-700 rounded-lg px-3.5 py-2.5 text-xs text-stone-100 placeholder-stone-500 focus:outline-hidden focus:border-emerald-500 font-sans disabled:opacity-50"
          />
          <button
            id="btn-send-message"
            type="submit"
            disabled={!input.trim() || isLoading}
            className="px-4 py-2.5 bg-emerald-700 hover:bg-emerald-600 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 transition disabled:opacity-40 disabled:cursor-not-allowed"
          >
            <Send className="w-3.5 h-3.5" />
            <span>Submit</span>
          </button>
        </div>
      </form>
    </div>
  );
};
