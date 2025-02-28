import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("mdl_crv1.pkl")

# Patch the model by setting the missing attribute for each estimator
if hasattr(model, 'estimators_'):
    for estimator in model.estimators_:
        if not hasattr(estimator, 'monotonic_cst'):
            setattr(estimator, 'monotonic_cst', None)

# Crop mapping dictionary
crop_dict = {
    0: 'rice', 1: 'maize', 2: 'chickpea', 3: 'kidneybeans', 4: 'pigeonpeas',
    5: 'mothbeans', 6: 'mungbean', 7: 'blackgram', 8: 'lentil', 9: 'pomegranate',
    10: 'banana', 11: 'mango', 12: 'grapes', 13: 'watermelon', 14: 'muskmelon',
    15: 'apple', 16: 'orange', 17: 'papaya', 18: 'coconut', 19: 'cotton',
    20: 'jute', 21: 'coffee'
}

# Streamlit UI
st.title("Crop Prediction System")
st.write("Enter the required parameters to predict the best crop.")

# User input fields
N = st.number_input("Nitrogen (N)", min_value=0.0, step=0.1)
P = st.number_input("Phosphorus (P)", min_value=0.0, step=0.1)
K = st.number_input("Potassium (K)", min_value=0.0, step=0.1)
temperature = st.number_input("Temperature (°C)", min_value=-10.0, step=0.1)
humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, step=0.1)
ph = st.number_input("pH Level", min_value=0.0, max_value=14.0, step=0.1)
rainfall = st.number_input("Rainfall (mm)", min_value=0.0, step=0.1)

# Predict button
if st.button("Predict Crop"):
    # Prepare input data
    input_data = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]],
                              columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])
    
    # Make prediction
    prediction = model.predict(input_data)[0]
    predicted_crop = crop_dict.get(prediction, "Unknown Crop")
    
    # Display result
    st.success(f"The recommended crop is: **{predicted_crop}**")
