import streamlit as st
import tensorflow as tf
import numpy as np

# Define your class labels (38 classes)
class_labels = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)_Powdery_mildew',
    'Cherry_(including_sour)_healthy',
    'Corn_(maize)_Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)Common_rust',
    'Corn_(maize)_Northern_Leaf_Blight',
    'Corn_(maize)_healthy',
    'Grape___Black_rot',
    'Grape__Esca(Black_Measles)',
    'Grape__Leaf_blight(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange__Haunglongbing(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,bell__Bacterial_spot',
    'Pepper,bell__healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

# Cache the model loading so it's done only once per session
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("model.h5")

model = load_model()

st.title("Plant Disease Detection")
st.write("Upload an image of a plant leaf to detect the disease.")

# File uploader widget for image input
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Use tf.keras.preprocessing.image.load_img to load and resize the image
    image = tf.keras.preprocessing.image.load_img(uploaded_file, target_size=(128, 128))
    
    # Display the uploaded image
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Convert the image to an array using img_to_array
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    # Convert single image to a batch by adding an extra dimension
    input_arr = np.expand_dims(input_arr, axis=0)
    
    # Optional: Display input shape for debugging
    st.write("Input shape:", input_arr.shape)
    
    # Make a prediction using the loaded model
    predictions = model.predict(input_arr)
    st.write("Raw predictions:", predictions)  # Debug output of probabilities
    
    predicted_index = np.argmax(predictions, axis=1)[0]
    predicted_class = class_labels[predicted_index]
    
    st.write("### Prediction:")
    st.write(f"**{predicted_class}**")
