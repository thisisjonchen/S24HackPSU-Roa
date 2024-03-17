import vehicle_counting
import requests
from time import sleep
from glob import glob

google_api_key = ""
weather_api_key = ""

#INSERT PATH HERE
path = "downloads"

road_temp = 280 #hardcoded number in Kelvin to represent 
is_black_ice = 0 #0 if little to no chance of black ice, 16 if chance of black ice on road
alert_level = 3 #number from 0-4 representing the severiety of possible weather condidtions (thunderstorm/tornado)
wind_speed =  6 #number from 0 to about 15(max) of the current wind speed in m/s
precipitation_rate = 21 #precipitation in the area in mm/hr
speed_limit = 45 #speed limit of the road the car is driving on
alert_name = "" # a string which represents any possible weather condition
#for getting whether or not the user is in a city

def vehicle_num_danger(path: str) -> bool:
        images = glob(path)
        vehicle_count = vehicle_counting.count_vehicles(images)
        if vehicle_count >= 5:
            return True
        else:
            return False

def get_weather_conditions(location: tuple) -> tuple:
    
    url = f"https://api.openweathermap.org/data/2.5/roadrisk?appid={{weather_api_key}}"
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


def get_speed_limit(location: tuple) -> float:
    longitude, latitude = location
    parameters = f"path={longitude}, {latitude}"
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
    
