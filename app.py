import vehicle_counting
import requests 
from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.models import load_model
import cv2
import numpy as np
from openai import OpenAI

app = Flask(__name__)

google_api_key = ""
weather_api_key = ""

#INSERT PATH HERE

road_temp = 280 #hardcoded number in Kelvin to represent 
is_black_ice = 0 #0 if little to no chance of black ice, 16 if chance of black ice on road
alert_level = 3 #number from 0-4 representing the severiety of possible weather condidtions (thunderstorm/tornado)
wind_speed =  6 #number from 0 to about 15(max) of the current wind speed in m/s
precipitation_rate = 21 #precipitation in the area in mm/hr
speed_limit = 45 #speed limit of the road the car is driving on
alert_name = "" # a string which represents any possible weather condition
#for getting whether or not the user is in a city

def vehicle_num_danger(image: str) -> bool:
        vehicle_count = vehicle_counting.count_vehicles(image)
        if vehicle_count >= 5:
            return True
        else:
            return False

@app.route('/get_data')
def get_data():
    data = {'latitude': -1, 'longitude': -1}
    return jsonify(data)

def get_weather_conditions():
    location_data_response = get_data()
    location_data = location_data_response.get_json()
    lon = location_data['longitude']
    lat = location_data['latitude']

    url = f"https://api.openweathermap.org/data/2.5/roadrisk?appid={weather_api_key}&lat={lat}&lon={lon}"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    else:
        print("Reponse failed with status code", response.status_code)
    data = response.json()

    precipitation_rate = data['weather']['precipitation_intensity']
    road_temp = data['road']['temp']
    is_black_ice = data['road']['state']
    alert_level = data['alerts']['event']
    alert_name = data['alerts']['name']
    wind_speed  = data['weather']['wind_speed']
    print(f"""DEBUG: rain: {precipitation_rate}
          black_ice: {is_black_ice}
          alert_level: {alert_level}
          road_temp: {road_temp}
          alert_name: {alert_name}
          wind_speed: {wind_speed}
    """)

def get_speed_limit():
    location_data_response = get_data()
    location_data = location_data_response.get_json()
    longitude = location_data['longitude']
    latitude = location_data['latitude']
    
    parameters = f"path={latitude}, {longitude}"
    url = f"https://roads.googleapis.com/v1/speedLimits?{parameters}&key={{google_api_key2}}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    else:
        print("Reponse failed with status code", response.status_code)
    data = response.json()
    
    speedlimit = data['speedLimits']['speedlimit']
    print(f"""DEBUG: rain: {precipitation_rate}
          black_ice: {is_black_ice}
          alert_level: {alert_level}
          road_temp: {road_temp}
          alert_name: {alert_name}
          wind_speed: {wind_speed}
    """)

#calculators to determine weather conditions    
FREEZING_TEMP_KELVIN = 273.5
BLACK_ICE_STATUS = 16
DANGER_WIND_SPEED_METERS_SECOND = 13.4
HIGH_WIND_SPEED_METERS_SECOND = 10
VIOLENT_RAIN_RATE_MM_H = 50
HEAVY_RAIN_RATE_MM_H = 7.6
MODERATE_RAIN_RATE_MM_H = 2.5 
LIGHT_RAIN_RATE_MM_H = 0.1
SPEED_LIMIT_RISK_FACTOR = 56.327
#road_temp, is_black_ice, alert_level, wind_speed, precipitation_rate, speed_limit, alert_name
def is_dangerous():
    """
    returns either a List (flags) or float (confidence meter)
    flags is used whenever weather is bad enough so that the user should take immediate caution (i.e when black ice occurs)
    a positive confidence level indicates that conditions can be potentially unsafe
    a negative confidence level indicates that conditions are more safe
    """
    total_risk = 0 #total value of rankings from conditions
    flags = [] #collection of reasons why the condition was automatically flagged
    if road_temp < FREEZING_TEMP_KELVIN: #if road temp if below freezing, add to total risk based on decision matrix in documentation
        total_risk += 2

    if is_black_ice == BLACK_ICE_STATUS: 
        flags.append("Icy roads")

    if alert_level == 4:
        flags.append(alert_name)

    total_risk += 5 * (alert_level / 3.0)

    if wind_speed > DANGER_WIND_SPEED_METERS_SECOND:
        flags.append("Too windy")

    if wind_speed > HIGH_WIND_SPEED_METERS_SECOND:
        total_risk+=2

    if precipitation_rate > VIOLENT_RAIN_RATE_MM_H:
        flags.append("Violent rain")

    if precipitation_rate > HEAVY_RAIN_RATE_MM_H:
        total_risk += 8
    elif precipitation_rate > MODERATE_RAIN_RATE_MM_H:
        total_risk += 4
    elif precipitation_rate > LIGHT_RAIN_RATE_MM_H:
        total_risk += 2

    speed_multiplier = speed_limit/SPEED_LIMIT_RISK_FACTOR
    total_risk = total_risk * speed_multiplier
    confidence = min(((total_risk - 8.5) / 8.5 * 100, 100))

    if len(flags) > 0:
        return flags, confidence #this is temporary

    return confidence

lastConfidenceScore = 0

#image detection algorithm
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
        confidence_score = -100 * np.round(confidence_score, 2)
    else:
        confidence_score = np.round(confidence_score, 2) * 100
    #last_Confidence_score = confidence_score #to use globally for stuff
    # Return the class name and confidence score
    return class_name[2:], str(confidence_score)


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
    return confidence_score #to use globally for stuff
    # Return the class name and confidence score

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

our_output = is_dangerous() #our confidence
their_output = lastConfidenceScore #their confidence
@app.route("/give_result", methods=["POST"])
def give_result():
    client = OpenAI(api_key = "API_KEY_HERE")

    # our_output = ["too windy, thunderstorm"] #our confidence
    # their_output = 10 #their confidence
    message = "write a message with confidence of "

    if isinstance(our_output,list):
        confidence = (100+their_output)/2.0
        message+= str(confidence)+" with the reason being due to "
        for reason in our_output:
            message+=str(reason)+", "

    else:
        confidence = (our_output+their_output)/2.0
        message+=str(confidence)


    if(confidence>0):
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are writing a message to someone currently driving a car to alert the driver that the road situation they are in looks like a situation in which a crash has either happened or is likely to happen.  The message should only be a few words long and does not need to have proper grammar. I will provide a confidence level for your response on a scale of 0-100. A response with higher confidence should be more assertive and urgent, while a message with low confidence should be a weaker, less stressed recommendation. An example of a message with high confidence is 'URGENT, DRIVE SAFE' while an example for a message with low confidence is 'caution.'"
                },
                {
                    "role": "user",
                    "content": message,
                }
            ],
            model="gpt-3.5-turbo",
        )

    response = {
        'confidence': confidence,
        'message': chat_completion.choices[0].message.content
    }

    return jsonify(response)
        



if __name__ == '__main__':
    app.run(debug=True)
    # print(give_result())
