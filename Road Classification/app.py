from flask import Flask, request, jsonify
from keras.models import load_model
import cv2
import numpy as np

app = Flask(__name__)

def load_labels(labels_path):
    with open(labels_path, "r") as f:
        labels = f.readlines()
    return [label.strip() for label in labels]

def predict_road_safety(image):
    # Load the model
    model = load_model("keras_Model.h5", compile=False)

    # Load the labels
    class_names = load_labels("labels.txt")

    # Resize the image
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Make the image a numpy array and reshape it to the model's input shape
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predict the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Format the confidence score based on the class name
    if "Safe" in class_name:
        confidence_score = -1 * np.round(confidence_score, 2)
    else:
        confidence_score = np.round(confidence_score, 2)

    # Return the class name and confidence score
    return class_name[2:], str(confidence_score)

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read the image
        image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        class_name, confidence_score = predict_road_safety(image)
        return jsonify({"class": class_name, "confidence_score": confidence_score})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)
