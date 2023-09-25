import json
import telebot
import requests

bot = telebot.TeleBot('6371717308:AAHMpP8olPnoVUWpxwN5PZcMtd0lQAloJFg')
API = 'bf1250a51aa3a3eae0a3e350c6fbf84d'


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
        if weather == 'Clouds':
            weather = 'Облачно ☁️'
            image = 'Clouds.jpg'
        elif weather == 'Snow':
            weather = 'Снег ❄️'
            image = 'Snow.jpg'
        elif weather == 'Clear':
            weather = 'Ясно 🌤'
            image = 'Clear.jpg'
        elif weather == 'Rain':
            weather = 'Дождь 🌧'
            image = 'Rain.jpg'
        elif weather == 'Sunny':
            weather = 'Солнечно ☀️'
            image = 'Sunny.jpg'
        else:
            weather = None
            image = None
        bot.reply_to(message, f'~Погода в городе {city.capitalize()}~\n\n'
                              f'{weather}\n'
                              f'Текущая температура воздуха: {temp} °C\n'
                              f'Ощущается как: {temp_feel} °C\n'
                              f'Минимальная температура на данный момент: {temp_min}°C\n'
                              f'Максимальная температура на данный момент: {temp_max} °C\n'
                              f'Влажность воздуха: {humidity}%')

        file = open(f'img/{image}', 'rb')
        bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, "Хорошего настроения! ;)")

    else:
        bot.reply_to(message, 'Город указан некорректно')


bot.polling(none_stop=True)
