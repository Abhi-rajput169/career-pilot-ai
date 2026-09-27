# 🚀 CareerPilot AI

> **An intelligent, agentic career preparation assistant powered by local LLMs (Ollama) and a beautiful React frontend.**

CareerPilot AI takes a single sentence — *"I want to become a Data Scientist in 6 months"* — and runs it through a multi-agent pipeline to deliver a fully personalized **career roadmap**, **skill gap analysis**, and **free learning resources**, all in real time.

---

## 📸 What It Does

1. **Understands your goal** — extracts career, timeline, and country from natural language
2. **Researches the career** — finds real requirements, salary, job outlook, and responsibilities using web search
3. **Asks smart questions** — generates customized assessment questions based on actual career requirements
4. **Analyzes your gaps** — compares your answers against career requirements to find skill gaps
5. **Finds free resources** — discovers free YouTube tutorials and courses for every gap
6. **Builds your roadmap** — creates a step-by-step personalized preparation roadmap

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────┐
│           React Frontend           │
│  (Vite + Tailwind + Framer Motion)  │
└──────────────────┬──────────────────┘
                   │ HTTP / SSE
┌──────────────────▼──────────────────┐
│         FastAPI Backend (api.py)    │
│    Session management + SSE streams │
└──────────────────┬──────────────────┘
                   │
    ┌──────────────▼──────────────┐
    │       Agent Pipeline        │
    │                             │
    │  1. career_agent.py         │
    │  2. research_agent.py       │
    │  3. question_agent.py       │
    │  4. user_profile.py         │
    │  5. skill_gap_agent.py      │
    │  6. resource_agent.py       │
    │  7. roadmap_agent.py        │
    └──────────────┬──────────────┘
                   │
    ┌──────────────▼──────────────┐
    │      Ollama (Local LLM)     │
    │      qwen2.5:1.5b model     │
    └─────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | Ollama (`qwen2.5:1.5b`) — runs **100% locally**, no API keys needed |
| **Agent Framework** | LangChain + LangGraph |
| **Web Search** | DuckDuckGo Search (`ddgs`) |
| **Backend** | FastAPI + Uvicorn |
| **Streaming** | Server-Sent Events (SSE) |
| **Frontend** | React 18 + Vite + Tailwind CSS v4 |
| **Animations** | Framer Motion |
| **Icons** | Lucide React |
| **HTTP Client** | Axios |
| **Python Version** | 3.13+ |
| **Package Manager** | `uv` |

---

## 📁 Project Structure

```
Career-Pilot AI/
│
├── agents/                    # Core AI agent pipeline
│   ├── career_agent.py        # Parses career goal from user input
│   ├── research_agent.py      # Researches career requirements via web search
│   ├── question_agent.py      # Generates assessment questions
│   ├── user_profile.py        # Collects and stores user answers
│   ├── skill_gap_agent.py     # Analyzes skill gaps vs requirements
│   ├── resource_agent.py      # Finds free learning resources (YouTube, etc.)
│   └── roadmap_agent.py       # Generates the final personalized roadmap
│
├── frontend/                  # React + Vite frontend app
│   ├── src/
│   │   ├── pages/             # One page per pipeline step
│   │   ├── components/        # Reusable UI components
│   │   ├── api.js             # All API calls to the backend
│   │   └── App.jsx            # Main app with routing/state
│   ├── package.json
│   └── vite.config.js
│
├── static/                    # Built frontend (served by FastAPI)
│
├── api.py                     # FastAPI app — all REST + SSE endpoints
├── main.py                    # CLI entrypoint (run pipeline in terminal)
├── pyproject.toml             # Python dependencies (uv)
└── README.md
```

---

## ⚙️ Prerequisites

Before you begin, make sure you have the following installed:

