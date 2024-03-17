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
    print("Given the condidtions: \nRoad temp is above freezing \nNo black ice \nHeavy rain \nSpeed limit: 45 \n we get a score of: ",end="")
    print(is_dangerous.is_dangerous(road_temp, 
                                            is_black_ice,
                                            alert_level,
                                            alert_name, 
                                            wind_speed, 
                                            precipitation_rate, 
                                            speed_limit))
    print()
    is_black_ice=16
    print("If we then declare black ice is on the road, we get: ",end="")
    print(is_dangerous.is_dangerous(road_temp, 
                                            is_black_ice,
                                            alert_level,
                                            alert_name, 
                                            wind_speed, 
                                            precipitation_rate, 
                                            speed_limit))
    print()
    speed_limit = 25
    print("If we then decrease the speed limit to 25mph, we get: ",end="")
    print(is_dangerous.is_dangerous(road_temp, 
                                            is_black_ice,
                                            alert_level,
                                            alert_name, 
                                            wind_speed, 
                                            precipitation_rate, 
                                            speed_limit))
    print()
    road_temp = 0
    alert_level = 4
    alert_name = "Earth froze over"
    wind_speed = 13.5
    precipitation_rate = 61
    speed_limit = 35
    print("If the earth freezes over and there's a massive blizzard, we get: ",end="")
    print(is_dangerous.is_dangerous(road_temp, 
                                            is_black_ice,
                                            alert_level,
                                            alert_name, 
                                            wind_speed, 
                                            precipitation_rate, 
                                            speed_limit))
    print()
    road_temp = 280
    alert_level = 0
    alert_name = ""
    wind_speed=0
    precipitation_rate = 0
    speed_limit = 35
    print("When the earth melts back and the weather is clear, we get: ",end="")
    print(is_dangerous.is_dangerous(road_temp, 
                                            is_black_ice,
                                            alert_level,
                                            alert_name, 
                                            wind_speed, 
                                            precipitation_rate, 
                                            speed_limit))
    print()
    precipitation_rate = 1
    print("As we increase the level of rainfall to fall within the 'Light Rain' category, confidence falls to: ",end="")
    print(is_dangerous.is_dangerous(road_temp, 
                                            is_black_ice,
                                            alert_level,
                                            alert_name, 
                                            wind_speed, 
                                            precipitation_rate, 
                                            speed_limit))
    print()
    precipitaion_rate = 3
    print("Then to 'Moderate Rain', confidence falls to: ",end="")
    print(is_dangerous.is_dangerous(road_temp, 
                                            is_black_ice,
                                            alert_level,
                                            alert_name, 
                                            wind_speed, 
                                            precipitation_rate, 
                                            speed_limit))
    print()
    print("Then to 'Heavy Rain', confidence falls to: ",end="")
    print(is_dangerous.is_dangerous(road_temp, 
                                            is_black_ice,
                                            alert_level,
                                            alert_name, 
                                            wind_speed, 
                                            precipitation_rate, 
                                            speed_limit))
