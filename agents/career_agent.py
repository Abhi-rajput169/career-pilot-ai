from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field


# Structure of the information we want from the user
class CareerGoal(BaseModel):
    career: str = Field(description="The career the user wants to prepare for")
    timeline: str | None = Field(
        default=None,
        description="The preparation timeline mentioned by the user"
    )
    country: str | None = Field(
        default=None,
        description="Country mentioned by the user"
    )


# Connect to our local Ollama model
llm = ChatOllama(
    model="qwen2.5:1.5b",
    temperature=0
)


def understand_career_goal(user_input: str):

    prompt = f"""
You extract structured information from user career goals.

Extract information EXACTLY from the user input.

USER INPUT:
"{user_input}"

Return these fields:

career:
- The specific career the user wants to become.

timeline:
- Extract the exact preparation duration if mentioned.
- Examples: "6 months", "90 days", "1 year".
- If no duration is mentioned, use null.

country:
- Extract the country name if mentioned.
- Examples: India, USA, Canada.
- If no country is mentioned, use null.

IMPORTANT:
Do not ignore timeline or country when they appear in the input.
"""


    structured_llm = llm.with_structured_output(CareerGoal)

    result = structured_llm.invoke(prompt)

    return result