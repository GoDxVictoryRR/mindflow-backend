import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import re

load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyAKXRuMPQsaBDStR5enP7QEJmT_dcVcGW8"))

model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

def extract_json(text):
    # Find first JSON object in the response
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in model response.")
    return json.loads(match.group())

def generate_mindmap(text):
    prompt = f"""
    Read the following paragraph and identify key concepts and how they are related.
    Return a JSON with:
    - nodes: list of objects with "id" and "label"
    - edges: list of objects with "from" and "to"

    Example format:
    {{
      "nodes": [{{"id": "AI", "label": "AI"}}, ...],
      "edges": [{{"from": "AI", "to": "Machine Learning"}}, ...]
    }}

    Text: {text}
    """
    try:
        response = model.generate_content(prompt)
        content = response.text
        result = extract_json(content)
        return result["nodes"], result["edges"]
    except Exception as e:
        print("Gemini Error:", e)
        return [], []
