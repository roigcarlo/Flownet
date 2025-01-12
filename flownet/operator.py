from flownet.agent import Agent

from ollama import chat
from ollama import ChatResponse

class Operator:
    def __init__(self, goal: str, agents: list[Agent]):
        self.goal = goal
        self.agents = {c.name:c for c in agents}

    def Execute(self):
        # Define some special agents that will be in charge of scheduling and managing the other agents
        operator_behavior = f"""
            Your goal is to execute a task and ensure that the result is correct.
            Based on this {self.goal} which agents from this list would you select to perform that task? 
            Please choose as many as necessary to ensure the task is very well accomplished: {[(v.name, v.desc) for _,v in self.agents.items()]}.
            Why did you choose those agents?. At the end of your response give the list in this foramt ["a","b","c",...]. 
            Do not write anything else after the list
        """

        operator_response: ChatResponse = chat(model='llama3.1', messages=[{
            'role': 'user',
            'content': operator_behavior,
        }])

        agents_to_use = operator_response["message"]["content"].split('\n')[-1]

        print(operator_response["message"]["content"])
        print("\n")

        try:
            agent_list = eval(agents_to_use)
            print(f'Agents to use = {agent_list}')
        except Exception as e:
            print(f'Error Cannot parse operator output: {agents_to_use, e}')

        prev_ctx = ''

        operator_result = {}

        if agent_list:
            for agent in agent_list:
                agent_instance = self.agents[agent]

                print(f'\tAgent [EXE] [{agent_instance.name}]...')
                
                descriptor_behaviour = f"""
                    Based on the info from the general goal which is: {self.goal}, 
                    and the description of this agent which is {agent_instance.desc},

                    which should be the task of this agent?
                """

                descriptor_response: ChatResponse = chat(model='llama3.1', messages=[{
                    'role': 'user',
                    'content': descriptor_behaviour,
                }])

                print(f'\tAgent [OBJ] [{agent_instance.name}] has been defined as: {descriptor_response["message"]["content"][:10] if not agent_instance.has_custom_goal() else agent_instance.goal[:10]}...')

                agent_response = agent_instance.run(
                    ctx=prev_ctx,
                    goal=descriptor_response["message"]["content"]
                )

                print(f'\tAgent [RES] [{agent_instance.name}] response: {agent_response["message"]["content"][:10]}...')

                prev_ctx += agent_response["message"]["content"] + "\n"

                operator_result[agent_instance.name] = agent_response["message"]["content"]

        return operator_result
        