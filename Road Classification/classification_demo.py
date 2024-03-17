import cv2
import numpy as np
import pyautogui
import time

def select_screen_area():
    print("Please select the screen area for the screenshots...")
    print("Move your mouse to the top-left corner of the area and press Enter.")
    input("Press Enter to continue...")
    x1, y1 = pyautogui.position()
    print(f"Top-left corner selected: ({x1}, {y1})")
    
    print("Move your mouse to the bottom-right corner of the area and press Enter.")
    input("Press Enter to continue...")
    x2, y2 = pyautogui.position()
    print(f"Bottom-right corner selected: ({x2}, {y2})")
    
    return x1, y1, x2, y2

def predict_road_safety(model_path="keras_Model.h5", labels_path="labels.txt"):
    from keras.models import load_model

    # Load the model
    model = load_model(model_path, compile=False)

    # Load the labels
    class_names = open(labels_path, "r").readlines()

    # Select the screen area
    x1, y1, x2, y2 = select_screen_area()

    while True:
        # Take a screenshot of the selected screen area
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
        # Convert the screenshot to an OpenCV image
        image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
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
        # Print the class name and confidence score
        print("Class:", class_name[2:])
        print("Confidence Score:", str(confidence_score))
        # Wait for 1 second before taking the next screenshot
        time.sleep(1)

# Example usage
predict_road_safety()
