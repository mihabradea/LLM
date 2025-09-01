from book_summaries import book_summaries,   book_summaries_dict

def get_summary_by_title(title: str) -> str:
    """Returnează rezumatul detaliat pentru un titlu exact."""
    return book_summaries_dict.get(title, "Nu am găsit rezumatul pentru titlul dat.")

openai_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_summary_by_title",
            "description": "Returnează rezumatul detaliat pentru o carte cu titlu exact.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Titlul exact al cărții"},
                },
                "required": ["title"],
            },
        },
    }
]
