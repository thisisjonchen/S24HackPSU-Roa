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
precipitation_rate = 51 #precipitation in the area in mm/hr
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
    

FREEZING_TEMP_KELVIN = 273.5
BLACK_ICE_STATUS = 16
DANGER_WIND_SPEED_METERS_SECOND = 13.4
HIGH_WIND_SPEED_METERS_SECOND = 10
VIOLENT_RAIN_RATE_MM_H = 50
HEAVY_RAIN_RATE_MM_H = 7.6
MODERATE_RAIN_RATE_MM_H = 2.5 
LIGHT_RAIN_RATE_MM_H = 0.1
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
    if road_temp<FREEZING_TEMP_KELVIN: #if road temp if below freezing, add to total risk based on decision matrix in documentation
        total_risk+=2

    if is_black_ice == BLACK_ICE_STATUS: 

        flags.append("Icy roads")
    if alert_level == 4:
        flags.append(alert_name)
    else:
        total_risk+=5*(alert_level/3.0)

    if wind_speed > DANGER_WIND_SPEED_METERS_SECOND:
        flags.append("Too windy")
        
    elif wind_speed > HIGH_WIND_SPEED_METERS_SECOND:
        total_risk+=2
    if precipitation_rate > VIOLENT_RAIN_RATE_MM_H:
        flags.append("Violent rain")
    elif precipitation_rate > HEAVY_RAIN_RATE_MM_H:
        total_risk+=8
    elif precipitation_rate > MODERATE_RAIN_RATE_MM_H:
        total_risk+=4
    elif precipitation_rate > LIGHT_RAIN_RATE_MM_H:
        total_risk+=2

    speed_multiplier= speed_limit/35.0
    total_risk = total_risk*speed_multiplier
    confidence = min(abs((total_risk-8.5)/8.5)*100,100)

    if len(flags)>0:
        return flags

    return confidence

if __name__ == '__main__':
    pass
