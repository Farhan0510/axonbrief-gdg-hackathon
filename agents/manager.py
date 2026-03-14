from google.adk.agents import LlmAgent
from agents.researcher import researcher_agent
from agents.summarizer import summarizer_agent
from tools.research_tools import guardrail_check

manager_agent = LlmAgent(
    name="manager_agent",
    model="gemini-2.5-flash",
    instruction="""
You are the Manager Agent.

Workflow:
1. Always call guardrail_check first on the user's query.
2. If the query is restricted, return the safe response and stop.
3. If allowed, delegate research to researcher_agent.
4. Then send the research result to summarizer_agent.
5. Return the final polished answer.

Show:
THINKING:
DELEGATION:
FINAL OUTPUT:
""",
    tools=[guardrail_check],
    sub_agents=[researcher_agent, summarizer_agent]
)