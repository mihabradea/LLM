import streamlit as st
import sys
sys.path.append("..\\chatbot")
from chatbot import run_chat_turn
import os

# Stil personalizat (CSS)
def apply_custom_style():
    st.markdown("""
        <style>
        body {
            background-color: #f3f1ea;
        }
        .stApp {
            font-family: 'Segoe UI', sans-serif;
        }
        .title {
            font-size: 50px;
            text-align: center;
            color: #3e3e3e;
        }
        .subtitle {
            text-align: center;
            color: #7a7a7a;
        }
        .chat-bubble {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 15px;
            margin-top: 15px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)


class StreamlitUI:
    def __init__(self, api_key: str, vector_store_id: str):
        self.api_key = api_key
        self.vector_store_id = vector_store_id

    def launch(self):
        apply_custom_style()

        st.markdown('<div class="title">📚 ReadGPT</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Welcome! 📚 Feel free to ask me anything about any book: from timeless classics to modern fantasy. Whether you\'re looking for a summary, a recommendation, or simply curious about what to read next, I\'m here to help!</div>', unsafe_allow_html=True)
        st.markdown("---")

        query = st.text_input("✍️ Ask a question...")

        if query:
            result = run_chat_turn(query)
            st.markdown(f'<div class="chat-bubble">💬 <strong>Answer:</strong><br>{result}</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    API_KEY = os.getenv("OPENAI_API_KEY")
    VECTOR_STORE_ID = os.getenv("CHROMA_COLLECTION", "book_summaries")

    app = StreamlitUI(api_key=API_KEY, vector_store_id=VECTOR_STORE_ID)
    app.launch()
