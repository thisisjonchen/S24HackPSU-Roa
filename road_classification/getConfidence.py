from keras.models import load_model
import cv2
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# Load an image
image_path = "/Users/scottgarciajr/Desktop/road_classification/asphalt-road-into-distance-512212945.jpg"
image = cv2.imread(image_path)

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

# Print prediction and confidence score
if "Safe" in class_name:
    confidence_score = -1 * np.round(confidence_score, 2) # format as a double between -1 and 0 for safe roads
else:
    confidence_score = np.round(confidence_score, 2) # format as a double between 0 and 1 for dangerous roads

print("Class:", class_name[2:])
print("Confidence Score:", str(confidence_score))

