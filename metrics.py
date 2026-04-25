from sentence_transformers import SentenceTransformer, util

# Load model once (important for performance)
model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_score(prediction, truth):
    """
    Computes semantic similarity between a single prediction and ground truth.
    Returns a float between -1 and 1.
    """
    emb1 = model.encode(prediction, convert_to_tensor=True)
    emb2 = model.encode(truth, convert_to_tensor=True)
    score = util.cos_sim(emb1, emb2)
    return float(score)


def compute_similarity_scores(predictions, ground_truths):
    """
    Computes semantic similarity scores for a list of prediction/truth pairs.
    Returns a list of floats.
    """
    return [semantic_score(p, t) for p, t in zip(predictions, ground_truths)]