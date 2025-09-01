Book Recommender Chatbot – Project Overview

1. What It Does?
This chatbot helps users find book recommendations and summaries through conversation. It uses OpenAI’s GPT for understanding questions and ChromaDB to search book summaries. You can ask for themes like “friendship and magic” or “war stories,” and it’ll suggest a book and give a detailed summary.

2. Key Features
- Conversational book recommendations (English & Romanian)
- Short and full book summaries
- Smart search with embeddings (RAG using ChromaDB)
- GPT-4o integration with tool-calling
- Streamlit web UI with chat history
- Offensive language filter

3. Tech Stack
- Python
- OpenAI API (GPT-4o + embeddings)
- ChromaDB (local vector store)
- Streamlit (for the UI)
- dotenv for environment variables (openAI key)

4. How It Works
- Book summaries are embedded and stored in ChromaDB
- User asks a question (e.g. "Books about courage")
- GPT uses semantic search to find the best match
- Then calls a tool to return the full summary

5. How to run it
5.1 Install dependencies:
    - pip install -r requirements.txt  
5.2 Add your OpenAI key to a .env file:
    - OPENAI_API_KEY=your-key  
5.3 Load book embeddings:
    - python embeddings_loader.py  
5.4 Start the app:
    - streamlit run ui.py  

6. Notes
- If you switch embedding models (e.g., small → large), reset ChromaDB to avoid dimension errors
- GPT handles English & Romanian, but title matching must be exact for full summaries
- The offensive word filter is easy to expand/customize. For this project, some mocked bad words were used.