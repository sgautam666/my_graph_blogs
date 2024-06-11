from dotenv import load_dotenv

load_dotenv()
from pprint import pprint

from graph.graph import app

question1 = "find articles about oxidative stress. Return the title of the most relevant article?"
inputs = {"question": question1}

for output in app.stream(inputs):
    for key, value in output.items():
        pprint(f"Finished running: {key}:")
pprint(value["generation"])