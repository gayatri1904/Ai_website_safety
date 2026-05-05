import streamlit as st
import pandas as pd
from src.classifier import WebsiteClassifier
from src.model_trainer import ModelTrainer
import os

# Page Config
st.set_page_config(page_title="AI Website Safety Classifier", page_icon="🛡️", layout="centered")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    .result-card {
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        color: white;
    }
    .safe { background-color: #28a745; }
    .suspicious { background-color: #ffc107; color: black; }
    .scam { background-color: #dc3545; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Website Safety Classifier")
st.markdown("Enter a URL below to check if it's Safe, Suspicious, or a Scam using our AI model.")

# Initialize Classifier
if not os.path.exists('models/rf_model.pkl'):
    with st.spinner("Initializing AI model for the first time..."):
        trainer = ModelTrainer()
        trainer.train()

classifier = WebsiteClassifier()

# User Input
url_input = st.text_input("Enter Website URL:", placeholder="https://example.com")

if st.button("Analyze Website"):
    if url_input:
        with st.spinner("Analyzing URL features..."):
            result = classifier.predict(url_input)
            
            if isinstance(result, dict):
                st.subheader("Analysis Result")
                
                # Dynamic Styling based on result
                class_name = result['classification'].lower()
                st.markdown(f"""
                <div class="result-card {class_name}">
                    <h2 style='text-align: center;'>{result['classification']}</h2>
                    <p style='text-align: center;'>Confidence: {result['confidence']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("### Extracted Features")
                feats = result['features']
                cols = st.columns(3)
                cols[0].metric("URL Length", feats['url_length'])
                cols[1].metric("HTTPS", "Yes" if feats['is_https'] else "No")
                cols[2].metric("Keyword Score", feats['keyword_score'])
                
                with st.expander("View Full Technical Details"):
                    st.json(feats)
            else:
                st.error(result)
    else:
        st.warning("Please enter a valid URL.")

st.sidebar.title("About")
st.sidebar.info("""
This AI system uses a Random Forest model trained on features like:
- Domain Age
- HTTPS Status
- URL Structure
- Content Keyword Analysis
""")
