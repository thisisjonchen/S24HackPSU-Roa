FREEZING_TEMP_KELVIN = 273.5
BLACK_ICE_STATUS = 16
DANGER_WIND_SPEED_METERS_SECOND = 13.4
HIGH_WIND_SPEED_METERS_SECOND = 10
VIOLENT_RAIN_RATE_MM_H = 50
HEAVY_RAIN_RATE_MM_H = 7.6
MODERATE_RAIN_RATE_MM_H = 2.5 
LIGHT_RAIN_RATE_MM_H = 0.1
#road_temp, is_black_ice, alert_level, wind_speed, precipitation_rate, speed_limit, alert_name
def is_dangerous(road_temp, is_black_ice, alert_level, alert_name, wind_speed, precipitation_rate, speed_limit):
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

    total_risk+=5*(alert_level/3.0)

    if wind_speed > DANGER_WIND_SPEED_METERS_SECOND:
        flags.append("Too windy")

    if wind_speed > HIGH_WIND_SPEED_METERS_SECOND:
        total_risk+=2

    if precipitation_rate > VIOLENT_RAIN_RATE_MM_H:
        flags.append("Violent rain")

    if precipitation_rate > HEAVY_RAIN_RATE_MM_H:
        total_risk+=8
    elif precipitation_rate > MODERATE_RAIN_RATE_MM_H:
        total_risk+=4
    elif precipitation_rate > LIGHT_RAIN_RATE_MM_H:
        total_risk+=2

    speed_multiplier= speed_limit/35.0
    total_risk = total_risk*speed_multiplier
    confidence = min(((total_risk-8.5)/8.5*100,100))

    if len(flags)>0:
        return flags

    return round(confidence,2)

