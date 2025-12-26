from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

texts = df["message_text"].tolist()
embeddings = model.encode(texts)

print(embeddings.shape)
df["embedding"] = list(embeddings)
df