import telebot
from telebot import types
import requests
from datetime import datetime

bot = telebot.TeleBot('1841051566:AAGKCVQ-1af1mUEQb7SV5CVyV3lza_YD4O4')

apiKey = 'e0636036b19462072b12cd7c047c2aa8'
url = 'https://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&appid={1}'
requestResult = ''
city = ''
keyboard = types.InlineKeyboardMarkup()
keyboard.add(types.InlineKeyboardButton("Получить информацию о боте \U0001F4CB", callback_data="infoAboutBot"))
keyboard.add(types.InlineKeyboardButton("Как пользоваться ботом ? \U0001F4A1", callback_data="howUseBot"))


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEBfbZg1yMGbMgQQwgzPTY5NQ5arfunuAACAQEAAladvQoivp8OuMLmNCAE")
    bot.send_message(message.chat.id, "Добро пожаловать, {0} ! \U0001F497\n".format(message.chat.first_name))
    bot.send_message(message.chat.id, "Здесь вы сможете узнать любую информацию о погоде. "
                                      "Просто введите название города.\n")
    bot.send_message(message.chat.id, "Для получения дополнительной информации напишите /help в сообщении.")


@bot.message_handler(commands=['help'])
def help_message(message):
    global keyboard
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAPxYNhPrkGvofrBmwRoy5KeW_j7G5cAAgUDAAJWnb0K65csNotQOoYgBA")
    bot.send_message(message.chat.id, "Здравствуйте! Что вы хотите узнать?", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    global requestResult, city, keyboard
    requestResult = requests.get(url.format(message.text, apiKey)).json()
    if (requestResult["cod"] == 200):
        city = message.text
        cityInfo = "Краткая информация о погоде в г. {0} на текущий момент времени \U0001F30D:\n\n" \
                   "Температура: {1} \u2103\n" \
                   "Атмосферное давление: {2} гПа\n" \
                   "Влажность воздуха: {3} %\n" \
                   "Скорость ветра: {4} м/с^2\n" \
                   "Облачность: {5} %\n".format(message.text, requestResult["main"]["temp"],
                                                requestResult["main"]["pressure"], requestResult["main"]["humidity"],
                                                requestResult["wind"]["speed"], requestResult["clouds"]["all"])

        keyboard = types.InlineKeyboardMarkup()
        additingInfoButton = types.InlineKeyboardButton(text='Получить дополнительную информацию о погоде',
                                                        callback_data='additingInfo')
        keyboard.add(additingInfoButton)

        bot.send_message(message.chat.id, cityInfo, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Информация о погоде в данном городе не найдена \U0001F622 ! Попробуйте снова!",
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global requestResult, city
    if call.data == "additingInfo":
        keyboard = types.InlineKeyboardMarkup()
        windDegInfoButton = types.InlineKeyboardButton(text='Направление ветра', callback_data='windDegInfo')
        windGustInfoButton = types.InlineKeyboardButton(text='Порыв ветра', callback_data='windGustInfo')
        sysSunriseInfoButton = types.InlineKeyboardButton(text='Время восхода', callback_data='sysSunriseInfo')
        sysSunsetInfoButton = types.InlineKeyboardButton(text='Время заката', callback_data='sysSunsetInfo')
        keyboard.add(windDegInfoButton, windGustInfoButton, sysSunriseInfoButton,
                     sysSunsetInfoButton)
        bot.send_message(call.message.chat.id, "Дополнительная информация:", reply_markup=keyboard)
    elif call.data == "windDegInfo":
        bot.send_message(call.message.chat.id,
                         "Направление ветра в г. {0}: {1}".format(city, requestResult["wind"]["deg"]))
    elif call.data == "windGustInfo":
        bot.send_message(call.message.chat.id,
                         "Порыв ветра в г. {0}: {1} м/с".format(city, requestResult["wind"]["gust"]))
    elif call.data == "sysSunriseInfo":
        bot.send_message(call.message.chat.id,
                         "Время восхода в г. {0}: {1}".
                         format(city, datetime.utcfromtimestamp(int(requestResult["sys"]["sunrise"])).
                                strftime('%Y-%m-%d %H:%M:%S')))
    elif call.data == "sysSunsetInfo":
        bot.send_message(call.message.chat.id,
                         "Время заката в г. {0}: {1}".
                         format(city, datetime.utcfromtimestamp(int(requestResult["sys"]["sunset"])).
                                strftime('%Y-%m-%d %H:%M:%S')))
    elif call.data == "infoAboutBot":
        bot.send_message(call.message.chat.id, "Инфорамация о боте:\n\n"\
                         "Данный бот позволяет получить информацию о погоде в текущий момент времени.\n"\
                         "В реализации бота использовалась технология API.\n"\
                         "Создатель: Силантьев А.Р. УлГТУ 2021\n")
    elif call.data == "howUseBot":
        bot.send_message(call.message.chat.id, "Как пользоваться ботом ?\n\n"\
                         "Необходимо просто ввести название нужного города на русском или английском языке.\n"\
                         "Далее бот отобразит все данные в виде сообщения.\n"\
                         "Имеется возможность получать дополнительную информацию о погоде, использую вспомогательные "
                                               "кнопки.\n"\
                         "Если введенный город не будет найден, бот сообщит об этом в сообщении.\n")


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message.sticker.file_id)


bot.polling(none_stop=True, interval=0)
