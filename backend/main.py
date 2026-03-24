from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimulationRequest(BaseModel):
    scenario: str

class ChatMessage(BaseModel):
    author: str
    role: str
    content: str
    
class TranscriptRequest(BaseModel):
    transcript: List[ChatMessage]

class BehavioralProfile(BaseModel):
    name: str
    traits: List[str]
    problem_statement: str

from agents import MetaAgent
from simulation import SimulationOrchestrator

@app.post("/api/simulation/start", response_model=List[ChatMessage])
async def start_simulation(req: SimulationRequest):
    orchestrator = SimulationOrchestrator(scenario=req.scenario)
    transcript = orchestrator.run_simulation()
    return transcript

@app.post("/api/simulation/analyze", response_model=List[BehavioralProfile])
async def analyze_simulation(req: TranscriptRequest):
    meta_agent = MetaAgent()
    profiles = []
    # Identify unique students from transcript
    student_names = set(turn.author for turn in req.transcript if turn.role == "Student")
    transcript_dicts = [{"author": t.author, "role": t.role, "content": t.content} for t in req.transcript]
    
    for name in student_names:
        result = meta_agent.analyze_student(name, transcript_dicts)
        profiles.append(
            BehavioralProfile(
                name=result.name,
                traits=result.traits,
                problem_statement=result.problem_statement
            )
        )
    return profiles

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

