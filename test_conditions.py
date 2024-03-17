import condition_processing, is_dangerous


if __name__ == '__main__':

    road_temp = 280 #hardcoded number in Kelvin to represent 
    is_black_ice = 0 #0 if little to no chance of black ice, 16 if chance of black ice on road
    alert_level = 3 #number from 0-4 representing the severiety of possible weather condidtions (thunderstorm/tornado)
    wind_speed =  6 #number from 0 to about 15(max) of the current wind speed in m/s
    precipitation_rate = 21 #precipitation in the area in mm/hr
    speed_limit = 45 #speed limit of the road the car is driving on
    alert_name = "" # a string which represents any possible weather condition
    #for getting whether or not the user is in a city
    print(is_dangerous.is_dangerous(road_temp, 
                                            is_black_ice,
                                            alert_level,
                                            alert_name, 
                                            wind_speed, 
                                            precipitation_rate, 
                                            speed_limit))
