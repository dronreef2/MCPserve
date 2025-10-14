import os
import logging
from openai import OpenAI, OpenAIError

logger = logging.getLogger(__name__)

def call_gemini(prompt: str, max_retries: int = 3) -> str:
    """Call Gemini API via OpenAI compatible endpoint with retry logic."""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        # Validate API key format
        if not api_key.startswith("AIza") and len(api_key) < 20:
            logger.warning("GEMINI_API_KEY format may be invalid")

        client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        for attempt in range(max_retries):
            try:
                logger.info(f"Calling Gemini API (attempt {attempt + 1}/{max_retries})")

                response = client.chat.completions.create(
                    model="gemini-1.5-flash",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=4000,
                    temperature=0.7,
                    timeout=60
                )

                if response.choices and len(response.choices) > 0:
                    content = response.choices[0].message.content
                    if content:
                        logger.info("Successfully received response from Gemini API")
                        return content.strip()
                    else:
                        raise ValueError("Empty response from Gemini API")

            except OpenAIError as e:
                logger.warning(f"Gemini API error on attempt {attempt + 1}: {str(e)}")
                if attempt == max_retries - 1:
                    raise

                # Wait before retry (exponential backoff)
                import time
                time.sleep(2 ** attempt)

        raise ValueError("Max retries exceeded")

    except Exception as e:
        logger.error(f"Failed to call Gemini API: {str(e)}")
        raise ValueError(f"Gemini API call failed: {str(e)}")