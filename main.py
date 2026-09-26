from agents.career_agent import understand_career_goal
from agents.research_agent import research_career
from agents.question_agent import generate_career_questions
from agents.user_profile import create_user_profile
from agents.skill_gap_agent import analyze_skill_gaps
from agents.resource_agent import find_resources_for_gap
from agents.roadmap_agent import generate_roadmap

user_input = input("What career do you want to prepare for? ")

# Step 1: Understand the user's goal
career_goal = understand_career_goal(user_input)

print("\n🎯 Career Goal:")
print(f"   Career  : {career_goal.career}")
print(f"   Country : {career_goal.country or 'Not specified'}")
print(f"   Timeline: {career_goal.timeline or 'Not specified'}")


# Step 2: Research the career
research_report, sources = research_career(
    career_goal.career,
    career_goal.country
)


# Step 3: Display research results
print("\n" + "=" * 60)
print("🔬 CAREER OVERVIEW")
print("=" * 60)
print(f"\n{research_report.career_overview}")

# Display career information (salary, outlook, etc.) — NOT requirements
info = research_report.career_information
print("\n" + "=" * 60)
print("📊 CAREER INFORMATION")
print("=" * 60)

if info.salary_range:
    print(f"\n💰 Salary Range     : {info.salary_range}")
if info.job_outlook:
    print(f"📈 Job Outlook      : {info.job_outlook}")
if info.typical_responsibilities:
    print(f"🗂️  Responsibilities : {info.typical_responsibilities}")
if info.work_environment:
    print(f"🏢 Work Environment : {info.work_environment}")

# Display the genuine requirements
print("\n" + "=" * 60)
print("✅ CAREER REQUIREMENTS")
print("=" * 60)

for i, req in enumerate(research_report.requirements, 1):
    print(f"\n{i}. {req.requirement}")
    print(f"   Category  : {req.category}")
    print(f"   Importance: {req.importance}")
    print(f"   Why       : {req.explanation}")


# Step 4: Generate questions from requirements only
print("\n❓ Generating career-specific questions...\n")

questions = generate_career_questions(
    career_goal.career,
    research_report
)

print("📝 QUESTIONS FOR YOU\n")

for i, question in enumerate(questions.questions, 1):
    print(f"{i}. {question.question}")
    print(f"   Category   : {question.category}")
    print(f"   Requirement: {question.requirement}")
    print(f"   Answer Type: {question.question_type}")
    print()


# Step 5: Collect user answers
print("\n👤 Collecting your answers...")

user_profile = create_user_profile(
    career_goal,
    questions
)

print("\n" + "=" * 60)
print("👤 USER PROFILE")
print("=" * 60)

print(f"\nCareer  : {user_profile.career}")
print(f"Timeline: {user_profile.timeline or 'Not specified'}")
print(f"Country : {user_profile.country or 'Not specified'}")

print("\nYour Answers:")

for answer in user_profile.answers:
    print(f"\n  Requirement : {answer.requirement}")
    print(f"  Question    : {answer.question}")
    print(f"  Type        : {answer.question_type}")
    print(f"  Answer      : {answer.answer}")


# Step 6: Analyze skill gaps
print("\n🧠 Analyzing your skill gaps...")

gap_report = analyze_skill_gaps(
    research_report,
    user_profile
)

print("\n" + "=" * 60)
print("📊 SKILL GAP REPORT")
print("=" * 60)

for gap in gap_report.gaps:
    print(f"\nRequirement: {gap.requirement}")
    print(f"  Category  : {gap.category}")
    print(f"  Importance: {gap.importance}")
    print(f"  Your Level: {gap.user_status}")
    print(f"  Gap       : {gap.gap_level}")
    print(f"  Note      : {gap.explanation}")


# Step 7: Find resources for actual gaps
print("\n" + "=" * 60)
print("📚 PERSONALIZED LEARNING RESOURCES")
print("=" * 60)

resource_reports = []

for gap in gap_report.gaps:

    if gap.gap_level == "None":
        continue

    resource_report = find_resources_for_gap(
        requirement=gap.requirement,
        category=gap.category,
        importance=gap.importance,
        user_status=gap.user_status
    )

    resource_reports.append({
        "requirement": gap.requirement,
        "gap_level": gap.gap_level,
        "resources": resource_report.resources
    })

    print(f"\n🎯 {gap.requirement}")
    print(f"   Gap: {gap.gap_level}")

    if not resource_report.resources:
        print("   ⚠️ No YouTube videos found for this requirement.")
    else:
        for resource in resource_report.resources:
            print(f"\n   📺 {resource.title}")
            print(f"      🔗 {resource.url}")



# Step 8: Generate personalized roadmap
print("\n" + "=" * 60)
print("🗺️  PERSONALIZED PREPARATION ROADMAP")
print("=" * 60)

roadmap = generate_roadmap(
    career_goal=career_goal,
    gap_report=gap_report,
    resource_reports=resource_reports
)

print(f"\n{roadmap}")

print("\n" + "=" * 60)
print("✅ CareerPilot AI — Analysis Complete!")
print("=" * 60)