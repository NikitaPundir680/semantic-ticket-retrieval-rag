from src.semantic_search import semantic_search

TOP_K = 5
SIMILARITY_THRESHOLD = 0.55
MIN_SUPPORTING_DOCS = 2

def retrieve_evidence(query, df):
    results = semantic_search(query, top_k=TOP_K)

    # Filter by similarity threshold
    evidence = results[results["similarity"] >= SIMILARITY_THRESHOLD]

    return evidence

def is_answer_allowed(evidence):
    if len(evidence) < MIN_SUPPORTING_DOCS:
        return False
    return True

def build_context(evidence):
    print("DEBUG: rows received in build_context =", len(evidence))
    print(evidence[['message_text', 'category', 'similarity']])
    context_blocks = []

    for _, row in evidence.iterrows():
        block = f"""
Ticket:
- Text: {row['message_text']}
- Category: {row['category']}
"""
        context_blocks.append(block)

    return "\n".join(context_blocks)

def build_prompt(user_query, context):
    return f"""
You are a customer support assistant.

RULES (STRICT):
- Base factual statements ONLY on the provided context.
- Do NOT invent timelines, policies, or guarantees.
- Do NOT claim actions were taken.
- You MAY suggest generic next steps that do not require new facts
  (e.g., contacting support, checking order status).
- If the context is insufficient, say so clearly.
- Keep response under 80 words.

CONTEXT:
{context}

USER QUESTION:
{user_query}

Give a short, direct answer.
"""

