from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from src.config import settings
from src.logger import log_info, log_error

client = Groq(api_key=settings.GROQ_API_KEY)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception),
    reraise=True,
)
def call_llm(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Analyze this lead and return JSON only."},
            ],
            temperature=0.1,
            max_tokens=500,
        )
        result = response.choices[0].message.content.strip()
        log_info("LLM response received")
        return result

    except Exception as e:
        log_error(f"LLM call failed: {e}")
        raise