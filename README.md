# Darukaa.Earth — AI Biodiversity & Ecological Intelligence Platform

> **"Scientific intelligence for healthier ecosystems."**  
> An evidence-grounded multi-metric environmental reasoning engine and ecological assistant powered by Retrieval-Augmented Generation (RAG), Gemini LLM integration, and canonical agricultural science.

---

## Executive Summary

**Darukaa.Earth** bridges the gap between complex ecological science and on-the-ground land stewardship. While generic AI tools frequently offer superficial or ungrounded agricultural tips, Darukaa.Earth enforces **peer-reviewed scientific grounding** (FAO, IPCC, IPBES, UNEP, USDA, ICRAF) and **coupled ecological reasoning**.

### Key Differentiators
1. **The 3-Variable Validation Constraint**: Rejects single-variable recommendations. Every diagnostic requires coupling at least 3 environmental parameters (e.g., Soil Organic Carbon %, annual precipitation, cropping system, agrochemical inputs) before prescribing land interventions.
2. **Deterministic Citation & Evidence Grounding**: All recommendations cite canonical treatises with DOI/ISBN references and explicit confidence scores. When empirical evidence is absent, the system explicitly refuses to speculate.
3. **Conversational Profile Accumulation**: A stateful conversation engine detects missing site variables, prompts land stewards with targeted clarifying inquiries, and builds a comprehensive ecological baseline over multiple dialogue turns.
4. **Trophic Cascade & Feedback Modeling**: Simulates non-linear systemic dynamics, such as pesticide-pollinator trophic collapse, mycorrhizal glomalin aggregate stability, and agroforestry hydraulic redistribution.
5. **Integrated AI ChatBot & Automated Test Suite**: A floating interactive assistant for instant ecological Q&A alongside an in-app test runner executing 24 unit and integration test cases with live console telemetry.

---

## System Architecture

The application is engineered as a hybrid, production-ready system supporting both Node/TypeScript full-stack execution and Python FastAPI services:

```
                      +----------------------------------------------------+
                      |               React 19 Frontend (Vite)             |
                      |  - Diagnostic Workbench   - Trophic Diagram        |
                      |  - Metrics Overview       - Knowledge Explorer     |
                      |  - In-App Test Runner     - Floating AI ChatBot    |
                      +-------------------------+--------------------------+
                                                | HTTP / REST
                                                v
                      +----------------------------------------------------+
                      |            Express 4.21 / Node.js Engine           |
                      |            (server.ts / dist/server.cjs)           |
                      |  - Knowledge Ingestion & Vector Matching (56 chunks)|
                      |  - Multi-Variable Diagnostic Reasoner              |
                      |  - Gemini 3.8 Flash LLM Reasoning & Offline Logic  |
                      |  - Automated Test Runner Bridge (/api/tests/run)   |
                      |  - DOCX & ZIP Submission Exporters                 |
                      +-------------------------+--------------------------+
                                                |
            +-----------------------------------+-----------------------------------+
            |                                                                       |
            v                                                                       v
+------------------------------------+                             +------------------------------------+
|       Python 3 Core Architecture   |                             |     Canonical Knowledge Base       |
|  - FastAPI (app/main.py)           |                             |  - 10 Peer-Reviewed Documents      |
|  - ChromaDB / Vector Store         |                             |  - FAO, IPCC, IPBES, UNEP, USDA    |
|  - Reasoning & Citation Validators |                             |  - Soil Carbon, Pollinators,       |
|  - Unittest Suite (24 Test Cases)  |                             |    Hydrology & Agroforestry        |
+------------------------------------+                             +------------------------------------+
```

---

## Directory Structure

