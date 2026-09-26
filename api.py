"""
CareerPilot AI — FastAPI backend
Wraps existing agents with zero changes to their internal logic.
"""

import asyncio
import json
import uuid
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

# ──────────────────────────────────────────
# App setup
# ──────────────────────────────────────────

app = FastAPI(title="CareerPilot AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the static frontend
_static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(_static_dir):
    app.mount("/static", StaticFiles(directory=_static_dir), name="static")

# ──────────────────────────────────────────
# In-memory session store
# ──────────────────────────────────────────

sessions: dict[str, dict[str, Any]] = {}


# ──────────────────────────────────────────
# Request / Response models
# ──────────────────────────────────────────

class StartRequest(BaseModel):
    user_input: str


class AnswersRequest(BaseModel):
    answers: list[dict]  # [{question, requirement, category, question_type, answer}]


# ──────────────────────────────────────────
# SSE helper
# ──────────────────────────────────────────

def sse(event: str, data: Any) -> str:
    payload = json.dumps({"event": event, **data} if isinstance(data, dict) else {"event": event, "data": data})
    return f"data: {payload}\n\n"


# ──────────────────────────────────────────
# Serialisers — convert Pydantic to plain dict
# ──────────────────────────────────────────

def serialise_career_goal(cg) -> dict:
    return {
        "career": cg.career,
        "country": cg.country,
        "timeline": cg.timeline,
    }


def serialise_requirement(r) -> dict:
    return {
        "requirement": r.requirement,
        "category": r.category,
        "importance": r.importance,
        "explanation": r.explanation,
    }


def serialise_research(report) -> dict:
    return {
        "career_overview": report.career_overview,
        "requirements": [serialise_requirement(r) for r in report.requirements],
        "career_information": {
            "salary_range": report.career_information.salary_range,
            "job_outlook": report.career_information.job_outlook,
            "typical_responsibilities": report.career_information.typical_responsibilities,
            "work_environment": report.career_information.work_environment,
        },
    }


def serialise_question(q) -> dict:
    return {
        "question": q.question,
        "requirement": q.requirement,
        "category": q.category,
        "question_type": q.question_type,
    }


def serialise_gap(g) -> dict:
    return {
        "requirement": g.requirement,
        "category": g.category,
        "importance": g.importance,
        "user_status": g.user_status,
        "gap_level": g.gap_level,
        "explanation": g.explanation,
    }


def serialise_resource(r) -> dict:
    return {
        "title": r.title,
        "url": r.url,
        "why_recommended": r.why_recommended,
    }


# ──────────────────────────────────────────
# Endpoints
# ──────────────────────────────────────────

@app.get("/")
def root():
    """Serve the frontend HTML."""
    index = os.path.join(os.path.dirname(__file__), "static", "index.html")
    return FileResponse(index)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/start")
def start(req: StartRequest):
    """
    Parse career goal from free-text input.
    Creates a session and returns session_id + parsed career_goal.
    """
    from agents.career_agent import understand_career_goal

    try:
        career_goal = understand_career_goal(req.user_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Career goal parsing failed: {e}")

    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "career_goal": career_goal,
        "research": None,
        "questions": None,
        "answers": None,
        "skill_gap": None,
        "resources": None,
        "roadmap": None,
    }

    return {
        "session_id": session_id,
        "career_goal": serialise_career_goal(career_goal),
    }


@app.get("/api/analyze/{session_id}")
async def analyze(session_id: str):
    """
    SSE stream: runs research + question generation.
    Emits step events as each agent completes.
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    career_goal = session["career_goal"]

    async def event_stream():
        loop = asyncio.get_event_loop()

        # ── Step 1: Research ──
        yield sse("step", {"step": "research", "status": "running", "label": "Researching career requirements..."})
        try:
            from agents.research_agent import research_career
            research_report, _ = await loop.run_in_executor(
                None, research_career, career_goal.career, career_goal.country
            )
            session["research"] = research_report
            yield sse("step", {
                "step": "research",
                "status": "done",
                "label": "Career requirements researched",
                "data": serialise_research(research_report),
            })
        except Exception as e:
            yield sse("error", {"message": f"Research failed: {e}"})
            return

        # ── Step 2: Questions ──
        yield sse("step", {"step": "questions", "status": "running", "label": "Building your assessment..."})
        try:
            from agents.question_agent import generate_career_questions
            questions = await loop.run_in_executor(
                None, generate_career_questions, career_goal.career, research_report
            )
            session["questions"] = questions
            yield sse("step", {
                "step": "questions",
                "status": "done",
                "label": "Assessment ready",
                "data": [serialise_question(q) for q in questions.questions],
            })
        except Exception as e:
            yield sse("error", {"message": f"Question generation failed: {e}"})
            return

        yield sse("done", {"message": "Phase 1 complete"})

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.post("/api/submit-answers/{session_id}")
def submit_answers(session_id: str, req: AnswersRequest):
    """Store user answers from the assessment step."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    from agents.user_profile import UserAnswer, UserProfile

    session = sessions[session_id]
    career_goal = session["career_goal"]

    user_answers = [
        UserAnswer(
            question=a["question"],
            requirement=a["requirement"],
            category=a["category"],
            question_type=a["question_type"],
            answer=a["answer"],
        )
        for a in req.answers
    ]

    session["answers"] = UserProfile(
        career=career_goal.career,
        timeline=career_goal.timeline,
        country=career_goal.country,
        answers=user_answers,
    )

    return {"ok": True}


@app.get("/api/complete/{session_id}")
async def complete(session_id: str):
    """
    SSE stream: runs skill-gap analysis, resource discovery and roadmap generation.
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]

    if not session.get("answers"):
        raise HTTPException(status_code=400, detail="Answers not submitted yet")

    async def event_stream():
        loop = asyncio.get_event_loop()
        research_report = session["research"]
        user_profile = session["answers"]
        career_goal = session["career_goal"]

        # ── Step 3: Skill Gap ──
        yield sse("step", {"step": "skill_gap", "status": "running", "label": "Analyzing your skill gaps..."})
        try:
            from agents.skill_gap_agent import analyze_skill_gaps
            gap_report = await loop.run_in_executor(
                None, analyze_skill_gaps, research_report, user_profile
            )
            session["skill_gap"] = gap_report
            yield sse("step", {
                "step": "skill_gap",
                "status": "done",
                "label": "Skill gaps identified",
                "data": [serialise_gap(g) for g in gap_report.gaps],
            })
        except Exception as e:
            yield sse("error", {"message": f"Skill gap analysis failed: {e}"})
            return

        # ── Step 4: Resources (parallel) ──
        yield sse("step", {"step": "resources", "status": "running", "label": "Finding free learning resources..."})
        try:
            from agents.resource_agent import find_resources_for_gap
            gaps_with_needs = [g for g in gap_report.gaps if g.gap_level != "None"]

            async def fetch_resource(gap):
                report = await loop.run_in_executor(
                    None,
                    lambda g=gap: find_resources_for_gap(
                        requirement=g.requirement,
                        category=g.category,
                        importance=g.importance,
                        user_status=g.user_status,
                    )
                )
                return {
                    "requirement": gap.requirement,
                    "gap_level": gap.gap_level,
                    "resources": [serialise_resource(r) for r in report.resources],
                }

            resource_reports = await asyncio.gather(*[fetch_resource(g) for g in gaps_with_needs])
            resource_reports = list(resource_reports)
            session["resources"] = resource_reports
            yield sse("step", {
                "step": "resources",
                "status": "done",
                "label": "Resources found",
                "data": resource_reports,
            })
        except Exception as e:
            yield sse("error", {"message": f"Resource discovery failed: {e}"})
            return

        # ── Step 5: Roadmap ──
        yield sse("step", {"step": "roadmap", "status": "running", "label": "Creating your personalized roadmap..."})
        try:
            from agents.roadmap_agent import generate_roadmap
            from agents.resource_agent import LearningResource

            # Rebuild resource_reports with Pydantic objects for roadmap_agent
            rr_for_roadmap = []
            for item in resource_reports:
                rr_for_roadmap.append({
                    "requirement": item["requirement"],
                    "gap_level": item["gap_level"],
                    "resources": [
                        LearningResource(
                            title=r["title"],
                            url=r["url"],
                            why_recommended=r["why_recommended"],
                        )
                        for r in item["resources"]
                    ],
                })

            gap_report_obj = session["skill_gap"]
            roadmap_text = await loop.run_in_executor(
                None,
                lambda: generate_roadmap(
                    career_goal=career_goal,
                    gap_report=gap_report_obj,
                    resource_reports=rr_for_roadmap,
                )
            )
            session["roadmap"] = roadmap_text
            yield sse("step", {
                "step": "roadmap",
                "status": "done",
                "label": "Roadmap ready",
                "data": roadmap_text,
            })
        except Exception as e:
            yield sse("error", {"message": f"Roadmap generation failed: {e}"})
            return

        yield sse("done", {"message": "Analysis complete"})

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.get("/api/session/{session_id}")
def get_session(session_id: str):
    """Return full session state (for page-refresh recovery)."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    s = sessions[session_id]
    return {
        "career_goal": serialise_career_goal(s["career_goal"]) if s["career_goal"] else None,
        "research": serialise_research(s["research"]) if s["research"] else None,
        "questions": [serialise_question(q) for q in s["questions"].questions] if s["questions"] else None,
        "skill_gap": [serialise_gap(g) for g in s["skill_gap"].gaps] if s["skill_gap"] else None,
        "resources": s["resources"],
        "roadmap": s["roadmap"],
    }
