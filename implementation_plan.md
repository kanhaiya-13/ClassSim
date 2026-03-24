# ClassSim: Multi-Agent Classroom Simulator for PBL Design

This plan outlines the steps to build a prototype of a multi-agent edtech simulation tool where student agents interact with a teacher agent around a healthcare problem. The simulation is observed by a meta-agent that generates personalized Problem-Based Learning (PBL) problem statements based on the behavioral traits revealed during the simulation.

## Proposed Changes

### Setup and Infrastructure

#### [NEW] `backend/requirements.txt`
Includes required packages: `fastapi`, `uvicorn`, `langchain`, `langchain-openai`, `python-dotenv`, `pydantic`. The backend will run within a Python virtual environment (`venv`).

#### [NEW] `backend/.env`
Environment file for storing `OPENROUTER_API_KEY`. We'll use free models provided by OpenRouter (e.g., `meta-llama/llama-3-8b-instruct:free`).

#### Next.js Frontend Setup
Create a new Next.js application in the `frontend` directory using React and TailwindCSS.

---

### Backend Components (Python / FastAPI)

#### [NEW] `backend/main.py`
FastAPI application entry point. Contains API routes:
- `POST /api/simulation/start`: Initiates a simulation run and returns the full conversation transcript.
- `POST /api/simulation/analyze`: Runs the meta-agent on a given transcript and returns the student behavioral profiles and personalized problem statements.

#### [NEW] `backend/agents.py`
Contains the definitions for the different LLM instances using `ChatOpenAI` configured for OpenRouter base URLs.
- `StudentAgent`: Contains state for name, behavioral disposition, and knowledge level. Instantiated 5 times.
- `TeacherAgent`: Contains the core healthcare scenario. Directs queries to specific students.
- `MetaAgent`: Takes the full transcript as context and outputs JSON-structured profiles and personalized PBL problem statements.

#### [NEW] `backend/simulation.py`
Orchestrates the classroom rounds (Round 1, Round 2, Free Discussion) and returns a list of conversation turns.

---

### Frontend Components (Next.js)

#### [MODIFY] `frontend/src/app/page.tsx`
The main dashboard containing two primary panels:
- **Panel 1: Simulation View**: A chat-like feed showing the classroom conversation, colored by agent roles. Includes a "Run Simulation" button that fetches data from the backend.
- **Panel 2: Meta-Agent Analysis**: A grid of cards displaying each student's name, identified behavioral traits, and the personalized PBL problem statement. Includes a "Generate Personalized Problems" button.

## Verification Plan

### Automated Tests
- Test that each agent responds consistently formatting and keeping character.
- Test that the FastAPI endpoints successfully return structured data.

### Manual Verification
- Run the simulation from the Next.js UI and observe if the conversation feed feels realistic and grounded in the provided healthcare scenario.
- Review the Meta-Agent generated problem statements to ensure they uniquely target the identified behavioral characteristics.
