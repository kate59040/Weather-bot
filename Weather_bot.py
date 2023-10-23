import json
import telebot
import requests

bot = telebot.TeleBot('///')
API = '\\\'


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Доброго времени суток:)\nНапишите мне название города, где вы проживаете или "
                                      "каким городом интересуетесь, и я пришлю вам актуальную информацию о погоде :3")


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")

    if res.status_code == 200:
        data = json.loads(res.text)
        temp = round(data["main"]["temp"])
        temp_feel = round(data["main"]["feels_like"])
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["main"]
        weather_img_dict = {'Clouds': ['Облачно ☁️', 'Clouds.jpg'], 'Snow': ['Снег ❄️', 'Snow.jpg'],
                            'Clear': ['Ясно 🌤', 'Clear.jpg'], 'Rain': ['Дождь 🌧', 'Rain.jpg'],
                            'Sunny': ['Солнечно ☀️', 'Sunny.jpg']}

        bot.reply_to(message, f'~Погода в городе {city.capitalize()}~\n\n'
                              f'{weather_img_dict[weather][0]}\n'
                              f'Текущая температура воздуха: {temp} °C\n'
                              f'Ощущается как: {temp_feel} °C\n'
                              f'Минимальная температура на данный момент: {temp_min}°C\n'
                              f'Максимальная температура на данный момент: {temp_max} °C\n'
                              f'Влажность воздуха: {humidity}%')

        file = open(f'img/{(weather_img_dict[weather][1])}', 'rb')
        bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, "Хорошего настроения! ;)")

    else:
        bot.reply_to(message, 'Город указан некорректно')


bot.polling(none_stop=True)
