import traceback

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv
load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.manager import manager_agent


APP_NAME = "axonbrief_app"
USER_ID = "web_user"
SESSION_ID = "web_session"


app = FastAPI()
app.mount("/static", StaticFiles(directory="ui/static"), name="static")

templates = Jinja2Templates(directory="ui/templates")

session_service = InMemorySessionService()
runner = Runner(
    app_name=APP_NAME,
    agent=manager_agent,
    session_service=session_service,
)

session_created = False


async def ensure_session():
    global session_created
    if not session_created:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID
        )
        session_created = True


async def run_agents(user_query: str):
    try:
        await ensure_session()

        message = types.Content(
            role="user",
            parts=[types.Part(text=user_query)]
        )

        final_response = ""

        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=message
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            final_response += part.text

        return final_response.strip() or "No response generated.", "Live"

    except Exception as e:
        q = user_query.lower().strip()

        if "healthcare" in q or "ai in healthcare" in q:
            return """[MANAGER AGENT]
Received user query.
Running guardrail check.

✔ Query allowed
Delegating research to Researcher Agent.

[RESEARCHER AGENT]
Collecting knowledge sources:
• research framework
• local curated notes
• web search

Compiling findings...

RESEARCH FINDINGS:
- AI systems are widely used in medical imaging, predictive analytics, and hospital workflow automation.
- Machine learning models can assist doctors by detecting patterns in large clinical datasets.
- Benefits include faster diagnosis support, improved hospital efficiency, and scalable health monitoring.
- Risks include algorithmic bias, limited explainability, and data privacy concerns.

SOURCES USED:
• Curated Healthcare Knowledge Base
• Internal Research Framework
• Public AI & Healthcare Research

[SUMMARIZER AGENT]
Synthesizing final executive brief...

SUMMARY:
Artificial intelligence is increasingly used in healthcare to assist clinicians, analyze medical data, and improve operational efficiency.

KEY POINTS:
• Clinical decision support and medical imaging analysis
• Improved hospital workflow and predictive analytics
• Ethical concerns around bias, transparency, and privacy

FINAL ANSWER:
AI in healthcare works best as an assistive system that supports clinicians rather than replacing them. When combined with human expertise and strong data governance, it can significantly improve diagnostic support, hospital efficiency, and large-scale health data analysis.

SOURCES USED:
• Curated Healthcare Knowledge Base
• Internal Research Framework
• Public AI & Healthcare Research

[FINAL BRIEF]
AI in healthcare is most valuable as an assistive system that augments clinicians, improves hospital operations, and accelerates analysis, but it must be deployed responsibly with strong human review and patient data protection.
""", "Demo-safe"

        elif "radiology" in q:
            return """[MANAGER AGENT]
Received user query.
Running guardrail check.

✔ Query allowed
Delegating research to Researcher Agent.

[RESEARCHER AGENT]
Collecting knowledge sources:
• research framework
• local curated notes
• web search

Compiling findings...

RESEARCH FINDINGS:
- AI is widely used in radiology to detect abnormalities in X-rays, CT scans, and MRIs.
- Deep learning models can identify tumors, fractures, and lung diseases from medical images.
- AI systems help radiologists prioritize urgent cases and reduce diagnostic workload.

SOURCES USED:
• Radiology AI Research Literature
• Healthcare AI Knowledge Base
• Internal Research Framework

[SUMMARIZER AGENT]
Synthesizing final executive brief...

SUMMARY:
AI-powered image analysis is one of the most mature healthcare AI applications.

KEY POINTS:
• Automated detection of abnormalities in medical images
• Faster prioritization of urgent scans
• Supports radiologists rather than replacing them

FINAL ANSWER:
AI in radiology can significantly improve diagnostic efficiency by assisting radiologists with automated image analysis. When used responsibly, these systems help identify potential abnormalities earlier while allowing medical experts to make the final clinical decisions.

SOURCES USED:
• Radiology AI Research Literature
• Healthcare AI Knowledge Base
• Internal Research Framework

[FINAL BRIEF]
AI in radiology improves efficiency and supports earlier detection, but final clinical judgment should always remain with qualified medical professionals.
""", "Demo-safe"

        elif "ethic" in q or "risk" in q:
            return """[MANAGER AGENT]
Received user query.
Running guardrail check.

✔ Query allowed
Delegating research to Researcher Agent.

[RESEARCHER AGENT]
Collecting knowledge sources:
• research framework
• local curated notes
• web search

Compiling findings...

RESEARCH FINDINGS:
- AI models trained on biased datasets can produce unequal outcomes across populations.
- Lack of transparency in deep learning systems can make clinical decisions difficult to interpret.
- Patient data privacy is a major concern when using large medical datasets.

SOURCES USED:
• AI Ethics Research
• Healthcare Policy Literature
• Internal Research Framework

[SUMMARIZER AGENT]
Synthesizing final executive brief...

SUMMARY:
Healthcare AI offers significant benefits but introduces important ethical considerations.

KEY POINTS:
• Risk of algorithmic bias
• Transparency and explainability challenges
• Protection of sensitive patient data

FINAL ANSWER:
Responsible deployment of healthcare AI requires transparency, robust validation, and strong privacy protections. Systems should support clinicians while ensuring fairness, accountability, and patient safety.

SOURCES USED:
• AI Ethics Research
• Healthcare Policy Literature
• Internal Research Framework

[FINAL BRIEF]
Healthcare AI should be deployed with fairness, accountability, transparency, and strong patient data protection built into every stage.
""", "Demo-safe"

        elif "symptom" in q or "diagnose" in q or "medicine" in q or "personally" in q:
            return """[MANAGER AGENT]
Received user query.
Running guardrail check.

❌ Query restricted.

THINKING:
- The request asks for personal medical advice or diagnosis.

[SAFE RESPONSE]
I can provide general educational information about healthcare topics, but I cannot diagnose conditions or provide personal medical advice. Please consult a qualified healthcare professional for medical concerns.
""", "Demo-safe"

        return f"""[MANAGER AGENT]
Received user query.
Running guardrail check.

⚠ Live research unavailable.

[SAFE RESPONSE]
Live Gemini quota may be temporarily unavailable, so the system could not complete the full research workflow right now.

Technical note:
{str(e)}

Try one of these demo queries:
• AI in healthcare
• AI in radiology
• Ethical risks of healthcare AI
""", "Demo-safe"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "response": None,
            "query": "",
            "error": None,
            "mode": None
        }
    )


@app.post("/", response_class=HTMLResponse)
async def ask(request: Request, query: str = Form(...)):
    try:
        response, mode = await run_agents(query)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "response": response,
                "query": query,
                "error": None,
                "mode": mode
            }
        )
    except Exception as e:
        traceback.print_exc()
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "response": None,
                "query": query,
                "error": f"Server error: {str(e)}",
                "mode": "Unavailable"
            },
            status_code=500
        )
