import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)


def build_context(chat_history):
    """
    Convert chat history into context string
    """
    context = ""
    for chat in chat_history[-5:]:  # last 5 messages only (efficient)
        context += f"User: {chat['prompt']}\nAI: {chat['response']}\n"
    return context


def get_response(prompt: str, chat_history=None) -> str:
    if not API_KEY:
        return "⚠️ API key missing. Please set GEMINI_API_KEY."

    try:
        context = build_context(chat_history or [])

        final_prompt = f"""
You are a helpful AI assistant.

Conversation so far:
{context}

User: {prompt}

Instructions:
- Understand previous conversation context
- Give clear, relevant answer
- Do NOT say "I don’t know previous context"
- Be concise but helpful

Answer:
"""

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(final_prompt)

        return response.text.strip()

    except Exception as e:
        return f"❌ Error: {str(e)}"