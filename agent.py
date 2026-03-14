import asyncio

from dotenv import load_dotenv
load_dotenv()
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

import os
print("KEY:", os.getenv("GOOGLE_API_KEY"))

APP_NAME = "research_app"
USER_ID = "farhan"
SESSION_ID = "session_001"


async def main():
    # session manager
    session_service = InMemorySessionService()

    # create agent
    root_agent = LlmAgent(
        name="research_agent",
        model="gemini-2.5-flash",
        instruction="You are a research assistant that explains topics clearly."
    )

    # create runner
    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service
    )

    # create session
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    # build user message
    message = types.Content(
        role="user",
        parts=[types.Part(text="Explain artificial intelligence")]
    )

    # run the agent
    final_response = None

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=message
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text

    print(final_response)


# run program
if __name__ == "__main__":
    asyncio.run(main())