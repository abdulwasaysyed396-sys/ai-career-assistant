import os

import gradio as gr
from dotenv import load_dotenv
from huggingface_hub import InferenceClient


# Load environment variables
load_dotenv()

# Get Hugging Face token
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN is not set. Please check your .env file.")


# Create Hugging Face client
client = InferenceClient(
    token=HF_TOKEN
)


# Model
MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"


# System prompt
SYSTEM_PROMPT = """
You are an AI Career and Interview Assistant.

Your job is to help users with:
- Career guidance
- Computer Science learning
- Programming questions
- Technical interview preparation
- Resume and job preparation
- Learning roadmaps

Give clear, practical, beginner-friendly answers.

Do not make up information.
If you are unsure, clearly say that you are unsure.
"""


def chat_with_ai(message, history):
    """
    Send the user's message and conversation history
    to the Hugging Face LLM.
    """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Add previous conversation
    for user_message, assistant_message in history:
        messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        messages.append(
            {
                "role": "assistant",
                "content": assistant_message
            }
        )

    # Add current user message
    messages.append(
        {
            "role": "user",
            "content": message
        }
    )

    # Send request to the model
    response = client.chat_completion(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )

    # Extract AI response
    answer = response.choices[0].message.content

    return answer


# Create Gradio interface
demo = gr.ChatInterface(
    fn=chat_with_ai,
    title="AI Career & Interview Assistant",
    description=(
        "Ask questions about careers, programming, "
        "Computer Science and technical interviews."
    ),
    examples=[
        "How should I prepare for a Python interview?",
        "Give me a roadmap to become a Machine Learning Engineer.",
        "Explain APIs to me like I am a beginner.",
        "Give me 5 beginner SQL interview questions."
    ]
)


# Start application
if __name__ == "__main__":
    demo.launch()