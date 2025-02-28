import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

st.title("Pest Detection Interface")

# Cache the model so it's loaded only once
@st.cache(allow_output_mutation=True)
def load_model():
    model = tf.keras.models.load_model("pest_model.h5")
    return model

model = load_model()

# Define the class names based on your dataset
class_names = ['aphids', 'armyworm', 'beetle', 'bollworm', 'grasshopper', 'mites', 'mosquito', 'sawfly', 'stem_borer']

st.write("Upload an image of a pest to detect:")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open the image file and display it
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Preprocess the image: resize to the size your model expects (225, 225)
    image_resized = image.resize((225, 225))
    image_array = np.array(image_resized)

    # Expand dimensions to match model's input shape (1, 225, 225, 3)
    image_array = np.expand_dims(image_array, axis=0)

    # Optionally, if your training pipeline used normalization, apply it here
    # image_array = image_array / 255.0

    # Get predictions from the model
    predictions = model.predict(image_array)
    predicted_index = np.argmax(predictions)
    predicted_class = class_names[predicted_index]
    confidence = np.max(predictions)

    st.write(f"**Prediction:** {predicted_class}")
    st.write(f"**Confidence:** {confidence:.2f}")
