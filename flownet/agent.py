from ollama import chat
from ollama import ChatResponse

class Agent:
    def __init__(self, name: str, model: str, desc: str, role: str, beha: str):
        self.model = model
        self.role = role
        self.name = name 
        self.desc = desc
        self.beha = beha

    def run(self, ctx, goal: str) -> ChatResponse:
        agent_response: ChatResponse = chat(model=self.model, messages=[
            {
                'role': self.role,
                'content': f'You are: {self.desc} .And should act like this: {self.beha}'
            },
            {
                'role': self.role,
                'content': f'Take into account this information: {ctx}'
            },
            {
                'role': self.role,
                'content': f'Perform the tasks as descrived in {goal}',
            }
        ])

        return agent_response
    
    def has_custom_goal(self):
        return False
