# MediBrief Swarm

## Project Description
MediBrief Swarm is a multi-agent digital employee built with Google ADK and Gemini. It safely researches healthcare AI topics, structures findings through a research framework tool, and produces a concise executive brief for the user.

## Functional Diagram
![Functional Diagram](app/functional-diagram.png)

```mermaid
flowchart TD
    U[User Query] --> M[Manager Agent]
    M --> G[Guardrail Tool]
    G -->|Allowed| R[Researcher Agent]
    G -->|Restricted| S1[Safe Response]
    R --> T[Research Framework Tool]
    T --> R
    R --> S[Summarizer Agent]
    S --> O[Final Executive Brief]