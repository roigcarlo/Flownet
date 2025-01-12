from pathlib import Path

from flownet.agent import Agent
from flownet.operator import Operator
from flownet.translator import Translator

KRATOS_PATH = Path("D:/cimne/Kratos")
FLOWGH_PATH = Path("D:/cimne/Flowgraph")

TARGET_NAME = "fix_scalar_variable_process"

# Get the context info
with open(KRATOS_PATH / "kratos" / "python_scripts" / "assign_scalar_variable_process.py", "r") as f:
    kts_ref_ctx = f.read()

with open(FLOWGH_PATH / "public" / "js" / "nodes" / "processes" / "assign_scalar_variable_process.js", "r") as f:
    fgh_res_ctx = f.read()

# Prepare the question
with open(KRATOS_PATH / "kratos" / "python_scripts" / f"{TARGET_NAME}.py", "r") as f:
    kts_src_ctx = f.read()

agents = [
    Translator(name='Translator', 
        model='llama3.1', desc='An Expert angent that looks into a context and uderstands how to make a class transformation based on the examples provided.', role='user', beha='Only answers with code. No description or explanation given.', ref=f'{kts_ref_ctx}', res=f'{fgh_res_ctx}', src=f'{kts_src_ctx}', lng='javascript'),
    Agent(name='Evaluator', 
        model='llama3.1', desc='An expert engineer specialized In answering: "Is this class correct?. You specialized in javascript"', role='user', beha='Only answers "YES" and "NO". Nothing else'),
    Agent(name='Optimizer',
        model='llama3.1', desc='An expert engineer specialized in understanding a class and proposing improvements if necessary"', role='user', beha='Answers with an improved version of the input code'),
    Agent(name='Debugger',
        model='llama3.1', desc='An expert engineer specialized in detecting possible bugs and fixing them"', role='user', beha='Answers with a version of the code without bugs'),
    Agent(name='Procastinator',
        model='llama3.1', desc='An expert in doing nothing, It will waste time and resources.', role='user', beha='To lazy to do anything'),
]

operator = Operator(goal='I want to get a class in python and translate it to its equivalent to javascript according to the context given', agents=agents)

result = operator.Execute()

print("== OPERATOR EXECUTED ==")

print(result)

print("== FINAL RESULT ==")

print(result['Translator'])

# JS_OUT_PATH = Path("C:/Users/Usuario/Desktop/OpenerSpotify")

# with open(JS_OUT_PATH / "classes" / f"{TARGET_NAME}.js", "w") as f:
#     class_code = '\n'.join(writter["message"]["content"].split('\n')[1:-1])
#     f.write(class_code)