| Requirement | Version | Install |
|---|---|---|
| **Python** | 3.13+ | [python.org](https://python.org) |
| **uv** | latest | `pip install uv` |
| **Node.js** | 18+ | [nodejs.org](https://nodejs.org) |
| **Ollama** | latest | [ollama.com](https://ollama.com) |

---

## 🚀 Setup & Installation

### Step 1 — Clone the Repository

```bash
git clone https://github.com/Abhi-rajput169/career-pilot-ai.git
cd "career-pilot-ai"
```

### Step 2 — Pull the LLM Model

Make sure Ollama is running, then pull the required model:

```bash
ollama pull qwen2.5:1.5b
```

> ✅ This model is small (~1 GB) and runs fast even on CPU.

### Step 3 — Install Python Dependencies

```bash
uv sync
```

This will create a virtual environment and install all dependencies from `pyproject.toml` automatically.

### Step 4 — Install Frontend Dependencies

```bash
cd frontend
npm install
```

---

## ▶️ Running the Application

### Option A — Full Web App (Recommended)

**Terminal 1 — Start the Backend:**

```bash
uv run uvicorn api:app --reload --port 8000
```

**Terminal 2 — Start the Frontend Dev Server:**

```bash
cd frontend
npm run dev
```

Then open **[http://localhost:5173](http://localhost:5173)** in your browser.

---

### Option B — CLI Mode (Terminal Only)

If you just want to run the full pipeline in your terminal without the frontend:

```bash
uv run python main.py
```

You will be asked:
```
What career do you want to prepare for?
```
Type something like: `I want to become a Machine Learning Engineer in India in 6 months`

The pipeline runs step by step and prints results directly to the terminal.

---

## 🌐 API Reference

The FastAPI backend exposes the following endpoints:

### `GET /` 
Serves the built frontend `index.html`.

---

### `GET /api/health`
Health check.

**Response:**
```json
{ "status": "ok" }
```

---

### `POST /api/start`
Parse the user's career goal and create a session.

**Request body:**
```json
{
  "user_input": "I want to become a Data Scientist in 6 months in India"
}
```

**Response:**
```json
{
  "session_id": "uuid-string",
  "career_goal": {
    "career": "Data Scientist",
    "country": "India",
    "timeline": "6 months"
  }
}
```

---

### `GET /api/analyze/{session_id}` — SSE Stream
Runs **Phase 1**: career research + question generation.  
Streams real-time progress events.

**Events emitted:**
| Event | Description |
|---|---|
| `step` (research running) | Research has started |
| `step` (research done) | Research result with requirements, overview, salary |
| `step` (questions running) | Question generation started |
| `step` (questions done) | Assessment questions ready |
| `done` | Phase 1 complete |
| `error` | Something went wrong |

---

### `POST /api/submit-answers/{session_id}`
Submit the user's answers to the assessment questions.

**Request body:**
```json
{
  "answers": [
    {
      "question": "Do you know Python?",
      "requirement": "Python Programming",
      "category": "Technical Skill",
      "question_type": "yes_no",
      "answer": "Yes"
    }
  ]
}
```

---

### `GET /api/complete/{session_id}` — SSE Stream
Runs **Phase 2**: skill gap analysis + resource discovery + roadmap generation.

**Events emitted:**
| Event | Description |
|---|---|
| `step` (skill_gap done) | List of analyzed skill gaps |
| `step` (resources done) | Free learning resources per gap |
| `step` (roadmap done) | Full personalized roadmap text |
| `done` | Pipeline complete |

---

### `GET /api/session/{session_id}`
Retrieve the full session state (useful for page-refresh recovery).

---

## 🤖 Agent Pipeline — Deep Dive

### 1. `career_agent.py`
Uses structured LLM output to extract `career`, `timeline`, and `country` from any free-text user input.

### 2. `research_agent.py`
Searches the web (DuckDuckGo) for real career data. Returns:
- **Career overview** — what the role is
- **Requirements** — atomic, single-skill requirements with category and importance
- **Career information** — salary range, job outlook, responsibilities, work environment

### 3. `question_agent.py`
Generates one unique, targeted question per career requirement. Questions are typed as:
- `yes_no` — for binary skills
- `scale_1_5` — for proficiency levels
- `text` — for open-ended experience answers

### 4. `user_profile.py`
Stores the user's answers tied to each requirement for downstream gap analysis.

### 5. `skill_gap_agent.py`
Compares user answers against researched requirements and assigns each a gap level:
- `None` — no gap, skill is covered
- `Low` — minor gap
- `Medium` — needs significant improvement
- `High` — critical gap, must work on this

### 6. `resource_agent.py`
For every gap (level ≠ `None`), finds free YouTube videos and tutorials specific to that skill.

### 7. `roadmap_agent.py`
Synthesizes everything — career goal, gaps, and resources — into a structured, week-by-week preparation roadmap.

---

## 🧩 Frontend Pages

The React app is a guided multi-step wizard:

| Page | Purpose |
|---|---|
| **GoalPage** | User enters their career goal |
| **ResearchPage** | Shows career overview, requirements, salary |
| **AssessmentPage** | Interactive question form |
| **SkillGapPage** | Visual skill gap breakdown |
| **ResourcesPage** | Free learning resources per gap |
| **RoadmapPage** | Final personalized roadmap |

---

## 🔒 Privacy

All processing happens **locally on your machine**:
- The LLM (`qwen2.5:1.5b`) runs via **Ollama** — no cloud API calls, no data sent to OpenAI or any third party
- Web searches use **DuckDuckGo** which does not track users
- No user data is stored to disk — all session data lives in memory and is lost when the server restarts

---

## 🐛 Troubleshooting

| Problem | Fix |
|---|---|
| `Connection refused` on backend | Make sure `uvicorn` is running on port 8000 |
| `ollama: command not found` | Install Ollama from [ollama.com](https://ollama.com) |
| Model not found error | Run `ollama pull qwen2.5:1.5b` |
| Frontend shows blank page | Run `npm run dev` inside the `frontend/` folder |
| `uv: command not found` | Run `pip install uv` first |
| SSE stream stops early | Check that Ollama is running: `ollama list` |

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is open-source. Feel free to use, modify, and distribute it.

---

<div align="center">
  <strong>Built with ❤️ using local AI — no cloud, no API keys, just your machine.</strong>
</div>
