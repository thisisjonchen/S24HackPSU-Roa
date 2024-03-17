road_temp = 280 #hardcoded number in Kelvin to represent 
is_black_ice = 0 #0 if little to no chance of black ice, 16 if chance of black ice on road
alert_level = 3 #number from 0-4 representing the severiety of possible weather condidtions (thunderstorm/tornado)
wind_speed =  6 #number from 0 to about 15(max) of the current wind speed in m/s
precipitation_rate = 20 #precipitation in the area in mm/hr
speed_limit = 45 #speed limit of the road the car is driving on
alert_name = "" # a string which represents any possible weather condition

def is_dangerous(road_temp, is_black_ice, alert_level, wind_speed, precipitation_rate, speed_limit, alert_name):
    total_risk = 0 #total value of rankings from conditions
    flags = [] #collection of reasons why the condition was automatically flagged
    if road_temp<273.5: #if road temp if below freezing, add to total risk based on decision matrix in documentation
        total_risk+=2
    if is_black_ice == 16: 
        flags.append("Icy roads")
    if alert_level == 4:
        flags.append(alert_name)
    else:
        total_risk+=5*(alert_level/3.0)
    if wind_speed > 13.4:
        flags.append("Too windy")
    elif wind_speed >10:
        total_risk+=2
    if precipitation_rate>50:
        flags.append("Violent rain")
    elif precipitation_rate>7.6:
        total_risk+=8
    elif precipitation_rate>2.5:
        total_risk+=4
    elif precipitation_rate>.1:
        total_risk+=2
    speed_multiplier= speed_limit/35.0
    total_risk = total_risk*speed_multiplier
    confidence = min(abs((total_risk-8.5)/8.5)*100,100)
    if len(flags)>0:
        return flags
    return confidence