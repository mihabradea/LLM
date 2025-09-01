# main.py
import re
from chatbot import run_chat_turn

BADWORDS = {"injuratura1", "injuratura2"} 

def is_clean(text: str) -> bool:
    t = text.lower()
    return not any(b in t for b in BADWORDS)

def main():
    print("📚 Book Recommender Chatbot \nWrite 'exit' to quit.\n")
    while True:
        q = input("Tu: ").strip()
        if q.lower() in {"exit", "quit"}:
            break
        if not is_clean(q):
            print("Bot: Te rog formulează întrebarea fără limbaj nepotrivit. Mulțumesc!")
            continue

        try:
            answer = run_chat_turn(q)
            print(f"\nBot: {answer}\n")
        except Exception as e:
            print(f"\nBot: A apărut o eroare: {e}\n")

if __name__ == "__main__":
    main()