```
├── README.md                      # Complete system documentation (this file)
├── metadata.json                  # Application metadata and runtime capabilities
├── package.json                   # Node.js dependencies (React 19, Tailwind v4, docx, motion)
├── requirements.txt               # Python dependencies (FastAPI, ChromaDB, google-genai, etc.)
├── server.ts                      # Full-stack Express + Vite server with reasoning engine
├── index.html                     # HTML5 application entry point
├── run.py                         # Python entry point for FastAPI backend
│
├── app/                           # Modular Python Backend Architecture
│   ├── main.py                    # FastAPI server entry point
│   ├── config.py                  # System configuration and environment settings
│   ├── api/                       # API router and endpoints
│   ├── database/                  # SQLAlchemy models and SQLite/PostgreSQL persistence
│   ├── models/                    # Pydantic schemas (EnvironmentalProfile, Recommendation)
│   ├── rag/                       # Document ingestion, chunking, and ChromaDB vector store
│   ├── services/                  # Reasoning engine, Chatbot, and Citation Validator
│   └── utils/                     # Structured logging and helper utilities
│
├── knowledge/                     # Canonical Scientific Knowledge Base
│   ├── agroforestry.md            # Faidherbia albida, hydraulic lift, nitrogen fixation
│   ├── biodiversity.md            # Functional diversity, trophic complexity, mycorrhizae
│   ├── climate.md                 # Aridity index, evapotranspiration, drought resilience
│   ├── ecosystem_resilience.md    # Multi-trophic buffering, resilience thresholds
│   ├── habitat_restoration.md     # Native hedgerows, pollinator strips, eco-corridors
│   ├── human_impact.md            # Tillage degradation, compaction, monoculture depletion
│   ├── land_use.md                # Rotational grazing, cover cropping, perennialization
│   ├── pollinators.md             # Wild bee nesting, pesticide sub-lethal impacts
│   ├── soil_health.md             # Soil Organic Carbon (SOC), glomalin, bulk density
│   ├── water_management.md        # Water holding capacity, infiltration, keyline design
│   └── sources.json               # Structured metadata, DOIs, authors, and confidence weights
│
├── src/                           # React 19 Client Application
│   ├── App.tsx                    # Main workbench view orchestrating state and panels
│   ├── main.tsx                   # React root entry point
│   ├── types.ts                   # TypeScript interfaces and type definitions
│   └── components/
│       ├── Navbar.tsx             # Header with stats, knowledge modal, and test runner triggers
│       ├── DiagnosticForm.tsx     # 3-variable land parameter inputs with preset scenarios
│       ├── MetricsOverview.tsx    # Multi-metric visual assessment cards
│       ├── FeedbackLoopDiagram.tsx# Interactive trophic cascade and ecological feedback graph
│       ├── ChatConsole.tsx        # Inline conversational diagnostic console
│       ├── ChatBotWidget.tsx      # Floating interactive AI assistant with quick prompts
│       ├── TestSuiteModal.tsx     # In-app automated test execution modal (24 tests)
│       ├── KnowledgeExplorer.tsx  # Searchable peer-reviewed scientific literature browser
│       └── SubmissionSummaryCard.tsx # Summary card with direct DOCX & ZIP downloads
│
├── tests/                         # Comprehensive 24-Case Automated Test Suite
│   ├── test_api_endpoints.py      # Health check, RAG search, chat, DOCX, ZIP endpoints
│   ├── test_chatbot.py            # Clarification triggers, profile accumulation, edge cases
│   ├── test_citations.py          # Grounding verification and refusal on ungrounded claims
│   ├── test_conversations.py      # Progressive memory accumulation and missing variable prompts
│   ├── test_rag.py                # Chunking integrity, semantic embeddings, vector retrieval
│   └── test_reasoning.py          # 3-variable validation rule and pesticide-pollinator coupling
│
├── scripts/                       # Automation & Packaging Utilities
│   ├── generate_docx.js           # Compiles official 8-chapter submission DOCX with formatting
│   ├── ingest_knowledge.py        # Indexes knowledge corpus into ChromaDB
│   ├── initialize_db.py           # Initializes database tables and schemas
│   ├── package_submission.py      # Bundles clean distribution archive
│   └── verify_docx.py             # Validates generated DOCX structure and sections
│
└── submission/                    # Evaluation Artifacts
    └── Darukaa_Earth_Submission.docx # Complete official project submission report
```

---

## The 3-Variable Validation Rule

To prevent oversimplified recommendations, Darukaa.Earth's reasoning engine enforces a strict mathematical prerequisite:

$$\text{Diagnostic Validity} \iff \sum_{i \in \text{Variables}} \mathbb{I}(\text{Value}_i \text{ is known}) \ge 3$$

| Variable | Metric Unit | Significance in Reasoning Model |
|---|---|---|
| **Soil Organic Carbon (SOC)** | $\%$ mass | Determines Water Holding Capacity (WHC) and glomalin aggregate stability. |
| **Annual Rainfall / Moisture** | $\text{mm/year}$ | Governs drought stress thresholds, aridity index, and species selection. |
| **Cropping / Land System** | Category | Defines biodiversity baseline, soil disturbance, and root depth dynamics. |
| **Agrochemical Inputs** | Frequency / Rate | Determines pesticide-pollinator toxicity and mycorrhizal disruption. |
| **Pollinator Abundance** | Index / Rating | Informs pollination efficacy, crop fruit set, and trophic resilience. |

If fewer than 3 variables are supplied, the system **suspends recommendation generation** and issues targeted clarifying questions to the user.

---

## Interactive AI ChatBot

