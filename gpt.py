import os
from openai import OpenAI

def call_gemini(prompt: str) -> str:
    """Call Gemini API via OpenAI compatible endpoint."""
    client = OpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    response = client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content