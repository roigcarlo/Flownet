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
        agent_behavior = f"""
            You are a {self.desc}, which has this info:
            1 - {self.beha}
            2 - {ctx}

            And should perform the tasks accoring to your role that make sense for this objective: 
            1 - {goal}
        """

        agent_response: ChatResponse = chat(model='llama3.1', messages=[{
            'role': self.role,
            'content': agent_behavior,
        }])

        return agent_response
    
    def has_custom_goal(self):
        return False