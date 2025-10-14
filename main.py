import os
import requests
from mcp.server.fastmcp import FastMCP
from gpt import call_gemini
from prompt import get_prompt

app = FastMCP("ai-tools")

@app.tool()
async def fetch(url: str) -> str:
    """Fetch the content of a web page using Jina AI."""
    jina_api_key = os.getenv("JINA_API_KEY")
    if not jina_api_key:
        return "Error: JINA_API_KEY not set"
    
    response = requests.get(f"https://r.jina.ai/{url}", headers={"Authorization": f"Bearer {jina_api_key}"})
    if response.status_code == 200:
        return response.text
    else:
        return f"Error fetching {url}: {response.status_code}"

@app.tool()
async def search(query: str) -> str:
    """Search the web using Jina AI."""
    jina_api_key = os.getenv("JINA_API_KEY")
    if not jina_api_key:
        return "Error: JINA_API_KEY not set"
    
    response = requests.get(f"https://s.jina.ai/{query}", headers={"Authorization": f"Bearer {jina_api_key}"})
    if response.status_code == 200:
        return response.text
    else:
        return f"Error searching {query}: {response.status_code}"

@app.tool()
async def translate(text: str, from_lang: str = "zh", to_lang: str = "en") -> str:
    """Translate text between Chinese and English using Gemini."""
    prompt = f"Translate the following {from_lang} text to {to_lang}: {text}"
    return call_gemini(prompt)

@app.tool()
async def translate_deepl(text: str, from_lang: str = "auto", to_lang: str = "en") -> str:
    """Translate text using DeepL API."""
    deepl_api_key = os.getenv("DEEPL_API_KEY")
    if not deepl_api_key:
        return "Error: DEEPL_API_KEY not set"
    
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        "text": text,
        "source_lang": from_lang.upper(),
        "target_lang": to_lang.upper()
    }
    headers = {"Authorization": f"DeepL-Auth-Key {deepl_api_key}"}
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result["translations"][0]["text"]
    else:
        return f"Error translating: {response.status_code}"

@app.prompt()
def optimize_prompt(user_prompt: str) -> str:
    """Optimize a user prompt using detailed templates."""
    return get_prompt(user_prompt)

if __name__ == "__main__":
    import mcp.server
    app.run()