from typing import List, Dict, Any
from agents import StudentAgent, TeacherAgent

STUDENTS = [
    StudentAgent("Alice", "Analytical and logical", "Advanced"),
    StudentAgent("Bob", "Creative but easily distracted", "Intermediate"),
    StudentAgent("Charlie", "Risk-averse, hesitates before answering", "Beginner"),
    StudentAgent("Diana", "Leadership-oriented, takes charge", "Advanced"),
    StudentAgent("Ethan", "Detail-focused, asks clarifying questions", "Intermediate")
]

class SimulationOrchestrator:
    def __init__(self, scenario: str):
        self.teacher = TeacherAgent(scenario)
        self.students = STUDENTS
        self.transcript: List[Dict[str, str]] = []
        
    def add_turn(self, author: str, role: str, content: str):
        turn = {"author": author, "role": role, "content": content}
        self.transcript.append(turn)
        
    def run_simulation(self) -> List[Dict[str, str]]:
        # Phase 1: Teacher introduces the problem
        teacher_intro = self.teacher.generate_response(self.transcript)
        self.add_turn("Teacher", "Teacher", teacher_intro)
        
        # Round 1: Each student responds
        for student in self.students:
            response = student.generate_response(self.transcript)
            self.add_turn(student.name, "Student", response)
            
        # Phase 2: Teacher follows up and targets specific students
        teacher_followup = self.teacher.generate_response(self.transcript)
        self.add_turn("Teacher", "Teacher", teacher_followup)
        
        # Round 2: Each student responds again
        for student in self.students:
            response = student.generate_response(self.transcript)
            self.add_turn(student.name, "Student", response)
            
        # Phase 3: Free discussion (a few students respond to each other)
        # For prototype: Just let Diana and Alice exchange (leaders/advanced)
        diana = next(s for s in self.students if s.name == "Diana")
        diana_resp = diana.generate_response(self.transcript)
        self.add_turn("Diana", "Student", diana_resp)
        
        alice = next(s for s in self.students if s.name == "Alice")
        alice_resp = alice.generate_response(self.transcript)
        self.add_turn("Alice", "Student", alice_resp)
        
        return self.transcript
