import os
import time
import streamlit as st

from google import genai
from google.genai import errors
from dotenv import load_dotenv

load_dotenv()


@st.cache_resource
def load_client():
    return genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )


def generate_answer(context, question):

    client = load_client()

    prompt = f"""
You are an Enterprise AI Knowledge Assistant.

Answer ONLY using the provided context.

If the answer is not found in the context, reply exactly:

"I couldn't find that information in the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
"""

    models = [
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
        "gemini-flash-latest"
    ]

    last_error = None

    for model in models:

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                return response.text

            except errors.ServerError as e:

                last_error = e

                time.sleep(2)

            except Exception as e:

                last_error = e

                break

    raise last_error