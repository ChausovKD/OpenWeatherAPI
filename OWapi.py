import json
import requests
import time
from translate import Translator


def get_weather_by_city(city):
    api_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': "8490d0a5fee05ff6087e44f358039bfa",
        'units': "metric",
        'lang': "ru"
    }
    try:
        res = requests.get(api_url, params=params, timeout=0.5)
        data = res.json()
        return [data, res.status_code]
    except ConnectionError:
        print("Ошибка подключения!")
        with open('dataset.json', 'r') as f:
            temp = json.load(f)
            return temp
    except requests.Timeout:
        print("Ошибка времени запроса!")
        with open('dataset.json', 'r') as f:
            temp = json.load(f)
            return temp
    except requests.RequestException:
        print("Глобальная ошибка!")


translator = Translator(from_lang="rus", to_lang="en")
while(True):
    try:
        city_rus = input("Для какого города необходима информация? ")
        city = translator.translate(city_rus)
        timeInterval = int(input("С какой периодичностью обновлять данные (в секундах)? "))
        response = get_weather_by_city(city)
        if(response[1] != 200):
            continue
        result_str = "Текущие показатели погоды в городе {} : {}"
        print(result_str.format(city_rus, response[0]["main"]))
        with open('dataset.json', "w+") as file:
            json.dump(response[0], file)
        with open('dataset.json', 'r') as file:
            temp = json.load(file)
            print(temp)
            time.sleep(timeInterval)
    except KeyboardInterrupt:
        print("Выполнение программы прервано!")
        exit(0)
