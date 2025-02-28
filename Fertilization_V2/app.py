import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load the pre-trained RandomForestClassifier model
model = joblib.load('mdl_fr_v5.pkl')

# Define mapping dictionaries for categorical inputs
soil_dict = {'Clayey': 0, 'Loamy': 1, 'Red': 2, 'Black': 3, 'Sandy': 4}
crop_dict = {
    'rice': 0,
    'Wheat': 1,
    'Tobacco': 2,
    'Sugarcane': 3,
    'Pulses': 4,
    'pomegranate': 5,
    'Paddy': 6,
    'Oil seeds': 7,
    'Millets': 8,
    'Maize': 9,
    'Ground Nuts': 10,
    'Cotton': 11,
    'coffee': 12,
    'watermelon': 13,
    'Barley': 14,
    'kidneybeans': 15,
    'orange': 16
}

# Define the fertilizer mapping (target variable encoding)
fertilizer_dict = {
    'Urea': 0,
    'TSP': 1,
    'Superphosphate': 2,
    'Potassium sulfate.': 3,
    'Potassium chloride': 4,
    'DAP': 5,
    '28-28': 6,
    '20-20': 7,
    '17-17-17': 8,
    '15-15-15': 9,
    '14-35-14': 10,
    '14-14-14': 11,
    '10-26-26': 12,
    '10-10-10': 13
}

# Inverse mapping to convert numeric prediction back to fertilizer name
inv_fertilizer_dict = {v: k for k, v in fertilizer_dict.items()}

# Define feature names (ensure order matches model training)
feature_names = np.array(['Temparature', 'Humidity', 'Moisture', 'Soil_Type', 'Crop_Type',
                           'Nitrogen', 'Potassium', 'Phosphorous'])

# App title and instructions
st.title("Fertilizer Recommendation")
st.write("Enter the following details to get a fertilizer recommendation:")

# Input fields for numeric features
temperature = st.number_input("Temparature", min_value=0.0, value=26.0)
humidity = st.number_input("Humidity", min_value=0.0, max_value=100.0, value=82.0)
moisture = st.number_input("Moisture", min_value=0.0, value=25.0)
nitrogen = st.number_input("Nitrogen", min_value=0.0, value=86.0)
potassium = st.number_input("Potassium", min_value=0.0, value=41.0)
phosphorous = st.number_input("Phosphorous", min_value=0.0, value=36.0)

# Dropdowns for categorical features
soil_type = st.selectbox("Soil Type", options=list(soil_dict.keys()))
crop_type = st.selectbox("Crop Type", options=list(crop_dict.keys()))

# Map the categorical inputs to their corresponding numeric values
soil_type_val = soil_dict[soil_type]
crop_type_val = crop_dict[crop_type]

# Create a DataFrame with a single row of input values in the correct order
input_data = pd.DataFrame([[temperature, humidity, moisture, soil_type_val, crop_type_val,
                            nitrogen, potassium, phosphorous]], columns=feature_names)

# When the "Predict Fertilizer" button is clicked, make the prediction and display the result
if st.button("Predict Fertilizer"):
    prediction = model.predict(input_data)
    predicted_fertilizer = inv_fertilizer_dict.get(prediction[0], "Unknown")
    st.success(f"Recommended Fertilizer: {predicted_fertilizer}")
