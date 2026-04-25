import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from metrics import compute_similarity_scores


def evaluate_system(predictions, ground_truths):
    """
    Evaluate model predictions against ground truths using semantic similarity.
    Returns a list of per-pair scores and the overall average.
    """
    scores = compute_similarity_scores(predictions, ground_truths)
    avg = sum(scores) / len(scores) if scores else 0.0
    return scores, avg


def render_evaluation_ui():
    st.title("🧠 AI Evaluation Lab")
    st.markdown("Evaluate AI answers using semantic similarity.")

    # Input areas
    predictions = st.text_area("Model Predictions (one per line)")
    ground_truths = st.text_area("Ground Truth Answers (one per line)")

    # Run evaluation
    if st.button("Run Evaluation"):
        preds = predictions.strip().split("\n")
        truths = ground_truths.strip().split("\n")

        # Safety check
        if len(preds) != len(truths):
            st.error("Number of predictions and ground truths must match")
        else:
            scores, avg = evaluate_system(preds, truths)

            df = pd.DataFrame({
                "Prediction": preds,
                "Ground Truth": truths,
                "Score": scores
            })

            # Show table
            st.markdown("### 📊 Results")
            st.dataframe(df)

            # Show average score
            st.markdown("### 📈 Average Score")
            st.progress(avg)
            st.success(f"Average Score: {avg:.2f}")

            # Plot chart
            fig, ax = plt.subplots()
            ax.hist(scores, bins=5)
            ax.set_title("Score Distribution")

            st.markdown("### 📉 Score Distribution")
            st.pyplot(fig)