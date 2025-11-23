import asyncio
import os
from dotenv import load_dotenv
from agents import Agent
from agents.extensions.models.litellm_model import LitellmModel

load_dotenv()

async def test_agent():
    try:
        print("Initializing Model...")
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Error: GEMINI_API_KEY not found.")
            return

        model = LitellmModel(
            model="gemini/gemini-1.5-flash",
            api_key=api_key
        )
        print("Model initialized.")
        
        print("Initializing Agent...")
        agent = Agent(
            name="TestAgent",
            model=model,
            instructions="Hello"
        )
        print("Agent initialized successfully.")
        
    except Exception as e:
        print(f"Caught exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_agent())
