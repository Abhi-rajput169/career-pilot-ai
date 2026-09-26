from ddgs import DDGS
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
import re


# ==========================================
# CAREER REQUIREMENT
# ==========================================

class CareerRequirement(BaseModel):

    requirement: str = Field(
        description="A single specific requirement. Short name only. No explanations, no lists, no 'such as' clauses."
    )

    category: str = Field(
        description=(
            "One of: skill, technology, education, "
            "experience, certification, license, exam, other"
        )
    )

    importance: str = Field(
        description="One of: essential, important, optional"
    )

    explanation: str = Field(
        description="Short explanation of why this requirement matters"
    )


# ==========================================
# CAREER INFORMATION (not requirements)
# ==========================================

class CareerInformation(BaseModel):

    salary_range: str = Field(
        default="",
        description="Typical salary range for this career in the specified country"
    )

    job_outlook: str = Field(
        default="",
        description="Job market outlook, demand, and growth trends"
    )

    typical_responsibilities: str = Field(
        default="",
        description="Common day-to-day tasks and responsibilities"
    )

    work_environment: str = Field(
        default="",
        description="Typical work setting, hours, and conditions"
    )


# ==========================================
# CAREER RESEARCH
# ==========================================

class CareerResearch(BaseModel):

    career_overview: str = Field(
        description="Short accurate overview of the career"
    )

    requirements: list[CareerRequirement] = Field(
        description="Specific genuine requirements supported by research"
    )

    career_information: CareerInformation = Field(
        default_factory=CareerInformation,
        description="General career information that is NOT a requirement"
    )


# ==========================================
# LLM
# ==========================================

llm = ChatOllama(
    model="qwen2.5:1.5b",
    temperature=0
)


# ==========================================
# WEB SEARCH
# ==========================================

def search_career_info(
    career: str,
    country: str | None = None
):

    location = f"in {country}" if country else ""

    queries = [
        f"How to become a {career} {location}",
        f"{career} job requirements skills qualifications {location}",
        f"{career} required skills experience education {location}",
        f"{career} license certification mandatory {location}",
        f"{career} degree education requirement {location}",
    ]

    all_results = []

    for query in queries:
        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=4)
                for result in results:
                    all_results.append({
                        "title": result.get("title", ""),
                        "href": result.get("href", ""),
                        "body": result.get("body", "")
                    })
        except Exception as e:
            print(f"⚠️ Search failed for query '{query}': {e}. Continuing...")
            continue

    return all_results


# ==========================================
# AI RESEARCH ANALYSIS
# ==========================================

