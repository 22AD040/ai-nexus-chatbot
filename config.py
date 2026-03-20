import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"


load_dotenv(dotenv_path=ENV_PATH)


GEMINI_API_KEY = (
    st.secrets.get("GEMINI_API_KEY", "")
    or os.getenv("GEMINI_API_KEY", "")
).strip()

MODEL_NAME = "gemini-2.5-flash"