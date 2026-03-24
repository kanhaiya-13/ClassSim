import os
from pydantic import BaseModel, Field
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# OpenRouter Configuration
def get_llm():
    return ChatOpenAI(
        model="meta-llama/llama-3.3-70b-instruct:free",
        openai_api_key=os.environ.get("OPENROUTER_API_KEY", ""),
        openai_api_base="https://openrouter.ai/api/v1",
        max_tokens=500
    )
    
class StudentAgent:
    def __init__(self, name: str, disposition: str, knowledge_level: str):
        self.name = name
        self.disposition = disposition
        self.knowledge_level = knowledge_level
        self.llm = get_llm()
        self.system_prompt = f"""You are a student named {name} participating in a classroom simulation.
Your hidden behavioral disposition is: {disposition}.
Your hidden knowledge level is: {knowledge_level}.

Instructions:
1. Reveal your traits through your behavior, the types of questions you ask, your confidence level, and how you frame your ideas.
2. DO NOT explicitly state your disposition or knowledge level. Let it shine through your actions.
3. Collaborate with or challenge other students. You can mention them by name.
4. Keep your responses concise (1-2 paragraphs max).
"""

    def generate_response(self, transcript_history: List[dict]) -> str:
        messages = [SystemMessage(content=self.system_prompt)]
        for turn in transcript_history:
            if turn["author"] == "Teacher":
                messages.append(HumanMessage(content=f"Teacher: {turn['content']}"))
            elif turn["author"] == self.name:
                messages.append(AIMessage(content=turn["content"]))
            else:
                messages.append(HumanMessage(content=f"Student {turn['author']}: {turn['content']}"))
        
        # Add prompt instructing them to reply
        messages.append(HumanMessage(content="It is your turn to speak. Reply to the discussion."))
        response = self.llm.invoke(messages)
        return response.content
        
class TeacherAgent:
    def __init__(self, scenario: str):
        self.name = "Teacher"
        self.scenario = scenario
        self.llm = get_llm()
        self.system_prompt = f"""You are the teacher in a healthcare classroom simulation.
Your scenario to guide the discussion: {scenario}

Instructions:
1. Facilitate the discussion, DO NOT just lecture.
2. Direct specific questions to specific students by name. (The students are: Alice, Bob, Charlie, Diana, Ethan)
3. Keep the conversation moving and engaged.
4. Keep your responses concise (1-2 paragraphs max).
"""
        
    def generate_response(self, transcript_history: List[dict]) -> str:
        messages = [SystemMessage(content=self.system_prompt)]
        for turn in transcript_history:
            if turn["author"] == "Teacher":
                messages.append(AIMessage(content=turn["content"]))
            else:
                messages.append(HumanMessage(content=f"Student {turn['author']}: {turn['content']}"))
        
        messages.append(HumanMessage(content="Act as the teacher and continue the discussion. Ask a targeted question if appropriate."))
        response = self.llm.invoke(messages)
        return response.content

class MetaAgentOutput(BaseModel):
    name: str = Field(description="The student's name")
    traits: List[str] = Field(description="3-4 bullet behavioral traits identified from transcript")
    problem_statement: str = Field(description="A 2-3 sentence personalized PBL problem statement")

class MetaAgent:
    def __init__(self):
        self.llm = get_llm()
        
    def analyze_student(self, student_name: str, transcript: List[dict]) -> MetaAgentOutput:
        # Format the transcript into a text block
        transcript_text = ""
        for turn in transcript:
            transcript_text += f"{turn['author']} ({turn['role']}): {turn['content']}\n"
            
        system_prompt = """You are a meta-agent observing a classroom simulation. 
Your job is to analyze the entire conversation log and extract a behavioral profile for a specific student.
Only infer traits purely from what the student said or how they interacted with others.
Then, generate a unique Problem-Based Learning (PBL) problem statement for that student tailored to push them just beyond their comfort zone.
Match their interest signals but target their knowledge gaps. 

Output your analysis strictly in JSON format matching the schema."""
        
        human_prompt = f"Analyze the following transcript focusing on student: {student_name}.\n\nTranscript:\n{transcript_text}"
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        # Using LLM with structured output (assuming model supports tool calling or JSON mode)
        structured_llm = self.llm.with_structured_output(MetaAgentOutput)
        response = structured_llm.invoke(messages)
        return response
