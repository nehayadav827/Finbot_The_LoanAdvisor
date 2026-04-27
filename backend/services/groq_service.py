"""
Groq LLM service – uses llama-3.3-70b-versatile via Groq API.
"""
import os
import json
import httpx
from typing import Optional

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

async def call_groq(
    system_prompt: str,
    messages: list[dict],
    temperature: float = 0.3,
    max_tokens: int = 512,
    json_mode: bool = False,
) -> str:
    """
    Call Groq API and return assistant content string.
    Raises RuntimeError on failure.
    """
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY environment variable not set.")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": system_prompt}] + messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(GROQ_API_URL, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


async def extract_json(system_prompt: str, messages: list[dict]) -> dict:
    """Call Groq in JSON mode and parse result."""
    raw = await call_groq(system_prompt, messages, json_mode=True, temperature=0.1)
    # Strip markdown fences if present
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())
