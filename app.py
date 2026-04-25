import streamlit as st
import base64
import pandas as pd
import matplotlib.pyplot as plt
from evaluator import evaluate_system
from generator import generate_answer
from retriever import retrieve

# -------------------------------
# SAMPLE TEST CASES
# -------------------------------
test_cases = {
    "High Quality": (
        [
            "RAG improves answers using external knowledge",
            "Hallucination occurs when AI generates unsupported information",
            "Retrieval grounds AI responses in real data"
        ],
        [
            "Retrieval augmented generation improves answer accuracy",
            "Hallucination occurs when models generate unsupported content",
            "Retrieval provides relevant external knowledge"
        ]
    ),

    "Low Quality": (
        [
            "Bananas are blue",
            "The sky is made of water",
            "AI means Apple Icecream"
        ],
        [
            "RAG improves answer accuracy",
            "Hallucination occurs due to lack of grounding",
            "AI stands for artificial intelligence"
        ]
    ),

    "Mixed": (
        [
            "RAG improves answers",
            "AI hallucination is guessing",
            "Retrieval gives context"
        ],
        [
            "Retrieval augmented generation improves accuracy",
            "Hallucination occurs when models generate unsupported content",
            "Retrieval provides external knowledge"
        ]
    )
}

# -------------------------------
# BACKGROUND
# -------------------------------
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_base64 = get_base64_image("assets/background.png")

st.set_page_config(page_title="AI Evaluation Lab", layout="wide")

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: url("data:image/png;base64,{img_base64}") no-repeat center center fixed;
    background-size: cover;
}}

.block-container {{
    background-color: rgba(15, 23, 42, 0.9);
    padding: 2rem;
    border-radius: 12px;
}}

.card {{
    background-color: rgba(30, 41, 59, 0.9);
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 15px;
}}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
st.title("🧠 Verifiable Reasoning Evaluation System")
st.markdown("Evaluate AI answers using semantic similarity and reliability metrics.")

# -------------------------------
# SESSION STATE
# -------------------------------
if "preds" not in st.session_state:
    st.session_state.preds = ""

if "truths" not in st.session_state:
    st.session_state.truths = ""

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("⚙️ Controls")

mode = st.sidebar.selectbox("Mode", ["Manual Input", "Auto Generate (LLM + Retrieval)"])

st.sidebar.markdown("---")
st.sidebar.subheader("🧪 Load Test Case")

selected_case = st.sidebar.selectbox("Select test case", list(test_cases.keys()))

if st.sidebar.button("Load Test Case"):
    preds, truths = test_cases[selected_case]
    st.session_state.preds = "\n".join(preds)
    st.session_state.truths = "\n".join(truths)
    st.rerun()

if st.sidebar.button("Clear Inputs"):
    st.session_state.preds = ""
    st.session_state.truths = ""
    st.rerun()

# -------------------------------
# INPUTS
# -------------------------------
predictions = st.text_area(
    "Model Predictions (one per line)",
    value=st.session_state.preds
)

ground_truths = st.text_area(
    "Ground Truth Answers (one per line)",
    value=st.session_state.truths
)

# -------------------------------
# RUN SYSTEM
# -------------------------------
if st.button("Run Evaluation"):

    if mode == "Manual Input":

        preds = predictions.strip().split("\n")
        truths = ground_truths.strip().split("\n")

    else:
        queries = predictions.strip().split("\n")
        preds = []
        truths = ground_truths.strip().split("\n")

        for q in queries:
            context = retrieve(q)
            answer = generate_answer(q + "\nContext: " + context)
            preds.append(answer)

    # Validation
    if len(preds) != len(truths):
        st.error("Number of predictions and ground truths must match.")
    else:
        scores, avg = evaluate_system(preds, truths)

        df = pd.DataFrame({
            "Prediction": preds,
            "Ground Truth": truths,
            "Score": scores
        })

        st.markdown("### 📊 Results")
        st.dataframe(df)

        st.markdown("### 📈 Average Score")
        st.progress(avg)
        st.success(f"Average Score: {avg:.2f}")

        # Chart
        st.markdown("### 📉 Score Distribution")
        fig, ax = plt.subplots()
        ax.hist(scores, bins=5)
        ax.set_title("Score Distribution")
        st.pyplot(fig)