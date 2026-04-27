# Bluesky Post Explainer

An AI agent that explains Bluesky posts by searching for and synthesizing relevant context. Paste a post URL and get a concise bullet-point explanation of what it's about, who's involved, and why it matters.

---

## How it works

```
Bluesky URL
     │
     ▼
1. FETCH       — retrieve the post text via the AT Protocol
     │
     ▼
2. GENERATE    — LLM produces search queries and extracts named entities
     │
     ▼
3. RERANK      — embed queries + entities, rank by cosine similarity to the post,
                 keep the top 3 most relevant search terms
     │
     ▼
4. SEARCH      — search Bluesky for each top-ranked term to gather context posts
     │
     ▼
5. SUMMARIZE   — LLM synthesizes the original post + context into 3–5 bullet points
```

---

## Prerequisites

### Python 3.11+
```bash
# macOS
brew install python

# or download from https://python.org
```

### uv (Python package manager)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Node.js 18+
```bash
# macOS
brew install node

# or download from https://nodejs.org
```

---

## Setup

### 1. Clone and install
```bash
git clone https://github.com/cirofdo/bsky-post-explainer
cd bsky-agent
uv sync
```

### 2. Configure environment
```bash
cp backend/.env.example backend/.env
```

Fill in `backend/.env`:

```env
# Bluesky — generate an App Password at: bsky.app → Settings → Privacy & Security → App Passwords
BSKY_HANDLE=yourname.bsky.social
BSKY_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx

# OpenAI — get your key at: platform.openai.com/api-keys
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

### 3. Run the backend
```bash
uv run uvicorn backend.app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### 4. Run the frontend
```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## Evaluation

Run the evaluation harness against the 10 test cases in `eval/test_cases.json`:

```bash
uv run eval/run_eval.py
```

Results are saved to `eval/results.json`. Each test case is scored by an LLM judge that checks how many expected concepts the explanation covers. A test passes if ≥ 50% of concepts are covered.

**Latest results: 9/10 passed | avg concept coverage: 81%**

---

## Key design decisions

### Prompts in `prompts.yaml`
All LLM prompts live in a single config file. No hardcoded strings in code — prompts can be iterated without touching Python.

### Dual retrieval: queries + entities
The agent generates two types of search terms from the post:
- **Queries** — broad topical searches (e.g. `"AI coding agents 2025"`)
- **Entities** — specific named things (e.g. `"Geoffrey Huntley"`, `"Claude"`)

This gives both topical breadth and named-entity precision.

### Embedding-based reranking (ML module)
Before searching, all candidate search terms (queries + entities) are embedded using `text-embedding-3-small`. Each is scored by cosine similarity to the original post embedding. Only the top 3 most semantically relevant terms are used for retrieval.

### Bluesky as the search space
Uses Bluesky's native search API.

### LLM-as-judge evaluation
The eval harness uses an LLM to score explanations against a list of expected concepts per test case.
