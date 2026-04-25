import os
from dotenv import load_dotenv
from openai import OpenAI   # ← HERE

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(query):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI."},
            {"role": "user", "content": query}
        ]
    )

    return response.choices[0].message.content