from pydantic import BaseModel, Field


class UserAnswer(BaseModel):
    question: str
    requirement: str
    category: str
    question_type: str
    answer: str


class UserProfile(BaseModel):
    career: str
    timeline: str | None = None
    country: str | None = None
    answers: list[UserAnswer] = Field(default_factory=list)


def collect_user_answers(questions):
    answers = []

    print("\n" + "=" * 60)
    print("👤 LET'S UNDERSTAND YOUR CURRENT LEVEL")
    print("=" * 60)

    for i, question in enumerate(questions.questions, 1):

        print(f"\n{i}. {question.question}")
        print(f"   Category: {question.category}")

        question_type = question.question_type.lower().strip()

        # LEVEL QUESTION
        if question_type == "level":

            print("   Choose your level:")
            print("   1. Beginner")
            print("   2. Intermediate")
            print("   3. Advanced")

            while True:
                choice = input("   Your choice (1/2/3): ").strip()

                levels = {
                    "1": "Beginner",
                    "2": "Intermediate",
                    "3": "Advanced"
                }

                if choice in levels:
                    answer = levels[choice]
                    break

                print("   ❌ Please choose 1, 2, or 3.")

        # YES / NO QUESTION
        elif question_type == "yes_no":

            while True:
                answer = input("   Your answer (Yes/No): ").strip().lower()

                if answer in ["yes", "y"]:
                    answer = "Yes"
                    break

                elif answer in ["no", "n"]:
                    answer = "No"
                    break

                print("   ❌ Please enter Yes or No.")

        # NUMBER QUESTION — accepts actual numeric input
        elif question_type == "number":

            while True:
                try:
                    raw = input("   Your answer (number, e.g. 2): ").strip()
                except EOFError:
                    print("\nNo input received. Please run this app in a normal terminal.")
                    raise SystemExit(0)

                # Accept integer or decimal
                try:
                    value = float(raw)
                    if value < 0:
                        print("   ❌ Please enter a non-negative number.")
                        continue
                    # Store as "X years" for clarity
                    if value == int(value):
                        answer = f"{int(value)} years"
                    else:
                        answer = f"{value} years"
                    break
                except ValueError:
                    print("   ❌ Please enter a number (e.g. 0, 1, 2, 5).")

        # TEXT QUESTION
        else:

            answer = input("   Your answer: ").strip()

            while not answer:
                print("   ❌ Please provide an answer.")
                answer = input("   Your answer: ").strip()

        answers.append(
            UserAnswer(
                question=question.question,
                requirement=question.requirement,
                category=question.category,
                question_type=question_type,
                answer=answer
            )
        )

    return answers


def create_user_profile(career_goal, questions):

    answers = collect_user_answers(questions)

    profile = UserProfile(
        career=career_goal.career,
        timeline=career_goal.timeline,
        country=career_goal.country,
        answers=answers
    )

    return profile