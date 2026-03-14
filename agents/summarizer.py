from google.adk.agents import LlmAgent

summarizer_agent = LlmAgent(
    name="summarizer_agent",
    model="gemini-2.5-flash",
    instruction="""
You are the Summarizer Agent.

Take the research findings and turn them into:
THINKING:
SUMMARY:
KEY POINTS:
FINAL ANSWER:

Make the final answer concise, clear, and presentation-ready.
""",
)