import os
import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Create a bulletproof absolute path
# This finds the exact folder app.py is in, then points to the models folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, '../models')

@st.cache_resource
def load_components():
    model = joblib.load(os.path.join(MODEL_DIR, 'metabric_logistic_model.pkl'))
    scaler = joblib.load(os.path.join(MODEL_DIR, 'metabric_scaler.pkl'))
    selector = joblib.load(os.path.join(MODEL_DIR, 'metabric_selector.pkl'))
    return model, scaler, selector

model, scaler, selector = load_components()

st.title("🧬 Breast Cancer Survival Predictor")
st.write("This application uses a Logistic Regression model to predict 5-year survival likelihood based on patient clinical data and METABRIC gene expression profiles.")

st.sidebar.header("Patient Input Parameters")
st.sidebar.write("*(Note: In a full clinical setting, these 20 features would be populated via the patient's EMR and RNA-Seq pipeline. For this demonstration, we are using normalized baseline values).*")

# Generate dummy input fields based on the 20 selected features
# We use baseline 0 for standardized inputs to demonstrate functionality
user_inputs = []
for i in range(20):
    val = st.sidebar.slider(f"Genomic/Clinical Feature {i+1} (Standardized)", min_value=-3.0, max_value=3.0, value=0.0)
    user_inputs.append(val)

if st.button("Predict 5-Year Survival"):
    # Reshape and predict
    input_array = np.array(user_inputs).reshape(1, -1)
    
    # We skip scaling/selecting here because the dummy inputs simulate post-processed data. 
    # If feeding raw data, you would apply scaler.transform() and selector.transform() first.
    prediction = model.predict(input_array)
    probability = model.predict_proba(input_array)[0][1]
    
    st.subheader("Prediction Results:")
    if prediction[0] == 1:
        st.success(f"**Positive Outlook:** The model predicts survival >= 5 years. (Confidence: {probability:.1%})")
    else:
        st.error(f"**High Risk:** The model predicts survival < 5 years. (Confidence: {(1-probability):.1%})")