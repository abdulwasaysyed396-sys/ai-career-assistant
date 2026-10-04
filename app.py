import os

import gradio as gr
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from rag import (
    extract_text_from_pdf,
    split_text,
    create_vector_database,
    search_documents
)

from tools import (
    calculator,
    generate_interview_topics
)


# ============================================================
# 1. LOAD HUGGING FACE TOKEN
# ============================================================

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError(
        "HF_TOKEN is not set. Please check your .env file."
    )


# ============================================================
# 2. CONNECT TO HUGGING FACE
# ============================================================

client = InferenceClient(token=HF_TOKEN)

MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"


# ============================================================
# 3. VARIABLES FOR RAG
# ============================================================

document_chunks = []
vector_database = None


# ============================================================
# 4. PROCESS PDF DOCUMENT
# ============================================================

def process_document(pdf_file):
    """
    Read the uploaded PDF, split it into chunks,
    create embeddings, and store them in FAISS.
    """

    global document_chunks
    global vector_database

    if pdf_file is None:
        return "Please upload a PDF first."

    try:
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_file)

        if not text.strip():
            return "Could not extract any text from the PDF."

        # Split text into smaller chunks
        document_chunks = split_text(text)

        if not document_chunks:
            return "No usable text was found in the PDF."

        # Create vector database
        vector_database = create_vector_database(
            document_chunks
        )

        return (
            "Document processed successfully! "
            f"Created {len(document_chunks)} text chunks."
        )

    except Exception as error:
        return f"Error processing document: {error}"


# ============================================================
# 5. SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are an AI Career and Interview Assistant.

Your job is to help users with:

- Career guidance
- Computer Science
- Programming
- Technical interviews
- Resume preparation
- Learning roadmaps
- Machine Learning
- Generative AI

Give clear, practical, beginner-friendly answers.

When information from an uploaded document is provided,
use that information to answer the user's question.

Do not invent information from the uploaded document.

If the answer cannot be found in the provided document,
clearly say that the information is not available
in the uploaded document.

Do not pretend that you used a tool if you did not.

Give answers that are useful for learning and interviews.
"""


# ============================================================
# 6. AGENT DECISION / ROUTER
# ============================================================

def agent_decision(message):
    """
    Decide whether the user's question should use:

    - Calculator
    - Interview topic tool
    - RAG
    - Normal LLM
    """

    message_lower = message.lower()


    # --------------------------------------------------------
    # Calculator detection
    # --------------------------------------------------------

    calculation_words = [
        "calculate",
        "percentage",
        "multiply",
        "divide",
        "add",
        "subtract"
    ]

    if any(
        word in message_lower
        for word in calculation_words
    ):
        return "calculator"


    # --------------------------------------------------------
    # Interview topic detection
    # --------------------------------------------------------

    interview_words = [
        "interview topics",
        "interview preparation topics",
        "topics for interview"
    ]

    if any(
        phrase in message_lower
        for phrase in interview_words
    ):
        return "interview_topics"


    # --------------------------------------------------------
    # RAG detection
    # --------------------------------------------------------

    if vector_database is not None:

        document_words = [
            "resume",
            "my cv",
            "my projects",
            "my education",
            "my experience",
            "my skills"
        ]

        if any(
            word in message_lower
            for word in document_words
        ):
            return "rag"


    # --------------------------------------------------------
    # Normal LLM
    # --------------------------------------------------------

    return "llm"


# ============================================================
# 7. MAIN CHAT FUNCTION
# ============================================================

def chat_with_ai(message, history):
    """
    Main function that handles the user's message.

    The agent decides whether to use:
    - Calculator
    - Interview topic tool
    - RAG
    - LLM
    """

    # --------------------------------------------------------
    # Decide which path to use
    # --------------------------------------------------------

    decision = agent_decision(message)


    # ========================================================
    # 8. CALCULATOR TOOL
    # ========================================================

    if decision == "calculator":

        expression = (
            message
            .replace("calculate", "")
            .replace("percentage", "")
            .strip()
        )

        result = calculator(expression)

        return f"The calculated result is: {result}"


    # ========================================================
    # 9. INTERVIEW TOPICS TOOL
    # ========================================================

    if decision == "interview_topics":

        topic = message.lower()

        if "python" in topic:
            selected_topic = "python"

        elif "sql" in topic:
            selected_topic = "sql"

        elif "machine learning" in topic:
            selected_topic = "machine learning"

        else:
            selected_topic = "general"


        topics = generate_interview_topics(
            selected_topic
        )


        return "\n".join(
            f"- {topic}"
            for topic in topics
        )


    # ========================================================
    # 10. RAG DOCUMENT SEARCH
    # ========================================================

    context = ""

    if (
        decision == "rag"
        and vector_database is not None
        and document_chunks
    ):

        relevant_chunks = search_documents(
            message,
            document_chunks,
            vector_database,
            top_k=3
        )

        context = "\n\n".join(
            relevant_chunks
        )


    # ========================================================
    # 11. CREATE MESSAGE HISTORY
    # ========================================================

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]


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


    # ========================================================
    # 12. ADD RAG CONTEXT IF AVAILABLE
    # ========================================================

    if context:

        user_content = f"""
Use the following information from the uploaded document
to answer the user's question.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{message}
"""

    else:

        user_content = message


    messages.append(
        {
            "role": "user",
            "content": user_content
        }
    )


    # ========================================================
    # 13. SEND REQUEST TO LLM
    # ========================================================

    try:

        response = client.chat_completion(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )

        answer = response.choices[0].message.content

        return answer

    except Exception as error:

        return (
            "Sorry, something went wrong while "
            f"communicating with the AI model.\n\n"
            f"Error: {error}"
        )


# ============================================================
# 14. GRADIO USER INTERFACE
# ============================================================

with gr.Blocks(
    title="AI Career & Interview Assistant"
) as demo:

    gr.Markdown(
        """
        # 🤖 AI Career & Interview Assistant

        Your AI assistant for:

        - Career guidance
        - Programming
        - Computer Science
        - Technical interviews
        - Resume questions
        - Learning roadmaps
        - Document-based questions

        You can also upload a PDF and ask questions
        about its contents.
        """
    )


    # ========================================================
    # PDF SECTION
    # ========================================================

    gr.Markdown("## 📄 Chat With Your Document")


    with gr.Row():

        pdf_file = gr.File(
            label="Upload a PDF",
            file_types=[".pdf"],
            type="filepath"
        )

        process_button = gr.Button(
            "Process Document"
        )


    document_status = gr.Textbox(
        label="Document Status",
        interactive=False
    )


    process_button.click(
        fn=process_document,
        inputs=pdf_file,
        outputs=document_status
    )


    # ========================================================
    # CHAT SECTION
    # ========================================================

    gr.Markdown("## 💬 Chat with the AI")


    gr.ChatInterface(
        fn=chat_with_ai,

        examples=[
            "Explain what an API is to a beginner.",

            "Calculate 9.05 * 10",

            "Give me Python interview topics",

            "Give me SQL interview topics",

            "What skills should I learn for a Machine Learning career?",

            "What projects are mentioned in my uploaded resume?"
        ]
    )


# ============================================================
# 15. START APPLICATION
# ============================================================

if __name__ == "__main__":
    demo.launch()