def analyze_career_research(
    career: str,
    country: str | None,
    search_results: list
):

    relevant_results = search_results[:12]

    research_text = ""
    for i, result in enumerate(relevant_results, 1):
        research_text += f"""
SOURCE {i}
TITLE: {result['title']}
URL: {result['href']}
INFORMATION: {result['body']}
--------------------------------
"""

    prompt = f"""
You are a career research analyst.

Career: {career}
Country: {country if country else "Not specified"}

Read the web research below carefully.

WEB RESEARCH:
{research_text}

==================================================
YOUR TASK
==================================================

Extract two things:

1. REQUIREMENTS: What a person genuinely needs
   to enter or practice the career: {career}

2. CAREER INFORMATION: Background facts
   (salary, job outlook, responsibilities, work environment)

==================================================
CRITICAL REQUIREMENT RULES
==================================================

RULE 1 — STAY ON TOPIC
You are analyzing ONLY: {career}
Do NOT add requirements for other careers.

RULE 2 — ONE ITEM PER REQUIREMENT
Each requirement must be ONE specific item.

GOOD examples:
- Python programming
- SQL
- Machine learning
- Bachelor's degree in Computer Science
- Data visualization
- Work experience in data analysis

BAD examples (these are compounds / blobs — NEVER do this):
- Skills: Strong analytical skills, proficiency in Python, R, SQL...
- Education: A bachelor's degree... A master's degree...
- Strong analytical skills and proficiency in programming languages
- Knowledge of Python, SQL, machine learning, and statistics

If multiple skills are needed, create a SEPARATE requirement
for each one. Do not list them together.

RULE 3 — KEEP IT SHORT
The requirement field must be 1 to 6 words maximum.
No sentences. No explanations. No colons.

GOOD: "Python programming"
GOOD: "SQL"
GOOD: "Machine learning"
GOOD: "Bachelor's degree"
BAD: "Skills: Strong analytical skills, proficiency in Python..."
BAD: "Education: A bachelor's degree in a relevant field..."

RULE 4 — WHAT COUNTS AS A REQUIREMENT

- skill: A practical ability (Python, Communication, Statistics)
- technology: A specific tool or platform (SQL, PyTorch, Tableau)
- education: A degree or qualification (Bachelor's degree)
- experience: Hands-on experience (Data analysis experience)
- certification: A named certification
- license: A government/professional license
- exam: A required entrance exam
- other: Medical fitness, background check

RULE 5 — WHAT IS NOT A REQUIREMENT

Do NOT create requirements from:
- Learning platforms: Coursera, Udemy, YouTube, bootcamps
- Vague traits: passion, motivation, staying updated
- Career information: salary, job growth, career outlook
- Compound lists of skills (see Rule 2)

RULE 6 — SELF-CHECK
After creating each requirement, ask yourself:
"Is this actually required to be a {career}?"
If the answer is "no" or "maybe", remove it.

RULE 7 — QUANTITY
Aim for 5 to 8 specific requirements.
Quality over quantity.

RULE 8 — IMPORTANCE
- essential: Normally required to enter the career
- important: Commonly expected
- optional: Helpful but not normally required

==================================================
CAREER INFORMATION (separate section)
==================================================

Extract these as career_information (NOT requirements):
- salary_range: typical pay in {country if country else "the country"}
- job_outlook: demand, growth, market
- typical_responsibilities: day-to-day tasks
- work_environment: work setting, hours

Return your analysis now.
"""

    structured_llm = llm.with_structured_output(CareerResearch)
    result = structured_llm.invoke(prompt)
    return result


# ==========================================
# PYTHON VALIDATION / CLEANING
# ==========================================

BLOCKED_TERMS = [
    "coursera", "udemy", "youtube", "edx",
    "online platform", "online platforms",
    "online course", "online courses",
    "structured learning", "structured education",
    "iit program", "iit programs",
    "iim program", "iim programs",
    "bootcamp", "bootcamps",
    "learning resources", "study materials",
    "tutorials", "books",
    "continuous learning", "staying updated",
    "industry connections", "passion", "motivation",
    "good attitude", "hard work", "interest in the field",
    "job growth", "salary", "career outlook", "career growth",
]

CAREER_SPECIFIC_TERMS = [
    ("aircraft handling", ["pilot", "aviation"]),
    ("supervised flight hours", ["pilot", "aviation", "flight"]),
    ("clinical hours", ["doctor", "physician", "nurse", "nursing", "medical"]),
    ("dgca", ["pilot", "aviation", "flight"]),
    ("dgca pilot license", ["pilot", "aviation"]),
    ("bar council", ["lawyer", "advocate", "legal", "law"]),
    ("bar exam", ["lawyer", "advocate", "legal", "law"]),
    ("llb", ["lawyer", "advocate", "legal", "law", "attorney"]),
    ("neet", ["doctor", "physician", "nurse", "medical", "mbbs"]),
    ("medical council registration", ["doctor", "physician", "nurse", "medical"]),
    ("medical fitness requirement", ["pilot", "doctor", "aviation", "military"]),
    ("upsc", ["civil service", "ias", "ips", "government officer"]),
    ("flight hours", ["pilot", "aviation", "flight"]),
    ("faa", ["pilot", "aviation", "flight"]),
    ("cpl", ["pilot", "aviation", "flight"]),
    ("atpl", ["pilot", "aviation", "flight"]),
]

