from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="qwen2.5:1.5b",
    temperature=0.3  # Slightly creative for roadmap generation
)


def generate_roadmap(
    career_goal,
    gap_report,
    resource_reports: list[dict]
):
    """
    Generate a personalized preparation roadmap.

    Parameters:
    - career_goal: CareerGoal object (career, country, timeline)
    - gap_report: SkillGapReport object
    - resource_reports: list of dicts with keys:
        requirement, gap_level, resources (list of LearningResource)
    """

    career = career_goal.career
    country = career_goal.country or "Not specified"
    timeline = career_goal.timeline or "Not specified"

    # Build gap summary
    gap_lines = []
    for gap in gap_report.gaps:
        gap_lines.append(
            f"- {gap.requirement} | Level: {gap.user_status} | "
            f"Gap: {gap.gap_level} | Importance: {gap.importance}"
        )
    gap_summary = "\n".join(gap_lines) if gap_lines else "No gaps identified."

    # Build resources summary
    resource_lines = []
    for item in resource_reports:
        req = item.get("requirement", "")
        gap_level = item.get("gap_level", "")
        resources = item.get("resources", [])

        if resources:
            resource_lines.append(f"\n{req} ({gap_level} gap):")
            for r in resources[:3]:  # Top 3 per requirement
                resource_lines.append(f"  • {r.title} — {r.url}")

    resources_summary = (
        "\n".join(resource_lines)
        if resource_lines
        else "No resources found."
    )

    prompt = f"""
You are a career preparation coach.

Create a personalized, practical preparation roadmap
for a person with the following profile:

TARGET CAREER: {career}
COUNTRY: {country}
TIMELINE: {timeline}

SKILL GAPS (current level → gap):
{gap_summary}

RECOMMENDED RESOURCES:
{resources_summary}

==================================================
ROADMAP RULES
==================================================

1. Structure the roadmap into PHASES based on the timeline.
   Example for 6 months:
   - Phase 1 (Month 1-2): Foundation
   - Phase 2 (Month 3-4): Core Skills
   - Phase 3 (Month 5-6): Advanced & Projects

2. Address the CRITICAL and HIGH gaps FIRST.
   Then MEDIUM and LOW gaps. Skip only "None" gaps (no gap needed).

3. For each phase, list:
   - Focus areas
   - Specific actions to take
   - Resources to use (from the list above)
   - Milestone to achieve by end of phase

4. Be specific, practical, and actionable.
   Not vague motivational advice.

5. Tailor the roadmap to the country context.
   For India, mention relevant local context where useful.

6. If timeline is not specified, create a 3-phase plan.

7. End with a short NEXT STEPS section
   (the immediate 2-3 actions to start today).

8. Keep the roadmap concise and readable.
   Use clear headers and bullet points.

Generate the roadmap now:
"""

    print("🗺️ Generating your personalized roadmap...")

    response = llm.invoke(prompt)

    return response.content.strip()
