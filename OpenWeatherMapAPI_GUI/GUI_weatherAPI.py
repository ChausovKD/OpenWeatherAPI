from tkinter import *
import tkinter.messagebox as mb
import time
import threading
import json
import requests


def get_weather_by_city():
    try:
        city_name = cityField_ent.get()
        api_url = "http://api.openweathermap.org/data/2.5/weather"

        params = {
            'q': city_name,
            'appid': "8490d0a5fee05ff6087e44f358039bfa",
            'units': "metric",
            'lang': "ru"
        }

        res = requests.get(api_url, params=params, timeout=0.5)
        data = res.json()
        response = [data, res.status_code]
        if response[1] == 200:
            with open('dataset.json', "w+") as file:
                json.dump(response[0], file)
                return response
        else:
            msg = "Некорректный запрос!"
            mb.showinfo("Информация", msg)
            root.destroy()
    except requests.Timeout:
        msg = "Превышен лимит времени ожидания ответа!"
        mb.showinfo("Информация", msg)
        root.destroy()
    except requests.RequestException:
        print("Глобальная ошибка!")
        root.destroy()
    except KeyboardInterrupt:
        print("Выполнение программы прервано!")
        root.destroy()


def create_plots_data(data):
    plots_data_lists['temperature_real'].add(data[0]['main']['temp'])
    plots_data_lists['temperature_felt'].add(data[0]['main']['feels_like'])
    plots_data_lists['humidity'].add(data[0]['main']['humidity'])
    plots_data_lists['weather_description'].add(data[0]['weather'][0]['description'])
    plots_data_lists['visibility'].add(data[0]['visibility'])
    plots_data_lists['wind_speed'].add(data[0]['wind']['speed'])
    return plots_data_lists


def get_with_interval():
    timeInterval = int(timeInterval_ent.get()) * 1000
    temp = get_weather_by_city()
    if temp[1] != 200:
        exit(0)
    output_of_received_information(temp)
    root.after(timeInterval, get_with_interval)


def get_current_time():
    current_time = time.strftime("%H:%M:%S")
    clock.config(text="Текущее время: " + current_time)
    clock.after(200, get_current_time)


def clearing_input_fields_labels(event):
    cityField_ent.delete(0, 'end')
    timeInterval_ent.delete(0, 'end')
    tempText_1.config(text="")
    tempText_2.config(text="")
    timeDataReceipt.config(text="")
    cityField_ent.focus_set()


def output_of_received_information(data):
    information_output_temp_real = data[0]['main']['temp']
    information_output_temp_feel = data[0]['main']['feels_like']
    information_output_humidity = data[0]['main']['humidity']
    information_output_weather_description = data[0]['weather'][0]['description']
    information_output_temp_visibility = data[0]['visibility']
    information_output_temp_wind_speed = data[0]['wind']['speed']
    timeDataReceipt.config(text="Время получения данных: " + time.strftime("%H:%M:%S") + ":")
    tempText_1.config(text="Температура: " + str(information_output_temp_real) + u"\u00b0C" + "\n\n" +
                    "Ощущаемая температура: " + str(information_output_temp_feel) + u"\u00b0C" + "\n\n" +
                    "Влажность: " + str(information_output_humidity) + "%")
    tempText_2.config(text="Состояние погоды: " + str(information_output_weather_description) + "\n\n" +
                         "Видимость: " + str(information_output_temp_visibility) + " метров" + "\n\n" +
                         "Скорость ветра: " + str(information_output_temp_wind_speed) + "м/с")


plots_data_lists = {
        'temperature_real': set(),
        'temperature_felt': set(),
        'humidity': set(),
        'weather_description': set(),
        'visibility': set(),
        'wind_speed': set(),
}

root = Tk()
root.title("Прогноз погоды")
root.iconbitmap("1.ico")
root.geometry('600x500')
root.resizable(width=False, height=False)

labels = [
    "Название города:",
    "Временной интервал (в сек.):",
    "Текущее время:"
]

frame_entry_1 = Frame(root, bd=5)
frame_entry_1.place(rely=0.09, relx=0.58, relwidth=0.4)

frame_entry_2 = Frame(root, bd=5)
frame_entry_2.place(rely=0.29, relx=0.58, relwidth=0.4)

frame_buttons = Frame(root, bd=5)
frame_buttons.place(rely=0.88, relx=0, relwidth=1)

frame_labels = Frame(root, bd=1)
frame_labels .place(rely=0.1, relx=0.025, relwidth=0.53, relheight=0.255)

frame_clock = Frame(root, bd=5)
frame_clock.place(rely=0.40, relx=0, relwidth=1)

frame_information_output = Frame(root, bd=5)
frame_information_output.place(rely=0.525, relx=0.05, relwidth=0.9, relheight=0.32)

cityField_ent = Entry(frame_entry_1, bg='white', font=("Arial Bold", 15), bd=2)
cityField_ent.pack()

timeInterval_ent = Entry(frame_entry_2, bg='white', font=("Arial Bold", 15), bd=2)
timeInterval_ent.pack()

btn_submit = Button(frame_buttons, text='Запрос', font=("Arial Bold", 15), bd=5, command=lambda: threading.Thread(target=get_with_interval, daemon=True).start())
btn_submit.pack(side=RIGHT, padx=15, ipadx=15)

btn_clear = Button(frame_buttons, text='Очистить', font=("Arial Bold", 15), bd=5)
btn_clear.bind("<Button-1>", clearing_input_fields_labels)
btn_clear.pack(side=LEFT, padx=15, ipadx=15)


label_1 = Label(frame_labels, text=labels[0], font=40)
label_1.pack(side=TOP)

label_2 = Label(frame_labels, text=labels[1], font=40)
label_2.pack(side=BOTTOM)

clock = Label(frame_clock, font=20)
clock.pack(side=BOTTOM)
get_current_time()

timeDataReceipt = Label(frame_information_output, font=20)
timeDataReceipt.pack(side=TOP)

tempText_1 = Label(frame_information_output, font=20)
tempText_1.pack(side=LEFT)

tempText_2 = Label(frame_information_output, font=20)
tempText_2.pack(side=RIGHT)

try:
    root.mainloop()
except KeyboardInterrupt:
    print("Выполнение программы прервано!")
