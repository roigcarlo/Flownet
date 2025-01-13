import json

from pathlib import Path

from flownet.agent import Agent
from flownet.operator import Operator
from flownet.translator import Translator

KRATOS_PATH = Path("/home/roigcarlo/Kratos")
FLOWGH_PATH = Path("/home/roigcarlo/Flowgraph")

TARGET_NAME = "fix_scalar_variable_process"

MAIN_MODEL = 'phi4'

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
        model=MAIN_MODEL, desc='An Expert angent that looks into a context and uderstands how to make a class transformation based on the examples provided.', role='user', beha='Only answers with code. No description or explanation given.', ref=f'{kts_ref_ctx}', res=f'{fgh_res_ctx}', src=f'{kts_src_ctx}', lng='javascript'),
    Agent(name='Evaluator', 
        model=MAIN_MODEL, desc='An expert engineer specialized In answering: "Is this class correct?". You are specialized in javascript. Your focus on syntax and meaning, but not care about calls to other libraries that may be missing', role='user', beha='Only answers "YES" and "NO". No extra information about the reasoning is given.'),
    Agent(name='Optimizer',
        model=MAIN_MODEL, desc='An expert engineer specialized in understanding a class and proposing improvements if necessary"', role='user', beha='Answers with an improved version of the input code'),
    Agent(name='Debugger',
        model=MAIN_MODEL, desc='An expert engineer specialized in detecting possible bugs and fixing them"', role='user', beha='Answers with a version of the code without bugs'),
    Agent(name='Procastinator',
        model=MAIN_MODEL, desc='An expert in doing nothing, It will waste time and resources.', role='user', beha='To lazy to do anything'),
]

operator = Operator(model=MAIN_MODEL, goal='I want to get a class in python and translate it to its equivalent to javascript according to the context given', agents=agents)

result = operator.Execute()

with open(Path('logs') / "result.json", "w+") as f:
    f.write(json.dumps(result, indent=4))

# JS_OUT_PATH = Path("C:/Users/Usuario/Desktop/OpenerSpotify")

# with open(JS_OUT_PATH / "classes" / f"{TARGET_NAME}.js", "w") as f:
#     class_code = '\n'.join(writter["message"]["content"].split('\n')[1:-1])
#     f.write(class_code)