The floating **Darukaa AI Assistant** (`ChatBotWidget.tsx`) provides continuous scientific support:
- **Real-Time Scientific Q&A**: Answers queries on glomalin aggregate stability, Faidherbia albida hydraulic lift, pollinator sub-lethal pesticide effects, and FAO carbon sequestration targets.
- **Context-Aware Clarification**: Automatically identifies missing variables when a user describes their farm, offering clickable suggestion chips.
- **Syncs with Diagnostic Workbench**: Ingested variables automatically populate the main environmental profile.
- **One-Click Copy & Clear**: Easily export AI responses and reset dialogue threads.

---

## Automated Test Suite (24 Test Cases)

The platform includes 24 automated unit and integration tests covering all critical invariants.

### Running Tests from Command Line
```bash
python3 -m unittest discover tests -v
```

### Running Tests Inside the Web Application
1. Click the **"Test Suite (24 Passed)"** button in the top navigation bar.
2. The modal triggers `/api/tests/run` in the backend.
3. View real-time test execution results, execution latency (ms), suite filters, and terminal logs.

### Test Suite Breakdown

| Suite | File | Tests | Validated Invariant |
|---|---|:---:|---|
| **ChatBot Engine** | `tests/test_chatbot.py` | **7** | Clarification on sparse data, progressive memory accumulation, 3-variable enforcement, trophic cascades, session persistence, edge cases. |
| **API Integration** | `tests/test_api_endpoints.py` | **6** | `/api/health`, `/api/knowledge/search`, sparse vs. complete `/api/chat`, DOCX and ZIP streaming. |
| **RAG Pipeline** | `tests/test_rag.py` | **3** | Document chunking, embedding generation, vector similarity retrieval. |
| **Reasoning Engine** | `tests/test_reasoning.py` | **3** | Multi-metric coupling, insufficient data detection, pesticide-pollinator feedback loops. |
| **Citation Validator** | `tests/test_citations.py` | **3** | Canonical source verification, citation matching, ungrounded claim refusal. |
| **Conversational Memory** | `tests/test_conversations.py` | **2** | Incremental profile building and dynamic clarifying question generation. |

---

## Getting Started

### Prerequisites
- **Node.js**: v18.0.0 or higher
- **Python**: 3.10 or higher
- **Gemini API Key**: (Optional for enhanced LLM generation; system includes robust offline fallback)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/darukaa-earth/darukaa-ai.git
   cd darukaa-earth
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your optional GEMINI_API_KEY
   ```

### Running the Application

- **Full-Stack Development Mode (Express + React Vite)**:
  ```bash
  npm run dev
  ```
  The app binds to `http://localhost:3000`.

- **Production Build & Execution**:
  ```bash
  npm run build
  npm start
  ```

- **Standalone Python FastAPI Service**:
  ```bash
  python3 run.py
  ```
  The FastAPI service runs on `http://localhost:8000` with interactive Swagger docs at `http://localhost:8000/docs`.

---

## Official Submission Documents

The project includes submission artifacts accessible directly through the web UI navigation bar:
- **Official Submission Document**: `submission/Darukaa_Earth_Submission.docx` (downloadable via `/api/submission/docx`)
  - 8 formal chapters covering Scientific Grounding, RAG Architecture, Multi-Metric Engine, Trophic Modeling, API Reference, and 25 peer-reviewed citations.
- **Source Code Archive**: `darukaa_earth_ai_biodiversity.zip` (downloadable via `/api/submission/zip`)
  - Regenerated using `python3 scripts/package_submission.py`.

---

## Citation & Academic Literature

Darukaa.Earth grounds all recommendations in peer-reviewed scientific treatises, including:
1. **FAO (2020)**: *Recarbonizing Global Soils — A Technical Manual of Recommended Management Practices*. Food and Agriculture Organization of the United Nations, Rome.
2. **IPBES (2019)**: *Global Assessment Report on Biodiversity and Ecosystem Services*. Intergovernmental Science-Policy Platform on Biodiversity and Ecosystem Services, Bonn.
3. **IPCC (2019)**: *Special Report on Climate Change, Desertification, Land Degradation, Sustainable Land Management, Food Security, and Greenhouse Gas Fluxes in Terrestrial Ecosystems*. Intergovernmental Panel on Climate Change.
4. **Goulson, D. et al. (2015)**: *Combined pesticide exposure severely affects individual- and colony-level traits in bees*. Science, 347(6229).
5. **Rillig, M. C. (2004)**: *Arbuscular mycorrhizae, glomalin, and soil aggregation*. Canadian Journal of Soil Science, 84(4), 355-363.
6. **Bayala, J. et al. (2015)**: *Hydraulic redistribution: Consequences for water, carbon, and nutrient fluxes in agroforestry systems*. Ecohydrology, 8(8), 1435-1448.
