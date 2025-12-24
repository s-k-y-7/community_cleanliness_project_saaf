import os
import google.generativeai as genai
from django.conf import settings

_client = None

def get_gemini_client():
    global _client

    if _client is None:
        if not settings.GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is not set")

        genai.configure(api_key=settings.GEMINI_API_KEY)
        _client = genai

    return _client
