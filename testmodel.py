import requests
import os
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('LLM_API_TOKEN')

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
headers = {"Authorization": token}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

output = query({
    "inputs": "For New Jersey, How long after submitting FOIA requests is a response required?",
})

print(output)
