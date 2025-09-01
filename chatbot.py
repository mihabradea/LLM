# chatbot.py
import os
import json
import openai
from dotenv import load_dotenv
from retriever import retrieve_candidates
from tools import get_summary_by_title, openai_tools

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = (
    "Ești un asistent care recomandă cărți. Primești o întrebare a utilizatorului "
    "și o listă de candidate (titlu + rezumat scurt). "
    "Alege cea mai potrivită carte, explică pe scurt de ce, și răspunde conversațional. "
    "După ce decizi titlul final, apelează tool-ul get_summary_by_title cu acel titlu. "
    "NU inventa titluri. Dacă nu ești sigur, spune asta și cere clarificări."
)

BAD_WORDS = [
    "injuratura1", "injuratura2"
]

def contains_bad_words(text):
    text_lc = text.lower()
    return any(bad_word in text_lc for bad_word in BAD_WORDS)

def build_context_message(query: str, candidates: list[dict]) -> str:
    lines = [f"Întrebarea utilizatorului: {query}", "", "Cărți candidate:"]
    for i, c in enumerate(candidates, 1):
        lines.append(f"{i}. {c['title']} — {c['short_summary']}")
    lines.append("")
    lines.append("Răspunde: recomandare conversațională + (vei apela tool-ul pentru rezumat detaliat).")
    return "\n".join(lines)

def call_openai_with_tools(messages):
    return openai.chat.completions.create(
        model="gpt-4o-mini",  
        messages=messages,
        tools=openai_tools,
        temperature=0.4,
    )

def run_chat_turn(user_query: str) -> str:
    # Filtru de limbaj nepotrivit
    if contains_bad_words(user_query):
        return "Te rog să folosești un limbaj respectuos. Sunt aici să te ajut cu recomandări de cărți!"

    # 1) RAG
    candidates = retrieve_candidates(user_query, k=4)
    if not candidates:
        return "Nu am găsit încă rezultate în vector store. Încearcă altă formulare."

    # 2) Mesaje
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": user_query},
        {"role": "assistant", "content": build_context_message(user_query, candidates)},
    ]

    # 3) Primul răspuns 
    first = call_openai_with_tools(messages)
    msg = first.choices[0].message


    # 4) Dacă modelul a cerut tool-ul, îl apelăm local și continuăm conversația 
    if getattr(msg, "tool_calls", None):
        messages.append({"role": "assistant", "content": msg.content or "", "tool_calls": msg.tool_calls})
        for tool_call in msg.tool_calls:
            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments or "{}")
            if tool_name == "get_summary_by_title":
                title = args.get("title", "")
                detailed = get_summary_by_title(title)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": detailed,
                })
        final = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.4,
        )
        return final.choices[0].message.content.strip()

    # Fallback: dacă nu a cerut tool-ul, returnăm mesajul brut
    return (msg.content or "").strip()
