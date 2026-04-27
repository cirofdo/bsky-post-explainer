import os
import json
from pathlib import Path

import yaml
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np

load_dotenv("backend/.env")

# Load prompts from config file
_prompts_path = Path(__file__).parent.parent / "prompts.yaml"
with open(_prompts_path) as f:
    PROMPTS = yaml.safe_load(f)

MODEL = os.environ["OPENAI_MODEL"]


def openai_client_auth():
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return client


def extract_entities(client, post_text: str) -> list[str]:
    prompt = PROMPTS["extract_entities"]
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"].format(post_text=post_text)},
        ],
        response_format={"type": "json_object"},
    )
    data = json.loads(response.choices[0].message.content)
    return [item for values in data.values() for item in values]


def generate_queries(client, post_text: str) -> list[str]:
    prompt = PROMPTS["generate_queries"]
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"].format(post_text=post_text)},
        ],
        response_format={"type": "json_object"},
    )
    data = json.loads(response.choices[0].message.content)
    return data["queries"]


def summarize(client, post_text: str, context_posts: list[str]) -> str:
    prompt = PROMPTS["summarize"]
    context_str = "\n---\n".join(context_posts)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt["system"]},
            {
                "role": "user",
                "content": prompt["user"].format(
                    post_text=post_text, context_str=context_str
                ),
            },
        ],
    )
    return response.choices[0].message.content


def embed(client, text: list[str]) -> list[list[float]]:
    result = client.embeddings.create(model="text-embedding-3-small", input=text)
    return result


def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

