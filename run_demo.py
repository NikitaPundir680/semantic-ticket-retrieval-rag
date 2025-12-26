from transformers import pipeline

llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    max_new_tokens=120
)

def call_llm(prompt):
    response = llm(prompt)[0]["generated_text"]
    return response.split("ANSWER:")[-1].strip()


def rag_response(query, df):
    evidence = retrieve_evidence(query, df)

    if not is_answer_allowed(evidence):
        return {
            "status": "REFUSED",
            "reason": "Insufficient evidence",
            "answer": "No relevant past cases found."
        }

    context = build_context(evidence)
    prompt = build_prompt(query, context)

    answer = call_llm(prompt)   

    return {
        "status": "ANSWERED",
        "evidence_used": evidence[["message_text", "category", "similarity"]]
                          .to_dict(orient="records"),
        "answer": answer
    }

rag_response(
    "My order is delayed again",
    df
)

rag_response(
    "Is my credit card hacked?",
    df
)

rag_response(
    "Why was my order delayed due to warehouse fire?",
    df
)

rag_response(
    "Something is wrong",
    df
)
rag_response(
    "My order is delayed again",
    df
)

