from ollama import chat
from ollama import ChatResponse

from flownet.agent import Agent

class Translator(Agent):
    def __init__(self, name: str, model: str, desc: str, role: str, beha: str, ref: str, res: str, src: str, lng: str):
        super().__init__(name, model, desc, role, beha)
        self.ref = ref
        self.res = res
        self.src = src 
        self.lng = lng

        self.goal  = ' '.join(f"""
            In my system this class: {self.ref} gives as a result this other class: {self.res}.
            Which {self.lng} code should I write to get the same result for this class: {self.src}?
            Give the code of the js class.
        """.split(' '))

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
                'content': f'Perform the tasks as descrived in {self.goal}',
            }
        ])

        return agent_response
    
    def has_custom_goal(self):
        return True
