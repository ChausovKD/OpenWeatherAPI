import time
import json
import requests


def get_weather_by_city(city):
    api_url = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        'q': city,
        'appid': "8490d0a5fee05ff6087e44f358039bfa",
        'units': "metric",
        'lang' : "ru"
    }

    res = requests.get(api_url, params=params)
    data = res.json()
    return data


city = input("Для какого города необходима информация? ")
timeInterval = int(input("С какой периодичностью обновлять данные (в секундах)? "))
while(True):
    response = get_weather_by_city(city)
    result_str = "Текущие показатели погоды в {}: {}"
    print(result_str.format(city, response["main"]))
    with open('dataset.json', "w+") as file:
        json.dump(response, file)
    with open('dataset.json', 'r') as file:
        temp = json.load(file)
        print(temp)
    time.sleep(180)
