from typing import Literal
from pydantic import BaseModel, Field


# ============================================================
# MODELS
# ============================================================

class CareerQuestion(BaseModel):
    question: str = Field(
        description="A specific technical question assessing the user's current ability"
    )

    requirement: str = Field(
        description="The exact requirement text from the career research"
    )

    category: Literal[
        "skill", "technology", "education", "experience",
        "certification", "license", "exam", "other",
    ]

    question_type: Literal["level", "yes_no", "number", "text"]


class CareerQuestions(BaseModel):
    questions: list[CareerQuestion]


# ============================================================
# DETERMINISTIC QUESTION TEMPLATES
# ============================================================
# No LLM — questions are generated from templates.
# This guarantees: correct type, technical focus, no soft questions.

def build_question(requirement: str, category: str) -> tuple[str, str]:
    """
    Returns (question_text, question_type).
    Templates are specific and technical per category.
    """
    category = category.strip().lower()
    r = requirement.strip()

    if category == "skill":
        return (
            f"How would you rate your current {r} skill level?",
            "level"
        )

    elif category == "technology":
        return (
            f"How would you rate your hands-on experience with {r}?",
            "level"
        )

    elif category == "education":
        r_clean = r.rstrip(".")
        return (
            f"Do you currently hold a {r_clean}?",
            "yes_no"
        )

    elif category == "certification":
        return (
            f"Do you currently hold the {r}?",
            "yes_no"
        )

    elif category == "license":
        return (
            f"Do you currently possess the required {r}?",
            "yes_no"
        )

    elif category == "exam":
        return (
            f"Have you appeared for and cleared the {r}?",
            "yes_no"
        )

    elif category == "experience":
        # Make experience questions specific
        r_lower = r.lower()
        if "data" in r_lower or "analysis" in r_lower or "science" in r_lower:
            return (
                f"How many years of hands-on {r} experience do you have?",
                "number"
            )
        elif "programming" in r_lower or "coding" in r_lower or "development" in r_lower:
            return (
                f"How many years of practical {r} experience do you have?",
                "number"
            )
        else:
            return (
                f"How many years of relevant {r} experience do you have?",
                "number"
            )

    else:
        # Generic but still specific
        return (
            f"Do you currently satisfy the {r} requirement?",
            "yes_no"
        )


# ============================================================
# REQUIREMENT SELECTION
# ============================================================

def select_requirements(requirements, target_count: int = 6):
    """
    Pick the most important requirements with category diversity.
    Priority: essential > important > optional
    Never picks the same requirement twice.
    """
    importance_order = {"essential": 0, "important": 1, "optional": 2}

    sorted_reqs = sorted(
        requirements,
        key=lambda r: importance_order.get(r.importance.strip().lower(), 3)
    )

    # First pass — strict per-category limits for variety
    MAX_PER_CATEGORY = {
        "skill":         5,
        "technology":    4,
        "education":     2,
        "experience":    2,
        "certification": 2,
        "license":       2,
        "exam":          2,
        "other":         1,
    }

    selected = []
    used_reqs = set()
    category_count = {}

    for req in sorted_reqs:
        if len(selected) >= target_count:
            break
        norm = req.requirement.strip().lower()
        if norm in used_reqs:
            continue
        cat = req.category.strip().lower()
        if category_count.get(cat, 0) >= MAX_PER_CATEGORY.get(cat, 2):
            continue
        selected.append(req)
        used_reqs.add(norm)
        category_count[cat] = category_count.get(cat, 0) + 1

    # Second pass — relax limits if still short, still no repeats
    if len(selected) < target_count:
        for req in sorted_reqs:
            if len(selected) >= target_count:
                break
            norm = req.requirement.strip().lower()
            if norm in used_reqs:
                continue
            selected.append(req)
            used_reqs.add(norm)

    return selected[:target_count]


# ============================================================
# MAIN QUESTION GENERATOR — NO LLM
# ============================================================

def generate_career_questions(career: str, research_report) -> CareerQuestions:
    """
    Generates career-specific technical questions using Python templates.
    No LLM is used — questions are deterministic, correct, and always technical.
    """

    requirements = research_report.requirements

    if not requirements:
        return CareerQuestions(questions=[])

    TARGET = 8

    print("🚀 Selecting requirements for assessment...")

    selected = select_requirements(requirements, target_count=TARGET)

    print(f"📌 Selected {len(selected)} requirements.")
    print("🔧 Building technical questions...")

    questions = []
    for req in selected:
        req_text = req.requirement.strip()
        category = req.category.strip().lower()

        question_text, question_type = build_question(req_text, category)

        questions.append(
            CareerQuestion(
                question=question_text,
                requirement=req_text,
                category=category,
                question_type=question_type,
            )
        )

    print(f"✅ Generated {len(questions)} focused technical questions.")

    return CareerQuestions(questions=questions)