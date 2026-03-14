from google.adk.agents import LlmAgent
from tools.research_tools import research_framework

researcher_agent = LlmAgent(
    name="researcher_agent",
    model="gemini-2.5-flash",
    instruction="""
You are the Research Agent.

Always call the research_framework tool first.
Use the tool output to structure your research.

Then produce:
THINKING:
RESEARCH FINDINGS:
- main facts
- important points
- useful examples

Do not give personal medical advice.
Keep the content educational and general.
""",
    tools=[research_framework]
)