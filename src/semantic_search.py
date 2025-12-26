def semantic_search(query, top_k=20):
    query_embedding = model.encode([query])
    doc_embeddings = np.vstack(df["embedding"].values)
    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
    df_results = df.copy()
    df_results["similarity"] = similarities
    results = df_results.sort_values("similarity", ascending=False).head(top_k)
    return results

query = "My order came very late again"
results = semantic_search(query)
results[["message_text", "category", "similarity"]]