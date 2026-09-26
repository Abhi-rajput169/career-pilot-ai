from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field


# ==========================================
# OUTPUT MODELS
# ==========================================

class RequirementMatch(BaseModel):
    requirement: str = Field(
        description="The exact career requirement being evaluated"
    )

    category: str = Field(
        description="The requirement category"
    )

    importance: str = Field(
        description="Importance: essential, important, or optional"
    )

    matched_question: str = Field(
        description="The exact user question that provides evidence for this requirement. Empty string if no matching question exists."
    )

    user_status: str = Field(
        description="The user's status based ONLY on the matched answer"
    )


class RequirementMatches(BaseModel):
    matches: list[RequirementMatch]


class SkillGap(BaseModel):
    requirement: str
    category: str
    importance: str
    user_status: str
    gap_level: str
    explanation: str


class SkillGapReport(BaseModel):
    gaps: list[SkillGap]


# ==========================================
# LLM
# ==========================================

llm = ChatOllama(
    model="qwen2.5:1.5b",
    temperature=0
)


# ==========================================
# STEP 1: MATCH REQUIREMENTS WITH ANSWERS
# ==========================================

def match_requirements_to_answers(career_research, user_profile):

    requirements_text = "\n".join(
        f"{i + 1}. {req.requirement}\n"
        f"   Category: {req.category}\n"
        f"   Importance: {req.importance}"
        for i, req in enumerate(career_research.requirements)
    )

    # Build answers text — include the requirement field when available
    answers_lines = []
    for i, answer in enumerate(user_profile.answers):
        line = (
            f"QUESTION {i + 1}:\n"
            f"{answer.question}\n"
            f"Covers requirement: {answer.requirement}\n"
            f"Category: {answer.category}\n"
            f"Answer: {answer.answer}\n"
        )
        answers_lines.append(line)
    answers_text = "\n".join(answers_lines)

    prompt = f"""
You are a requirement matching assistant.

CAREER:
{user_profile.career}

CAREER REQUIREMENTS:
{requirements_text}

USER QUESTIONS AND ANSWERS:
{answers_text}

Your task is ONLY to match each career requirement
with the user question that provides evidence about it.

IMPORTANT RULES:

1. Use ONLY the information provided.

2. NEVER invent a user answer.

3. NEVER assume the user has a skill or qualification.

4. Use the "Covers requirement" field as the PRIMARY
   matching signal. If a question says it covers a
   requirement, prefer that match.

5. If no question provides information about a requirement,
   matched_question MUST be an empty string.

6. Do NOT use an answer from one requirement for another
   unrelated requirement.

7. For example:

Question:
"How would you rate your Python skills?"
Answer:
"Intermediate"

This answer can be used for:
Python programming

But it CANNOT be used for:
Machine learning
Deep learning
NLP
PyTorch
etc.

8. Match requirements based on the actual meaning of
   the question, not just the category.

9. Keep the requirement name EXACTLY as provided.

10. Return one match for each researched requirement.

11. Do not calculate gap levels.
    Only identify the user's status from the answer.

For unmatched requirements:
matched_question = ""
user_status = "Unknown"
"""

    structured_llm = llm.with_structured_output(RequirementMatches)

    result = structured_llm.invoke(prompt)

    return result


# ==========================================
# STEP 2: FIND ACTUAL ANSWER
# ==========================================

def find_answer_for_requirement(requirement, user_profile):
    """Find answer by matching the requirement field directly."""

    normalized_req = requirement.strip().lower()

    # First try: match by requirement field (most reliable)
    for answer in user_profile.answers:
        if answer.requirement.strip().lower() == normalized_req:
            return answer

    # Fallback: fuzzy match on requirement field
    for answer in user_profile.answers:
        ans_req = answer.requirement.strip().lower()
        if ans_req and (ans_req in normalized_req or normalized_req in ans_req):
            return answer

    return None


def find_answer_for_question(question, user_profile):
    """Find answer by matching the question text."""

    if not question:
        return None

    normalized_question = question.strip().lower()

    for answer in user_profile.answers:
        if answer.question.strip().lower() == normalized_question:
            return answer

    return None


# ==========================================
# STEP 3A: NORMALIZE ANSWER TEXT
# ==========================================

def normalize_answer(user_status: str, category: str) -> str:
    """
    Convert natural language answers to standardized tokens.
    Handles text answers like 'i am not comfortable', 'yes', '0 years', etc.
    """
    s = user_status.strip().lower()

    # Already standard tokens — pass through
    if s in ["beginner", "intermediate", "advanced", "yes", "no",
             "none", "completed", "not completed", "have it", "unknown"]:
        return s

    # Numeric years (experience category)
    if category == "experience":
        # e.g. "0 years", "2 years"
        try:
            years = float(s.replace("years", "").replace("year", "").strip())
            return f"{int(years)} years"
        except (ValueError, AttributeError):
            pass

    # Level words
    if "beginner" in s or "just started" in s or "new to" in s:
        return "beginner"
    if "intermediate" in s or "some experience" in s:
        return "intermediate"
    if "advanced" in s or "expert" in s or "proficient" in s or "strong" in s:
        return "advanced"

    # Negative phrases → "no"
    negative_phrases = [
        "not comfortable", "not familiar", "not confident",
        "don't have", "do not have", "haven't", "have not",
        "i don't", "i do not", "no experience",
        "uncomfortable", "not yet", "i am not",
        "cannot", "can't", "no,", "nope",
    ]
    if any(phrase in s for phrase in negative_phrases):
        return "no"

    # Positive phrases → "yes"
    positive_phrases = [
        "comfortable", "confident", "familiar with",
        "have it", "i have", "i do", "yes,", "yeah",
    ]
    if any(phrase in s for phrase in positive_phrases):
        return "yes"

    # Simple yes/no at start
    if s.startswith("yes"):
        return "yes"
    if s.startswith("no"):
        return "no"

    # Return original cleaned string
    return s


