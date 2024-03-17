from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.models import load_model
import cv2
import numpy as np

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
with open("labels.txt", "r") as f:
    class_names = [line.strip() for line in f.readlines()]

app = Flask(__name__)
CORS(app)

# Endpoint for uploading an image
@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"})
    
    # Read the image
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    
    # Resize the image
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    
    # Normalize the image array
    image = (image / 255.0)[np.newaxis, ...]
    
    # Predict the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = float(prediction[0][index])
    
    # Format confidence score based on class
    if "Safe" in class_name:
        confidence_score = -1 * np.round(confidence_score, 2)  # Format as a double between -1 and 0 for safe roads
    else:
        confidence_score = np.round(confidence_score, 2)  # Format as a double between 0 and 1 for dangerous roads
    
    return jsonify({"class": class_name, "confidence_score": confidence_score})

if __name__ == "__main__":
    app.run(debug=True)