# Category prefix patterns the LLM sometimes prepends
CATEGORY_PREFIX_PATTERN = re.compile(
    r'^(skills?|education|experience|certification|license|'
    r'exam|technology|other|requirement)\s*:\s*',
    re.IGNORECASE
)

# Compound requirement detection — these phrases indicate the LLM bundled multiple items
COMPOUND_INDICATORS = [
    " such as ", " including ", " such as,", " and experience with",
    " and knowledge of", ", and ", " proficiency in ", " as well as ",
]


def strip_category_prefix(text: str) -> str:
    """Remove leading 'Skills:', 'Education:' etc. from requirement text."""
    return CATEGORY_PREFIX_PATTERN.sub("", text).strip()


def is_compound_requirement(text: str) -> bool:
    """Return True if the requirement looks like a bundled list of multiple items."""
    # Long requirements with commas are almost always compounds
    if len(text) > 80 and "," in text:
        return True
    # Contains telltale compound phrases
    text_lower = text.lower()
    if any(indicator in text_lower for indicator in COMPOUND_INDICATORS):
        return True
    return False


def is_career_specific_contamination(requirement_text: str, career: str) -> bool:
    req_lower = requirement_text.lower()
    career_lower = career.lower()
    for term, valid_careers in CAREER_SPECIFIC_TERMS:
        if term in req_lower:
            career_matches = any(valid in career_lower for valid in valid_careers)
            if not career_matches:
                return True
    return False


NOT_REQUIRED_PHRASES = [
    "not a requirement",
    "not required",
    "is not required",
    "is not mandatory",
    "not mandatory",
    "can be beneficial",
    "beneficial for those interested in",
    "may be preferred",
    "often preferred",
]


def clean_requirements(requirements, career: str = ""):

    clean = []
    seen = set()

    for req in requirements:

        requirement_text = req.requirement.strip()

        # Strip category prefixes the LLM sometimes adds
        requirement_text = strip_category_prefix(requirement_text)
        # Truncate at first sentence boundary or semicolon
        requirement_text = re.split(r'[.;]', requirement_text)[0].strip()

        if not requirement_text:
            continue

        normalized = requirement_text.lower()

        # Block compound / bundled requirements
        if is_compound_requirement(requirement_text):
            print(f"⚠️ Removed compound requirement: {requirement_text[:60]}...")
            continue

        # Block requirements containing noise terms
        if any(term in normalized for term in BLOCKED_TERMS):
            print(f"⚠️ Removed blocked term requirement: {requirement_text}")
            continue

        # Block cross-career contamination
        if career and is_career_specific_contamination(requirement_text, career):
            print(f"⚠️ Removed cross-career requirement: {requirement_text}")
            continue

        # Block self-negating requirements
        explanation_lower = req.explanation.lower()
        if any(phrase in explanation_lower for phrase in NOT_REQUIRED_PHRASES):
            print(f"⚠️ Removed self-negating requirement: {requirement_text}")
            continue

        # Remove duplicates
        if normalized in seen:
            continue
        seen.add(normalized)

        # Validate category
        valid_categories = [
            "skill", "technology", "education", "experience",
            "certification", "license", "exam", "other"
        ]
        category = req.category.strip().lower()
        if category not in valid_categories:
            category = "other"

        # Validate importance
        valid_importance = ["essential", "important", "optional"]
        importance = req.importance.strip().lower()
        if importance not in valid_importance:
            importance = "important"

        clean.append(
            CareerRequirement(
                requirement=requirement_text,
                category=category,
                importance=importance,
                explanation=req.explanation.strip()
            )
        )

    return clean


# ==========================================
# CORE REQUIREMENT GUARANTEES
# ==========================================

