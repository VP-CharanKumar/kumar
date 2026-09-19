import {
  Document,
  Packer,
  Paragraph,
  TextRun,
  HeadingLevel,
  Table,
  TableRow,
  TableCell,
  WidthType,
  BorderStyle,
  AlignmentType,
  ShadingType,
  Header,
  Footer,
  PageNumber,
  NumberFormat,
  convertInchesToTwip
} from "docx";
import fs from "fs";
import path from "path";

async function generateSubmissionDocx() {
  const tableBorder = {
    top: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" },
    bottom: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" },
    left: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" },
    right: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" },
    insideHorizontal: { style: BorderStyle.SINGLE, size: 4, color: "E0E0E0" },
    insideVertical: { style: BorderStyle.SINGLE, size: 4, color: "E0E0E0" }
  };

  const headerCell = (text, widthPercent) =>
    new TableCell({
      width: { size: widthPercent, type: WidthType.PERCENTAGE },
      shading: { fill: "1E3A2F", type: ShadingType.CLEAR },
      children: [
        new Paragraph({
          children: [
            new TextRun({ text, bold: true, color: "FFFFFF", font: "Calibri", size: 21 })
          ]
        })
      ],
      margins: { top: 120, bottom: 120, left: 140, right: 140 }
    });

  const bodyCell = (text, widthPercent, isCode = false) =>
    new TableCell({
      width: { size: widthPercent, type: WidthType.PERCENTAGE },
      children: [
        new Paragraph({
          children: [
            new TextRun({
              text,
              font: isCode ? "Consolas" : "Calibri",
              size: isCode ? 19 : 21,
              color: isCode ? "1A365D" : "2D3748"
            })
          ]
        })
      ],
      margins: { top: 100, bottom: 100, left: 140, right: 140 }
    });

  const p = (text, options = {}) =>
    new Paragraph({
      children: [
        new TextRun({
          text,
          font: "Calibri",
          size: options.size || 22,
          bold: options.bold || false,
          italics: options.italics || false,
          color: options.color || "2D3748"
        })
      ],
      spacing: { after: options.after || 140, before: options.before || 0 },
      alignment: options.align || AlignmentType.LEFT
    });

  const h1 = (text) =>
    new Paragraph({
      heading: HeadingLevel.HEADING_1,
      children: [
        new TextRun({
          text,
          font: "Calibri",
          size: 32,
          bold: true,
          color: "1A3E31"
        })
      ],
      spacing: { before: 320, after: 160 }
    });

  const h2 = (text) =>
    new Paragraph({
      heading: HeadingLevel.HEADING_2,
      children: [
        new TextRun({
          text,
          font: "Calibri",
          size: 26,
          bold: true,
          color: "2D5A46"
        })
      ],
      spacing: { before: 240, after: 120 }
    });

  const bullet = (boldPrefix, text) =>
    new Paragraph({
      children: [
        new TextRun({ text: "• ", bold: true, color: "1A3E31", font: "Calibri", size: 22 }),
        new TextRun({ text: boldPrefix + " ", bold: true, color: "1A3E31", font: "Calibri", size: 22 }),
        new TextRun({ text, font: "Calibri", size: 22, color: "2D3748" })
      ],
      spacing: { after: 100 },
      indent: { left: convertInchesToTwip(0.25) }
    });

  const callout = (title, text, color = "E8F5E9", border = "2E7D32") =>
    new Table({
      width: { size: 100, type: WidthType.PERCENTAGE },
      borders: {
        top: { style: BorderStyle.NONE },
        bottom: { style: BorderStyle.NONE },
        right: { style: BorderStyle.NONE },
        left: { style: BorderStyle.SINGLE, size: 24, color: border }
      },
      rows: [
        new TableRow({
          children: [
            new TableCell({
              shading: { fill: color, type: ShadingType.CLEAR },
              children: [
                new Paragraph({
                  children: [
                    new TextRun({ text: title + "\n", bold: true, color: "1B5E20", font: "Calibri", size: 22 }),
                    new TextRun({ text, font: "Calibri", size: 21, color: "2D3748" })
                  ],
                  spacing: { after: 80 }
                })
              ],
              margins: { top: 140, bottom: 140, left: 180, right: 180 }
            })
          ]
        })
      ]
    });

  const codeBox = (codeLines) =>
    new Table({
      width: { size: 100, type: WidthType.PERCENTAGE },
      borders: {
        top: { style: BorderStyle.SINGLE, size: 4, color: "CBD5E0" },
        bottom: { style: BorderStyle.SINGLE, size: 4, color: "CBD5E0" },
        left: { style: BorderStyle.SINGLE, size: 4, color: "CBD5E0" },
        right: { style: BorderStyle.SINGLE, size: 4, color: "CBD5E0" }
      },
      rows: [
        new TableRow({
          children: [
            new TableCell({
              shading: { fill: "F7FAFC", type: ShadingType.CLEAR },
              children: codeLines.map(
                (line) =>
                  new Paragraph({
                    children: [new TextRun({ text: line, font: "Consolas", size: 19, color: "1A202C" })],
                    spacing: { after: 40 }
                  })
              ),
              margins: { top: 120, bottom: 120, left: 160, right: 160 }
            })
          ]
        })
      ]
    });

  const doc = new Document({
    creator: "Darukaa.Earth AI Team",
    title: "Darukaa.Earth: AI Biodiversity Intelligence Submission Document",
    description: "Official Hackathon Technical Submission and Architecture Report",
    sections: [
      {
        properties: {
          page: {
            margin: {
              top: convertInchesToTwip(1),
              bottom: convertInchesToTwip(1),
              left: convertInchesToTwip(1),
              right: convertInchesToTwip(1)
            }
          }
        },
        headers: {
          default: new Header({
            children: [
              new Paragraph({
                children: [
                  new TextRun({
                    text: "Darukaa.Earth — AI Biodiversity Intelligence System | Technical Submission Report",
                    font: "Calibri",
                    size: 18,
                    color: "718096"
                  })
                ],
                alignment: AlignmentType.RIGHT,
                spacing: { after: 120 }
              })
            ]
          })
        },
        footers: {
          default: new Footer({
            children: [
              new Paragraph({
                children: [
                  new TextRun({ text: "Page ", font: "Calibri", size: 18, color: "718096" }),
                  new TextRun({ children: [PageNumber.CURRENT], font: "Calibri", size: 18, color: "718096" }),
                  new TextRun({ text: " of ", font: "Calibri", size: 18, color: "718096" }),
                  new TextRun({ children: [PageNumber.TOTAL_PAGES], font: "Calibri", size: 18, color: "718096" }),
                  new TextRun({
                    text: "   |   Confidential — Darukaa.Earth Hackathon Review",
                    font: "Calibri",
                    size: 18,
                    color: "718096"
                  })
                ],
                alignment: AlignmentType.CENTER
              })
            ]
          })
        },
        children: [
          // TITLE BLOCK
          new Paragraph({
            children: [
              new TextRun({
                text: "Darukaa.Earth: AI Biodiversity Intelligence",
                bold: true,
                font: "Calibri",
                size: 48,
                color: "133E2B"
              })
            ],
            spacing: { before: 200, after: 100 },
            alignment: AlignmentType.CENTER
          }),
          new Paragraph({
            children: [
              new TextRun({
                text: "Scientific Intelligence for Healthier Ecosystems — Technical Submission Report",
                italics: true,
                font: "Calibri",
                size: 24,
                color: "2D5A46"
              })
            ],
            spacing: { after: 280 },
            alignment: AlignmentType.CENTER
          }),

          callout(
            "SUBMISSION STATUS & FORMAL NOTICE",
            "This document is the official, complete technical submission for the Darukaa.Earth AI Biodiversity Intelligence Hackathon Challenge. It details the end-to-end scientific reasoning engine, retrievable RAG pipeline, multi-metric interaction validator, conversational state memory, and evidence-grounded recommendation system.",
            "E8F5E9",
            "1B5E20"
          ),

          new Paragraph({ spacing: { after: 200 } }),

          // 1. Project Title
          h1("1. Project Title"),
          p("Darukaa.Earth: AI Biodiversity Intelligence System", { bold: true, size: 24 }),
          p("Subtitle: Scientific intelligence for healthier ecosystems."),
          p("Classification: Knowledge-Grounded Multi-Metric Environmental Reasoning Platform."),

          // 2. Problem Statement
          h1("2. Problem Statement"),
          p(
            "Global terrestrial biodiversity is declining at an unprecedented rate, accelerated by agricultural intensification, chemical pesticide overuse, monoculture expansion, and habitat fragmentation. While land managers, farmers, and conservationists routinely observe warning signs—such as plummeting insect numbers, topsoil erosion, and reduced crop vigor—most conventional digital advisory tools and generic LLMs fail to provide actionable ecological support."
          ),
          p("Generic AI systems exhibit fatal deficiencies in environmental intelligence:"),
          bullet("Shallow, Obvious Advice:", "Outputting ungrounded platitudes like 'use sustainable farming' or 'plant more trees' without mechanistic rationale or ecological context."),
          bullet("Single-Variable Tunnel Vision:", "Treating environmental metrics in isolation, ignoring that soil organic carbon, precipitation deficit, and cropping regime act synergistically."),
          bullet("Absence of Scientific Grounding:", "Hallucinating unverified studies, fictitious DOI citations, and unsupported percentage estimates."),
          bullet("Zero Environmental Memory:", "Failing to maintain progressive environmental profiles across multi-turn user dialogues."),

          // 3. Proposed Solution
          h1("3. Proposed Solution"),
          p(
            "Darukaa.Earth AI Biodiversity Intelligence is an expert environmental reasoning platform that behaves as an AI Environmental Scientist rather than a generic conversational bot. The system couples a curated, peer-reviewed scientific knowledge layer with a deterministic Multi-Metric Reasoning Engine, an Evidence Validation layer, and Google Gemini."
          ),
          p("The solution implements a closed-loop reasoning pipeline:"),
          bullet("Intelligent Input Ingestion:", "Parses freeform conversational text, structured JSON telemetry, and geographic coordinates into a formal Environmental Profile."),
          bullet("Missing Variable Detection:", "Identifies critical missing baseline parameters and prompts high-value clarifying questions rather than generating speculative recommendations."),
          bullet("Retrievable RAG Layer:", "Retrieves authoritative scientific research from FAO, IPCC, IPBES, UNEP, ICRAF, and USDA-NRCS stored in ChromaDB vector and structured document indexes."),
          bullet("Multi-Metric Coupling:", "Explicitly computes bi-directional interactions across at least three simultaneous environmental variables (e.g., SOC ↔ Soil Moisture ↔ Crop Regime)."),
          bullet("Evidence Grounding & Citation Validation:", "Rejects claims lacking traceable literature backing, assigning structured confidence levels and verifiable monitoring indicators."),

          // 4. Key Features
          h1("4. Key Features"),
          bullet("Multi-Metric Environmental Reasoning:", "Analyzes simultaneous interdependencies across soil health, rainfall patterns, biodiversity metrics, land use, and anthropogenic pressures."),
          bullet("Deterministic 3-Variable Validator:", "Enforces that no complex recommendation is emitted without proving mathematical or ecological interaction across at least three distinct metrics."),
          bullet("Targeted Clarification Engine:", "Proactively asks 2 to 4 high-value clarifying questions when critical environmental parameters are omitted."),
          bullet("Conversational State & Profile Synthesis:", "Maintains conversation history, incrementally updating soil pH, organic carbon, rainfall, and land use across multiple turns without requiring re-entry."),
          bullet("Rigorous Citation & Evidence Grounding:", "All recommended actions link directly to published scientific syntheses (FAO, IPCC, IPBES, UNEP, USDA) with specific mechanisms and time horizons."),
          bullet("Structured Dual Input Architecture:", "Accepts natural dialogue alongside direct JSON sensor payloads and latitude/longitude spatial coordinates."),
          bullet("Actionable Monitoring Protocols:", "Prescribes specific ecological indicators, sampling frequencies, and verification targets for every recommended intervention."),
          bullet("4 Built-in Hackathon Demo Scenarios:", "One-click execution of semi-arid cereal monocultures, pesticide/pollinator crises, forest fragmentation, and severe drought stress."),

          // 5. System Architecture
          h1("5. System Architecture"),
          p(
            "The system rejects naive end-to-end LLM architectures in favor of an orchestrated multi-stage pipeline where Gemini functions as a scientific synthesizer governed by deterministic validators."
          ),
          codeBox([
            "   [User Message / Structured JSON]                                ",
            "                 │                                                ",
            "                 ▼                                                ",
            "        Input Parser & Extractor                                  ",
            "                 │                                                ",
            "                 ▼                                                ",
            "    Conversational Memory & Profile Store (SQLite)                ",
            "                 │                                                ",
            "                 ▼                                                ",
            "        Missing Variable Detector                                 ",
            "          ├── Incomplete? ──► Generate Clarifying Questions       ",
            "          │                                                       ",
            "          └── Sufficient?                                         ",
            "                 │                                                ",
            "                 ▼                                                ",
            "       RAG Retriever (ChromaDB + Vector Store)                    ",
            "                 │                                                ",
            "                 ▼                                                ",
            "   Multi-Metric Reasoning Engine (>= 3 Environmental Variables)   ",
            "                 │                                                ",
            "                 ▼                                                ",
            "     Scientific LLM Synthesizer (Gemini API)                      ",
            "                 │                                                ",
            "                 ▼                                                ",
            "        Evidence & Citation Validator                             ",
            "                 │                                                ",
            "                 ▼                                                ",
            "  Recommendation Engine & Monitoring Plan Builder                 ",
            "                 │                                                ",
            "                 ▼                                                ",
            "   Structured Output UI / JSON Payload                            "
          ]),

          // 6. RAG Architecture
          h1("6. RAG Architecture"),
          p(
            "The Retrieval-Augmented Generation (RAG) system guarantees that all environmental analyses are anchored in verified scientific datasets. The pipeline is implemented via app/rag/ and comprises six modular components:"
          ),
          bullet("Document Loader (document_loader.py):", "Scans the knowledge/ repository, extracting markdown sections, frontmatter, and JSON schemas."),
          bullet("Semantic Chunker (chunker.py):", "Splits documents into coherent ecological units (500–800 tokens, 100-token overlap) respecting heading boundaries to prevent fragmenting scientific causal mechanisms."),
          bullet("Embedding Pipeline (embeddings.py):", "Computes dense semantic embeddings using Gemini text-embedding models with cosine distance indexing."),
          bullet("Vector Store (vector_store.py):", "Persists chunk vectors and metadata into an on-disk ChromaDB collection with fast filtered similarity querying."),
          bullet("Retriever & Reranker (retriever.py):", "Executes multi-query retrieval filtering by environmental category (soil, pollinators, climate, etc.) and returns top-k citations with relevance scores."),
          bullet("Ingestion CLI (scripts/ingest_knowledge.py):", "Provides an idempotent, automated ingestion tool that tracks file hashes to prevent redundant re-indexing."),

          // 7. Knowledge Base Design
          h1("7. Knowledge Base Design"),
          p(
            "The knowledge repository contains 10 rigorous ecological domains authored from primary intergovernmental reports and meta-analyses. No speculative claims or fictitious sources exist in the dataset."
          ),
          new Table({
            width: { size: 100, type: WidthType.PERCENTAGE },
            borders: tableBorder,
            rows: [
              new TableRow({
                children: [
                  headerCell("Domain", 25),
                  headerCell("Key Indicators & Concepts", 45),
                  headerCell("Authoritative Sources", 30)
                ]
              }),
              new TableRow({
                children: [
                  bodyCell("Soil Health", 25),
                  bodyCell("SOC (0.3-1.5%), pH dynamics, AMF fungi, bulk density, infiltration capacity", 45),
                  bodyCell("FAO (2020), USDA-NRCS (2021)", 30)
                ]
              }),
              new TableRow({
                children: [
                  bodyCell("Climate Stress", 25),
                  bodyCell("Aridity index, VPD, precipitation concentration, canopy thermal buffering", 45),
                  bodyCell("IPCC SRCCL (2019), FAO (2019)", 30)
                ]
              }),
              new TableRow({
                children: [
                  bodyCell("Land Use", 25),
                  bodyCell("Monoculture exhaustion, patch isolation, crop diversification indices", 45),
                  bodyCell("IPBES (2019), IPCC (2019)", 30)
                ]
              }),
              new TableRow({
                children: [
                  bodyCell("Pollinators", 25),
                  bodyCell("Neonicotinoid/organophosphate toxicity, floral sequence gaps, wild solitary bees", 45),
                  bodyCell("IPBES (2016), UNEP (2020)", 30)
                ]
              }),
              new TableRow({
                children: [
                  bodyCell("Agroforestry", 25),
                  bodyCell("Reverse phenology (Faidherbia), hydraulic lift, microclimate cooling", 45),
                  bodyCell("ICRAF / CIFOR (2018)", 30)
                ]
              }),
              new TableRow({
                children: [
                  bodyCell("Restoration", 25),
                  bodyCell("Stepping-stone corridors, structural connectivity, assisted natural regeneration", 45),
                  bodyCell("UNEP (2021), IPBES (2019)", 30)
                ]
              })
            ]
          }),

          // 8. Multi-Metric Reasoning
          h1("8. Multi-Metric Reasoning"),
          p(
            "The hallmark of Darukaa.Earth is its requirement that recommendations evaluate multi-variable feedbacks rather than single parameters. The Multi-Metric Reasoning Engine (app/services/environmental_reasoning.py) cross-references variables across four primary multi-metric coupling matrices:"
          ),
          bullet("Matrix A: Soil Carbon ↔ Rainfall Deficit ↔ Monoculture Stress:", "When SOC is depleted (<0.5%) and rainfall is low (<450 mm), monoculture wheat triggers compounded moisture stress. Cover cropping or agroforestry is evaluated with rainfall feasibility bounds."),
          bullet("Matrix B: Chemical Intensity ↔ Pollinator Loss ↔ Floral Diversity:", "High pesticide frequency combined with monoculture destroys natural pollinator populations, causing fruit-set decline. The system maps the biological transition to flowering buffer strips and IPPM."),
          bullet("Matrix C: Forest Fragmentation ↔ Water Stress ↔ Connectivity:", "Fragmented forest patches suffer desiccating perimeter edge effects and restricted wildlife dispersal. The system calculates optimal wildlife corridor widths."),
          bullet("Matrix D: Drought ↔ Soil Compaction ↔ Vegetative Cover:", "Low vegetative ground cover amplifies soil surface temperatures (>50°C), terminating microbial activity. The engine prescribes stubble mulching and contour water harvesting."),

          callout(
            "DETERMINISTIC 3-VARIABLE VALIDATION RULE",
            "The system explicitly checks: `len(variables_used_for_reasoning) >= 3`. If fewer than 3 environmental variables are provided or inferred with sufficient certainty, the engine flags this condition, reduces recommendation confidence to LOW, and prioritizes clarifying queries.",
            "FFF9C4",
            "FBC02D"
          ),

          // 9. Conversational Memory
          h1("9. Conversational Memory"),
          p(
            "Environmental assessments rarely happen in a single prompt. A farmer might first state 'My farm is semi-arid', subsequently mention 'Rainfall is 420mm', and in a third turn add 'Soil organic carbon tested at 0.3%'. The Conversational Memory engine maintains session-bound environmental state in SQLite:"
          ),
          bullet("Stateful Entity Extraction:", "Natural language messages are parsed for numerical and categorical environmental entities."),
          bullet("Non-Destructive Merge:", "Newly declared values update the session profile without erasing previously established parameters."),
          bullet("Clarification Tracking:", "Already answered clarifying questions are marked as resolved, preventing redundant questions in subsequent turns."),

          // 10. Evidence-Based Recommendation System
          h1("10. Evidence-Based Recommendation System"),
          p(
            "Every recommendation generated by app/services/recommendation_service.py adheres to a strictly typed schema containing:"
          ),
          bullet("Action:", "Precise agronomic or ecological intervention (e.g., 'Introduce drought-hardy cowpea cover crops in rotation')."),
          bullet("Why It Works (Scientific Mechanism):", "Causal explanation grounded in soil physics and microbiology (e.g., biological nitrogen fixation + aggregate glomalin binding)."),
          bullet("Impacted Metrics:", "List of specific environmental variables improved (e.g., SOC %, Water Retention, Mycorrhizal Biomass)."),
          bullet("Expected Direction:", "Directional vectors (+15–25% SOC over 2–3 years per FAO studies)."),
          bullet("Time Horizon:", "Categorized as Short Term (0–12 months), Medium Term (1–3 years), or Long Term (3+ years)."),
          bullet("Confidence Level:", "Calculated as HIGH, MEDIUM, or LOW based on data completeness and citation match."),
          bullet("Trade-offs & Constraints:", "Potential risks (e.g., cover crops consuming soil moisture in hyper-arid zones <300mm)."),
          bullet("Monitoring Plan:", "Specific testing intervals and measurement methods."),

          // 11. Database Schema
          h1("11. Database Schema"),
          p("The application utilizes an embedded, zero-configuration SQLite database with SQLAlchemy ORM models:"),
          new Table({
            width: { size: 100, type: WidthType.PERCENTAGE },
            borders: tableBorder,
            rows: [
              new TableRow({
                children: [
                  headerCell("Table Name", 25),
                  headerCell("Primary Columns", 45),
                  headerCell("Relationships & Purpose", 30)
                ]
              }),
              new TableRow({
                children: [
                  bodyCell("conversations", 25),
                  bodyCell("id (UUID), title, created_at, updated_at", 45),
                  bodyCell("Parent table for multi-turn sessions", 30)
                ]
              }),
              new TableRow({
                children: [
                  bodyCell("messages", 25),
                  bodyCell("id, conversation_id, sender (user/assistant), content, timestamp", 45),
                  bodyCell("Full message dialogue history", 30)
                ]
              }),
              new TableRow({
                children: [
                  bodyCell("environmental_profiles", 25),
                  bodyCell("id, conversation_id, region, land_use, crop_type, soc, rainfall, ph, lat, lon, etc.", 45),
                  bodyCell("Cumulative extracted environmental state", 30)
                ]
              }),
              new TableRow({
                children: [
                  bodyCell("recommendations", 25),
                  bodyCell("id, conversation_id, action, mechanism, metrics, horizon, confidence, sources", 45),
                  bodyCell("Historical recommendations log", 30)
                ]
              }),
              new TableRow({
                children: [
                  bodyCell("knowledge_sources", 25),
                  bodyCell("id, source_id, title, organization, category, year, doi_url, summary", 45),
                  bodyCell("Indexed scientific citations catalog", 30)
                ]
              })
            ]
          }),

          // 12. API Architecture
          h1("12. API Architecture"),
          p("The FastAPI backend exposes clean, RESTful endpoints adhering to strict Pydantic schemas:"),
          new Table({
            width: { size: 100, type: WidthType.PERCENTAGE },
            borders: tableBorder,
            rows: [
              new TableRow({
                children: [
                  headerCell("Method & Endpoint", 35),
                  headerCell("Request / Parameters", 35),
                  headerCell("Response Summary", 30)
                ]
              }),
              new TableRow({
                children: [
                  bodyCell("GET /api/health", 35, true),
                  bodyCell("None", 35),
                  bodyCell("System status, RAG & DB health", 30)
                ]
              }),
              new TableRow({
                children: [
                  bodyCell("POST /api/chat", 35, true),
                  bodyCell("{ conversation_id?, message, profile_override? }", 35, true),
                  bodyCell("Conversational reply, profile, RAG evidence", 30)
                ]
              }),
              new TableRow({
                children: [
                  bodyCell("POST /api/analyze", 35, true),
                  bodyCell("{ region, soil_organic_carbon, rainfall, ... }", 35, true),
                  bodyCell("Complete multi-metric scientific analysis", 30)
                ]
              }),
              new TableRow({
                children: [
                  bodyCell("GET /api/conversations/{id}", 35, true),
                  bodyCell("conversation_id path parameter", 35),
                  bodyCell("Conversation history and active profile", 30)
                ]
              }),
              new TableRow({
                children: [
                  bodyCell("DELETE /api/conversations/{id}", 35, true),
                  bodyCell("conversation_id path parameter", 35),
                  bodyCell("Session deletion confirmation", 30)
                ]
              }),
              new TableRow({
                children: [
                  bodyCell("GET /api/knowledge/search", 35, true),
                  bodyCell("?query=...&category=...&top_k=5", 35, true),
                  bodyCell("Top retrieved chunks and citations", 30)
                ]
              }),
              new TableRow({
                children: [
                  bodyCell("POST /api/knowledge/ingest", 35, true),
                  bodyCell("{ force_reindex?: boolean }", 35, true),
                  bodyCell("Ingestion metrics and chunk counts", 30)
                ]
              })
            ]
          }),

          // 13. Technology Stack
          h1("13. Technology Stack"),
          bullet("Core Language:", "Python 3.10+ / 3.11+"),
          bullet("API Framework:", "FastAPI & Starlette for high-throughput asynchronous HTTP serving."),
          bullet("Data Validation:", "Pydantic v2 for strict type enforcement and JSON serialization."),
          bullet("Vector Engine & RAG:", "ChromaDB with Gemini / Sentence-Transformers embedding integration."),
          bullet("Generative AI & Reasoning:", "Google Gemini API via the official @google/genai SDK."),
          bullet("Persistence & Database:", "SQLite 3 with SQLAlchemy ORM and Alembic-ready schemas."),
          bullet("Frontend Interface:", "Vanilla HTML5, CSS3, and modern ES6 JavaScript dashboard with zero complex build overhead for maximum local developer accessibility."),
          bullet("Containerization:", "Multi-stage Dockerfile and Docker Compose configuration."),
          bullet("Automated Testing:", "Pytest test suite with mocked AI adapters for deterministic offline execution."),

          // 14. Installation Instructions
          h1("14. Installation Instructions"),
          p("Prerequisites: Python 3.10 or higher, Git, and an active Google Gemini API key."),
          codeBox([
            "# 1. Clone or extract the project",
            "cd darukaa_earth_ai_biodiversity",
            "",
            "# 2. Create and activate a Python virtual environment",
            "python3 -m venv venv",
            "source venv/bin/activate    # Linux / macOS",
            "# venv\\Scripts\\activate   # Windows",
            "",
            "# 3. Install core dependencies",
            "pip install --upgrade pip",
            "pip install -r requirements.txt"
          ]),

          // 15. Local Setup
          h1("15. Local Setup"),
          p("Configure environment variables and initialize the local knowledge base:"),
          codeBox([
            "# 1. Copy environment template",
            "cp .env.example .env",
            "",
            "# 2. Set your Gemini API key in .env",
            "GEMINI_API_KEY=\"your_actual_gemini_api_key_here\"",
            "DATABASE_URL=\"sqlite:///./data/darukaa.db\"",
            "CHROMA_PATH=\"./chroma_db\"",
            "APP_ENV=\"development\"",
            "",
            "# 3. Ingest scientific knowledge base into ChromaDB",
            "python scripts/ingest_knowledge.py",
            "",
            "# 4. Launch the application",
            "python run.py",
            "# or alternatively: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload",
            "",
            "# 5. Open browser at: http://127.0.0.1:8000"
          ]),

          // 16. Testing
          h1("16. Testing"),
          p(
            "The repository includes a comprehensive automated test suite in tests/. All external Gemini API calls are safely mocked to ensure tests run offline without consuming API tokens or failing on network drops:"
          ),
          codeBox([
            "# Run the complete test suite with coverage report",
            "pytest -v",
            "",
            "# Run specific subsystem test suites",
            "pytest tests/test_api.py -v",
            "pytest tests/test_rag.py -v",
            "pytest tests/test_reasoning.py -v",
            "pytest tests/test_conversation.py -v",
            "pytest tests/test_recommendations.py -v"
          ]),

          // 17. CI/CD
          h1("17. CI/CD"),
          p(
            "The repository includes a pre-configured GitHub Actions workflow in .github/workflows/test.yml. The pipeline triggers on every push and pull request to main, provisioning Python 3.10 and 3.11 runners, installing dependencies, executing knowledge ingestion sanity checks, and running the full pytest test suite."
          ),

          // 18. Docker
          h1("18. Docker"),
          p("For containerized production deployment, the project includes Dockerfile and docker-compose.yml:"),
          codeBox([
            "# Build and launch the containerized application",
            "docker compose up --build -d",
            "",
            "# View live logs",
            "docker compose logs -f",
            "",
            "# Stop the container stack",
            "docker compose down"
          ]),

          // 19. Demo Scenarios
          h1("19. Demo Scenarios"),
          p("The system includes 4 fully populated, pre-configured scientific demo scenarios accessible via the web interface:"),
          bullet("Scenario 1: Semi-Arid Cereal Monoculture:", "SOC: 0.3%, Rainfall: 420mm/yr, Monoculture Wheat. Demonstrates multi-metric reasoning connecting carbon starvation, evaporative water deficit, and structural soil degradation, proposing legume cover crops and Faidherbia agroforestry."),
          bullet("Scenario 2: Pesticide Overuse & Pollinator Decline:", "Frequent organophosphate sprays, plummeting solitary bee visitation, simplified landscape. Proposes flowering buffer strips, nesting refugia, and twilight IPPM protocol."),
          bullet("Scenario 3: Forest Fragmentation & Water Stress:", "Disconnected woodland remnants, 600m patch isolation, drying streams. Recommends riparian stepping-stone corridors and assisted natural regeneration."),
          bullet("Scenario 4: Chronic Drought & Compaction:", "Rainfall: 280mm, Soil Moisture: 6%, High Soil Compaction. Triggers contour swale water-harvesting, stubble retention, and native drought-tolerant perennial grasses."),

          // 20. Limitations
          h1("20. Limitations"),
          bullet("Geospatial Grounding:", "Coordinates (lat/lon) are captured in the environmental profile, but automated satellite NDVI and precipitation extraction requires external GIS API keys not included by default."),
          bullet("Hyper-Local Microclimate Variations:", "Soil chemistry recommendations require laboratory soil test verification before physical fertilizer implementation."),
          bullet("Vector Context Windows:", "RAG chunk retrieval is capped at top-5 relevant chunks per turn to ensure fast response latency."),

          // 21. Future Enhancements
          h1("21. Future Enhancements"),
          bullet("Satellite Earth Observation Pipeline:", "Direct integration with Sentinel-2 and Landsat 8/9 multispectral feeds to auto-populate NDVI, NDWI, and soil moisture indices."),
          bullet("Federated Citizen-Science Ingestion:", "Real-time sync with GBIF (Global Biodiversity Information Facility) and iNaturalist observation APIs."),
          bullet("Automated Carbon Credit Calculation:", "Integration of Verra VM0042 methodology to quantify verified carbon units generated through recommended soil re-carbonization."),

          // 22. GitHub Repository Link
          h1("22. GitHub Repository Link"),
          callout(
            "OFFICIAL GITHUB REPOSITORY",
            "https://github.com/YOUR_USERNAME/darukaa-earth\n\n[PLACEHOLDER — UPDATE BEFORE SUBMISSION]\n(Replace YOUR_USERNAME with your GitHub handle prior to final portal submission)",
            "E3F2FD",
            "1976D2"
          ),

          // 23. Live Demo Link
          h1("23. Live Demo Link"),
          callout(
            "LIVE DEMO APPLICATION URL",
            "https://YOUR-LIVE-DEMO-URL\n\n[PLACEHOLDER — UPDATE BEFORE SUBMISSION]\n(Replace with your deployed Cloud Run / Render / AWS live URL prior to final portal submission)",
            "E3F2FD",
            "1976D2"
          ),

          // 24. Reviewer Instructions
          h1("24. Reviewer Instructions"),
          p("For Hackathon Evaluation Committee and Technical Reviewers:"),
          p(
            "As designated in the official Darukaa.Earth Hackathon Submission Guidelines, if the GitHub repository is set to private, collaborator access must be granted to the following reviewer accounts:"
          ),
          bullet("Reviewer 1:", "ankita.dasgupta@darukaa.com"),
          bullet("Reviewer 2:", "harsh.kumar@darukaa.com"),
          bullet("Reviewer 3:", "utkarsh.gauniyal@darukaa.com"),
          bullet("Reviewer 4:", "guneet.mutreja@darukaa.com"),
          p("If the repository is set to public, access invitations are not required and the repository link above will resolve directly."),
          p("Evaluation Checklist Reference:"),
          bullet("Depth of Reasoning (30%):", "Verified via Multi-Metric Interaction Matrix and the 3-variable validator."),
          bullet("Scientific Grounding (25%):", "Verified via RAG evidence drawer and citations from FAO, IPCC, IPBES, UNEP, and USDA."),
          bullet("Knowledge System Design (20%):", "Verified via ChromaDB vector store and 10 markdown knowledge base documents in knowledge/."),
          bullet("Conversational Intelligence (15%):", "Verified via stateful conversation memory and proactive clarifying questions for incomplete inputs."),
          bullet("Output Clarity (10%):", "Verified via structured recommendation cards, monitoring indicators, and time horizons.")
        ]
      }
    ]
  });

  const buffer = await Packer.toBuffer(doc);
  const outDir = path.resolve("./submission");
  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }
  const outFile = path.join(outDir, "Darukaa_Earth_Submission.docx");
  fs.writeFileSync(outFile, buffer);
  console.log(`Successfully generated valid Office Open XML Word document: ${outFile}`);
  console.log(`File size: ${buffer.length} bytes`);
}

generateSubmissionDocx().catch((err) => {
  console.error("Error generating DOCX:", err);
  process.exit(1);
});
