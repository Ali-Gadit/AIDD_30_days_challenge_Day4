import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner,set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
set_tracing_disabled(True)
load_dotenv()

# Configure the model using LiteLLM to support Gemini
# Ensure GEMINI_API_KEY is set in your .env file
def get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    # Using gemini-1.5-flash for speed and efficiency
    return LitellmModel(
        model="gemini/gemini-2.5-flash",
        api_key=api_key
    )

async def summarize_text(text: str) -> str:
    """
    Summarizes the provided text using the Agent.
    """
    agent = Agent(
        name="Summarizer",
        model=get_model(),
        instructions="You are an expert study assistant. Summarize the provided study notes clearly and concisely. Highlight key concepts and definitions."
    )
    
    # Run the agent
    # We limit the text length if necessary to avoid token limits, though Gemini 1.5 has a large context window.
    result = await Runner.run(agent, f"Please summarize the following text:\n\n{text}")
    return result.final_output

async def generate_quiz(text: str, num_questions: int = 5) -> str:
    """
    Generates a quiz based on the original text.
    """
    agent = Agent(
        name="QuizGenerator",
        model=get_model(),
        instructions=f"You are a teacher creating a quiz. Create {num_questions} multiple-choice questions (MCQs) based on the text provided. For each question, provide 4 distinct options, each starting on a new line and labeled 'a)', 'b)', 'c)', 'd)'. Ensure there is a blank line between each option. At the very end of the quiz, list all the correct answers (e.g., '1: c, 2: a, ...'). Do NOT reveal the answer immediately after each question."
    )
    
    result = await Runner.run(agent, f"Generate a {num_questions}-question MCQ quiz from this text:\n\n{text}")
    return result.final_output
