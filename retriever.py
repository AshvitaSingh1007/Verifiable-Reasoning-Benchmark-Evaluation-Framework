from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

documents = [
    "RAG improves accuracy by grounding responses in data",
    "Hallucination occurs when models generate unsupported content",
    "Verification ensures reliability of AI systems"
]

def retrieve(query):
    query_emb = model.encode(query, convert_to_tensor=True)
    doc_emb = model.encode(documents, convert_to_tensor=True)

    scores = util.cos_sim(query_emb, doc_emb)[0]

    best_idx = scores.argmax()
    return documents[best_idx]