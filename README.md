# 🧠 EngineIQ — Engineering Knowledge RAG System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6B35?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

**Turn your engineering documentation into an intelligent, queryable knowledge base.**

[🚀 Live Demo](#) · [📖 Docs](#usage) · [🐛 Issues](../../issues)

</div>

---

## 📌 What is EngineIQ?

EngineIQ is a **Retrieval-Augmented Generation (RAG)** system built for engineering teams.  
It ingests your internal documentation — ADRs, runbooks, API specs, incident reports, policies — and lets you query it in natural language using a powerful LLM, grounded strictly in your own knowledge base.

> **No hallucinations. No guessing. Only answers backed by your own docs.**

---

## ✨ Features

| Feature | Details |
|---------|---------|
| 📄 **Multi-format Ingestion** | Supports `.md`, `.pdf`, and `.txt` documents |
| 🧹 **Smart Cleaning Pipeline** | OCR error fixing, boilerplate removal, deduplication — 10-step pipeline |
| ✂️ **Structure-Aware Chunking** | Respects Markdown headings and document hierarchy |
| 🔍 **3 Retrieval Strategies** | Similarity · MMR · Hybrid (BM25 + Semantic) |
| 🤖 **Groq LLM** | Fast inference with Llama 3 or any Groq-supported model |
| 🔗 **LangSmith Tracing** | Full observability for every query |
| 🎛️ **Streamlit UI** | Simple, clean chat interface with source attribution |

---

## 🏗️ Architecture

```
Documents (PDF / MD / TXT)
        │
        ▼
  ┌─────────────┐
  │   Loader    │  DirectoryLoader — multi-format support
  └──────┬──────┘
         │
         ▼
  ┌─────────────────────┐
  │  Cleaning Pipeline  │  10-step: noise removal → OCR fix → normalization
  └──────────┬──────────┘
             │
             ▼
  ┌───────────────────────┐
  │  Structure-Aware      │  Respects Markdown section hierarchy
  │  Chunker              │  + metadata: title, section, parent
  └──────────┬────────────┘
             │
             ▼
  ┌──────────────────────┐
  │  HuggingFace         │  all-MiniLM-L6-v2 embeddings
  │  Embeddings          │
  └──────────┬───────────┘
             │
             ▼
  ┌──────────────────────┐
  │  ChromaDB            │  Persistent local vector store
  └──────────┬───────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
 User Query      Retriever (Similarity / MMR / Hybrid)
    │                 │
    └────────┬────────┘
             │
             ▼
  ┌──────────────────────┐
  │   Groq LLM           │  Grounded answer generation
  │   + Prompt           │
  └──────────┬───────────┘
             │
             ▼
     Answer + Sources
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- A [Groq API key](https://console.groq.com/)
- *(Optional)* A [LangSmith API key](https://smith.langchain.com/) for tracing

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/engineiq.git
cd engineiq
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r Requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
# Required
llm_api_key=your_groq_api_key
llm_model_name=llama-3.3-70b-versatile

# Optional — LangSmith tracing
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key
```

### 5. Add your documents

Place your documents inside `Data/Documents/`:

```
Data/Documents/
├── markdown/    ← .md files (ADRs, guides, runbooks...)
├── Pdf/         ← .pdf files (API specs, architecture docs...)
└── Txt/         ← .txt files (incident reports, policies...)
```

### 6. Build the knowledge base

```bash
python ingest.py
```

### 7. Launch the app

```bash
streamlit run app.py
```

---

## 🔍 Retrieval Strategies

Select your retrieval strategy from the sidebar:

| Strategy | Best For |
|----------|----------|
| **Similarity** | Fast, precise semantic search |
| **MMR** | Diverse results, avoids repetition |
| **Hybrid** | Best overall — combines keyword (BM25) + semantic |

---

## 📁 Project Structure

```
engineiq/
├── app.py                      ← Streamlit entry point
├── ingest.py                   ← Run once to build the Vector DB
├── Requirements.txt
├── .env                        ← Your secrets (not committed)
│
├── Src/
│   ├── Config/
│   │   └── Settings.py         ← Pydantic settings (env-driven)
│   ├── Application/
│   │   └── rag_service.py      ← RAGService orchestrator
│   ├── Ingestion/
│   │   ├── Loader.py           ← Multi-format document loader
│   │   ├── Chunker.py          ← Text splitter
│   │   ├── Cleaning/           ← 10-step cleaning pipeline
│   │   └── chunking/           ← Structure-aware Markdown chunker
│   ├── Retriver/
│   │   ├── Embedding.py        ← HuggingFace embeddings
│   │   ├── Vector_Store.py     ← ChromaDB factory
│   │   └── retriver.py         ← Retrieval strategies
│   └── Generation/
│       ├── llm.py              ← Groq LLM
│       └── Prompt.py           ← System prompt
│
├── Data/
│   ├── Documents/              ← Your source documents
│   ├── Vector_DB/              ← ChromaDB (auto-generated)
│   ├── Evaluation/
│   │   └── questions.json      ← 30 evaluation questions
│   └── MetaData/
│       └── documents.json      ← Document registry
│
└── Test/
    └── cleaner_test.py
```

---

## 🧹 Cleaning Pipeline

The cleaning pipeline handles real-world noisy documents — OCR output, Confluence exports, mixed formatting:

```
Raw Text
  ↓  Remove noise patterns (separators, junk lines)
  ↓  Remove noise keywords (Confluence exports, Wiki headers)
  ↓  Remove boilerplate (page numbers, timestamps)
  ↓  Fix OCR errors (0→o, 1→l, targeted replacements)
  ↓  Remove consecutive duplicates
  ↓  Normalize punctuation (curly quotes, dashes)
  ↓  Normalize lines (strip leading/trailing whitespace)
  ↓  Remove global duplicate lines
  ↓  Normalize whitespace (tabs, multiple spaces)
  ↓  Remove empty lines
Clean Text ✅
```

---

## 📊 Evaluation

The project ships with **30 curated evaluation questions** across diverse categories:

| Type | Count | Example |
|------|-------|---------|
| `semantic` | 8 | "Why does the platform use Kafka?" |
| `exact` | 5 | "What HTTP status means unauthorized?" |
| `procedure` | 4 | "How do I roll back the Payment Service?" |
| `policy` | 3 | "Where should production secrets be stored?" |
| `multi-source` | 5 | "What should a client do on HTTP 429?" |
| `incident` | 2 | "What caused the duplicate payment charge?" |
| `version-aware` | 2 | "Which ADR version is current?" |
| `conflict` | 1 | "Is Kafka still the default for all async?" |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | [Groq](https://groq.com/) (Llama 3.3 70B) |
| Embeddings | [HuggingFace](https://huggingface.co/) — `all-MiniLM-L6-v2` |
| Vector Store | [ChromaDB](https://www.trychroma.com/) |
| Framework | [LangChain](https://www.langchain.com/) |
| UI | [Streamlit](https://streamlit.io/) |
| Observability | [LangSmith](https://smith.langchain.com/) |
| Settings | [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) |

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">
Built with ❤️ for engineering teams who deserve better documentation tooling.
</div>
