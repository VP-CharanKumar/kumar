import React, { useState, useEffect } from "react";
import { Navbar } from "./components/Navbar";
import { EnvironmentalProfileCard } from "./components/EnvironmentalProfileCard";
import { InteractionsPanel } from "./components/InteractionsPanel";
import { RecommendationsList } from "./components/RecommendationsList";
import { ScenarioPresets } from "./components/ScenarioPresets";
import { KnowledgeExplorer } from "./components/KnowledgeExplorer";
import { ChatConsole } from "./components/ChatConsole";
import { SubmissionSummaryCard } from "./components/SubmissionSummaryCard";
import { TestSuiteModal } from "./components/TestSuiteModal";
import { ChatBotWidget } from "./components/ChatBotWidget";
import {
  EnvironmentalProfile,
  ChatMessage,
  MultiMetricInteraction,
  RecommendationItem,
  MonitoringItem
} from "./types";

export default function App() {
  const [conversationId, setConversationId] = useState<string>(`conv_${Date.now()}`);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome-1",
      sender: "assistant",
      content:
        "Welcome to **Darukaa.Earth: AI Biodiversity Intelligence**.\n\nI am your specialized ecological reasoning assistant grounded in peer-reviewed scientific literature (FAO, IPCC, IPBES, UNEP, USDA, ICRAF).\n\nTo begin an assessment, describe your site's environmental baseline (e.g. soil organic carbon %, precipitation, crop rotation, pesticide usage), or select an evaluation scenario above.",
      timestamp: new Date().toISOString()
    }
  ]);

  const [profile, setProfile] = useState<EnvironmentalProfile>({});
  const [missingVariables, setMissingVariables] = useState<string[]>([
    "Soil Organic Carbon (SOC %)",
    "Annual Precipitation (mm/year)",
    "Land-use & Cropping Pattern"
  ]);
  const [variablesUsed, setVariablesUsed] = useState<string[]>([]);
  const [interactions, setInteractions] = useState<MultiMetricInteraction[]>([]);
  const [recommendations, setRecommendations] = useState<RecommendationItem[]>([]);
  const [monitoringPlan, setMonitoringPlan] = useState<MonitoringItem[]>([]);
  const [uncertainties, setUncertainties] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isKnowledgeOpen, setIsKnowledgeOpen] = useState<boolean>(false);
  const [isTestModalOpen, setIsTestModalOpen] = useState<boolean>(false);
  const [knowledgeCount, setKnowledgeCount] = useState<number>(56);

  useEffect(() => {
    // Check health endpoint
    fetch("/api/health")
      .then((res) => res.json())
      .then((data) => {
        if (data.rag_chunks_indexed) {
          setKnowledgeCount(data.rag_chunks_indexed);
        }
      })
      .catch((e) => console.log("Backend connection check:", e));
  }, []);

  const handleSendMessage = async (text: string) => {
    setIsLoading(true);

    const userMsg: ChatMessage = {
      id: `msg_u_${Date.now()}`,
      sender: "user",
      content: text,
      timestamp: new Date().toISOString()
    };
    setMessages((prev) => [...prev, userMsg]);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: text
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();

      if (data.environmental_profile) {
        setProfile(data.environmental_profile);
      }
      if (data.missing_variables) {
        setMissingVariables(data.missing_variables);
      }

      if (data.analysis) {
        setVariablesUsed(data.analysis.variables_used_for_reasoning || []);
        setInteractions(data.analysis.environmental_interactions || []);
        setRecommendations(data.analysis.recommendations || []);
        setMonitoringPlan(data.analysis.monitoring_plan || []);
        setUncertainties(data.analysis.uncertainties || []);
      } else {
        setVariablesUsed([]);
        setInteractions([]);
        setRecommendations([]);
        setMonitoringPlan([]);
        setUncertainties([]);
      }

      const assistantMsg: ChatMessage = {
        id: `msg_a_${Date.now()}`,
        sender: "assistant",
        content: data.message,
        timestamp: new Date().toISOString(),
        analysis: data.analysis,
        clarifyingQuestions: data.clarifying_questions
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      console.error("Chat error:", err);
      const errorMsg: ChatMessage = {
        id: `msg_err_${Date.now()}`,
        sender: "assistant",
        content: "Error communicating with reasoning engine. Please ensure the backend server is running and retry.",
        timestamp: new Date().toISOString()
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectScenario = (prompt: string, title: string) => {
    handleSendMessage(prompt);
  };

  const handleResetConversation = () => {
    setConversationId(`conv_${Date.now()}`);
    setProfile({});
    setMissingVariables([
      "Soil Organic Carbon (SOC %)",
      "Annual Precipitation (mm/year)",
      "Land-use & Cropping Pattern"
    ]);
    setVariablesUsed([]);
    setInteractions([]);
    setRecommendations([]);
    setMonitoringPlan([]);
    setUncertainties([]);
    setMessages([
      {
        id: `welcome-${Date.now()}`,
        sender: "assistant",
        content:
          "Session reset. Ready for a new ecological assessment. Please describe your environmental parameters or pick a preset scenario above.",
        timestamp: new Date().toISOString()
      }
    ]);
  };

  const handleUpdateVariable = (key: keyof EnvironmentalProfile, value: any) => {
    setProfile((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <div className="min-h-screen bg-stone-950 text-stone-100 flex flex-col font-sans selection:bg-emerald-800 selection:text-white">
      {/* Navigation & Header */}
      <Navbar
        onOpenKnowledge={() => setIsKnowledgeOpen(true)}
        onOpenTests={() => setIsTestModalOpen(true)}
        knowledgeCount={knowledgeCount}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
        {/* Preset Evaluation Scenarios */}
        <ScenarioPresets
          onSelectScenario={handleSelectScenario}
          isLoading={isLoading}
        />

        {/* Main 2-Column Responsive Workspace */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          
          {/* Left Column: Conversational Console & Submission Document (5 cols) */}
          <div className="lg:col-span-5 space-y-6">
            <ChatConsole
              messages={messages}
              onSendMessage={handleSendMessage}
              isLoading={isLoading}
              onResetConversation={handleResetConversation}
            />

            <SubmissionSummaryCard />
          </div>

          {/* Right Column: Environmental Memory, Interactions & Recommendations (7 cols) */}
          <div className="lg:col-span-7 space-y-6">
            <EnvironmentalProfileCard
              profile={profile}
              missingVariables={missingVariables}
              variablesUsed={variablesUsed}
              onUpdateVariable={handleUpdateVariable}
            />

            <InteractionsPanel
              interactions={interactions}
              variablesUsed={variablesUsed}
              uncertainties={uncertainties}
            />

            <RecommendationsList
              recommendations={recommendations}
              monitoringPlan={monitoringPlan}
            />
          </div>
        </div>
      </main>

      {/* Peer-Reviewed Knowledge Explorer Modal */}
      <KnowledgeExplorer
        isOpen={isKnowledgeOpen}
        onClose={() => setIsKnowledgeOpen(false)}
      />

      {/* Automated 24-Test Suite Runner Modal */}
      <TestSuiteModal
        isOpen={isTestModalOpen}
        onClose={() => setIsTestModalOpen(false)}
      />

      {/* Floating Interactive AI ChatBot Assistant */}
      <ChatBotWidget
        currentProfile={profile}
        onProfileUpdate={(p) => setProfile((prev) => ({ ...prev, ...p }))}
      />

      {/* Footer */}
      <footer className="border-t border-stone-800 bg-stone-900/60 text-stone-500 text-xs py-4 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>
            Darukaa.Earth AI Biodiversity Intelligence © 2025 • Scientific RAG Grounding Engine
          </span>
          <span className="font-mono text-[11px] text-stone-400">
            FAO • IPCC • IPBES • UNEP • USDA • ICRAF Verified
          </span>
        </div>
      </footer>
    </div>
  );
}