# These requirements MUST appear for each career.
# If the model misses them (due to compounding or hallucination),
# they are injected automatically.
CAREER_CORE_REQUIREMENTS = {
    "data scientist": [
        {"requirement": "Python programming", "category": "skill", "importance": "essential",
         "explanation": "Python is the primary language for data science workflows."},
        {"requirement": "SQL", "category": "technology", "importance": "essential",
         "explanation": "SQL is essential for querying and managing data."},
        {"requirement": "Machine learning", "category": "skill", "importance": "essential",
         "explanation": "Core skill for building predictive models."},
        {"requirement": "Statistics", "category": "skill", "importance": "essential",
         "explanation": "Statistical knowledge underpins all data science work."},
        {"requirement": "Data visualization", "category": "skill", "importance": "important",
         "explanation": "Communicating insights through charts and dashboards."},
    ],
    "machine learning engineer": [
        {"requirement": "Python programming", "category": "skill", "importance": "essential",
         "explanation": "Python is the standard language for ML engineering."},
        {"requirement": "Machine learning", "category": "skill", "importance": "essential",
         "explanation": "Core skill for designing and training models."},
        {"requirement": "Deep learning", "category": "skill", "importance": "important",
         "explanation": "Neural network knowledge for advanced models."},
        {"requirement": "SQL", "category": "technology", "importance": "important",
         "explanation": "Required for data querying and pipeline work."},
    ],
    "software engineer": [
        {"requirement": "Programming language proficiency", "category": "skill", "importance": "essential",
         "explanation": "Fluency in at least one language is mandatory."},
        {"requirement": "Data structures and algorithms", "category": "skill", "importance": "essential",
         "explanation": "Fundamental to software engineering interviews and work."},
        {"requirement": "Version control (Git)", "category": "technology", "importance": "essential",
         "explanation": "Standard tool for collaborative software development."},
    ],
    "web developer": [
        {"requirement": "HTML and CSS", "category": "skill", "importance": "essential",
         "explanation": "Foundational skills for any web development role."},
        {"requirement": "JavaScript", "category": "technology", "importance": "essential",
         "explanation": "Core language for interactive web development."},
    ],
}


def inject_core_requirements(requirements, career):
    """
    Ensure that known core requirements are always present
    for well-known careers. Only injects items that are missing.
    """
    career_lower = career.strip().lower()

    # Find the best matching career key
    matched_core = None
    for key in CAREER_CORE_REQUIREMENTS:
        if key in career_lower or career_lower in key:
            matched_core = CAREER_CORE_REQUIREMENTS[key]
            break

    if not matched_core:
        return requirements  # Unknown career — nothing to inject

    # Build set of already-present requirement names (lowercase)
    existing = {r.requirement.strip().lower() for r in requirements}

    injected = list(requirements)
    for item in matched_core:
        req_lower = item["requirement"].lower()
        # Skip if already present (exact or substring match)
        if any(req_lower in ex or ex in req_lower for ex in existing):
            continue
        print(f"💉 Injecting guaranteed requirement: {item['requirement']}")
        injected.append(
            CareerRequirement(
                requirement=item["requirement"],
                category=item["category"],
                importance=item["importance"],
                explanation=item["explanation"],
            )
        )
        existing.add(req_lower)

    return injected


# ==========================================
# MAIN RESEARCH FUNCTION
# ==========================================

def research_career(career: str, country: str | None = None):

    print("\n🔎 Searching the web...")

    search_results = search_career_info(career, country)

    print(f"🌐 Found {len(search_results)} search results.")

    if not search_results:
        print("⚠️ No search results found. Proceeding with LLM knowledge only.")

    print("🧠 Analyzing career requirements...")

    research_report = analyze_career_research(career, country, search_results)

    print("🧹 Validating requirements...")

    cleaned_requirements = clean_requirements(
        research_report.requirements,
        career=career
    )

    # Guarantee core requirements are present for known careers
    cleaned_requirements = inject_core_requirements(cleaned_requirements, career)

    research_report = CareerResearch(
        career_overview=research_report.career_overview,
        requirements=cleaned_requirements,
        career_information=research_report.career_information
    )

    print(f"✅ Kept {len(cleaned_requirements)} valid requirements.")

    return research_report, search_results