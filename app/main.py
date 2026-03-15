import asyncio
import os
import logging

logging.getLogger("google").setLevel(logging.ERROR)

from dotenv import load_dotenv
load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agents.manager import manager_agent

APP_NAME = "axonbrief_app"
USER_ID = "farhan"
SESSION_ID = "axonbrief_session_001"


async def main():
    if not os.getenv("GOOGLE_CLOUD_PROJECT"):
        raise ValueError("GOOGLE_CLOUD_PROJECT not found in .env")

    if not os.getenv("GOOGLE_CLOUD_LOCATION"):
        raise ValueError("GOOGLE_CLOUD_LOCATION not found in .env")

    session_service = InMemorySessionService()

    runner = Runner(
        app_name=APP_NAME,
        agent=manager_agent,
        session_service=session_service,
    )

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    user_query = input("Enter your research topic: ")

    message = types.Content(
        role="user",
        parts=[types.Part(text=user_query)]
    )

    final_response = None

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=message
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                text_chunks = []
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        text_chunks.append(part.text)
                final_response = "\n".join(text_chunks).strip()

    print("\n=== FINAL RESPONSE ===\n")
    print(final_response)


if __name__ == "__main__":
    asyncio.run(main())
