from evaluator import evaluate_system

def load_data():
    # You can later replace this with file loading
    predictions = [
        "RAG systems use retrieval to improve answers",
        "Hallucination occurs due to missing knowledge"
    ]

    ground_truths = [
        "Retrieval improves grounding of generated answers",
        "Hallucination happens when models generate unsupported content"
    ]

    return predictions, ground_truths


def run_experiment():
    preds, truths = load_data()

    scores, avg = evaluate_system(preds, truths)

    print("\n📊 Evaluation Results")
    print("-" * 40)

    for i, (p, t, s) in enumerate(zip(preds, truths, scores)):
        print(f"\nExample {i+1}")
        print(f"Prediction: {p}")
        print(f"Truth: {t}")
        print(f"Score: {s:.3f}")

    print("\n" + "-" * 40)
    print(f"Average Score: {avg:.3f}")


if __name__ == "__main__":
    run_experiment()