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

        self.goal  = f"""
            In my system this class: {self.ref} gives as a result this other class: {self.res}.
            Which {self.lng} code should I write to get the same result for this class: {self.src}?
            Give the code of the js class.
        """

    def run(self, ctx, goal: str) -> ChatResponse:
        agent_behavior = f"""
            My context is the following: {ctx}
            In my system this class: {self.ref} gives as a result this other class: {self.res}.
            Which {self.lng} code should I write to get the same result for this class: {self.src}?
            Give the code of the js class.
            I should stick to {self.beha}
        """

        agent_response: ChatResponse = chat(model='llama3.1', messages=[{
            'role': self.role,
            'content': agent_behavior,
        }])

        return agent_response
    
    def has_custom_goal(self):
        return True