# ==========================================
# STEP 3B: CALCULATE GAP
# ==========================================

def calculate_gap(
    category,
    importance,
    user_status,
    answer
):

    # No information available
    if answer is None:
        return "Unknown"

    # Normalize the raw answer text before processing
    user_status = normalize_answer(user_status, category)

    if user_status == "unknown":
        return "Unknown"

    status = user_status.strip().lower()
    importance = importance.strip().lower()
    category = category.strip().lower()

    # --------------------------------------
    # EDUCATION / CERTIFICATION / LICENSE / EXAM
    # --------------------------------------

    if category in [
        "education",
        "certification",
        "license",
        "exam"
    ]:

        if status in ["no", "not completed", "none"]:
            if importance == "essential":
                return "Critical"
            if importance == "important":
                return "High"
            # optional + No → Low
            return "Low"

        if status in ["yes", "completed", "have it"]:
            return "None"

        return "Unknown"

    # --------------------------------------
    # SKILL / TECHNOLOGY
    # --------------------------------------

    if category in ["skill", "technology"]:

        if status == "beginner":

            if importance == "essential":
                return "High"

            if importance == "important":
                return "Medium"

            return "Low"

        if status == "intermediate":

            if importance == "essential":
                return "Medium"

            if importance == "important":
                return "Low"

            return "Low"

        if status == "advanced":
            return "None"

        if status in ["no", "none"]:
            if importance == "essential":
                return "High"
            return "Medium"

        return "Unknown"

    # --------------------------------------
    # EXPERIENCE
    # --------------------------------------

    if category == "experience":

        # Try to parse numeric years from the status
        # e.g. "2 years" → 2, "0 years" → 0
        try:
            years_str = status.replace("years", "").replace("year", "").strip()
            years = float(years_str)

            if years == 0:
                if importance == "essential":
                    return "High"
                if importance == "important":
                    return "Medium"
                return "Low"

            if years < 1:
                if importance == "essential":
                    return "Medium"
                return "Low"

            if years < 2:
                if importance == "essential":
                    return "Medium"
                return "Low"

            if years < 5:
                return "Low"  # Has decent experience, small gap

            return "None"  # 5+ years, no meaningful gap

        except (ValueError, AttributeError):
            # Cannot parse numeric years
            # Fall through to handle text-based status like "yes"/"no"
            if status in ["no", "none"]:
                return "High" if importance == "essential" else "Medium"
            if status in ["yes", "have it", "completed"]:
                return "Low"
            return "Unknown"

    # --------------------------------------
    # OTHER
    # --------------------------------------

    if status in ["no", "none"]:

        if importance == "essential":
            return "Critical"

        if importance == "important":
            return "High"

        return "Low"

    if status in ["yes", "completed"]:
        return "None"

    return "Unknown"


# ==========================================
# STEP 4: GENERATE EXPLANATION
# ==========================================

def generate_explanation(
    requirement,
    category,
    importance,
    user_status,
    gap_level
):

    prompt = f"""
Write ONE short practical explanation for this career
skill gap. Be concise — 1 or 2 sentences maximum.

Requirement:
{requirement}

Category:
{category}

Importance:
{importance}

User status:
{user_status}

Gap:
{gap_level}

Rules:

- Talk ONLY about this specific requirement.
- Do not mention other requirements.
- Do not invent facts.
- Do not mention certifications unless this requirement
  itself is about certification.
- Do not mention education unless this requirement
  itself is about education.
- Do not invent required years of experience.
- Be clear and practical.
- If gap is None or Unknown, explain that briefly.
- Keep it to 1 or 2 sentences.
"""

    response = llm.invoke(prompt)

    return response.content.strip()


# ==========================================
# MAIN SKILL GAP FUNCTION
# ==========================================

def analyze_skill_gaps(career_research, user_profile):

    print("🔍 Matching requirements with your answers...")

    matches = match_requirements_to_answers(
        career_research,
        user_profile
    )

    print("🧮 Calculating skill gaps...")

    gaps = []

    # Create lookup of actual user answers by question text
    answer_lookup = {
        answer.question.strip().lower(): answer
        for answer in user_profile.answers
    }

    for match in matches.matches:

        answer = None

        # Try direct requirement match first (most reliable)
        answer = find_answer_for_requirement(
            match.requirement,
            user_profile
        )

        # Fall back to question text match
        if answer is None and match.matched_question:
            answer = find_answer_for_question(
                match.matched_question,
                user_profile
            )

        # Fall back to answer_lookup
        if answer is None and match.matched_question:
            answer = answer_lookup.get(
                match.matched_question.strip().lower()
            )

        # Safety check
        if answer is None:
            user_status = "Unknown"
        else:
            user_status = answer.answer

        gap_level = calculate_gap(
            category=match.category,
            importance=match.importance,
            user_status=user_status,
            answer=answer
        )

        explanation = generate_explanation(
            requirement=match.requirement,
            category=match.category,
            importance=match.importance,
            user_status=user_status,
            gap_level=gap_level
        )

        gaps.append(
            SkillGap(
                requirement=match.requirement,
                category=match.category,
                importance=match.importance,
                user_status=user_status,
                gap_level=gap_level,
                explanation=explanation
            )
        )

    print("✅ Skill-gap analysis complete!")

    return SkillGapReport(gaps=gaps)