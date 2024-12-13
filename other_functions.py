import telebot, string, random
from telebot import types

#кидает ссылки на полезные сайты
def more_information(bot, message):
    markup = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton("google", url='https://www.google.com/')
    button2 = types.InlineKeyboardButton("Moodle", url='https://newlms.misis.ru/login/index.php')
    button3 = types.InlineKeyboardButton("Калькулятор матриц", url='https://matrixcalc.org/ru/')
    button4 = types.InlineKeyboardButton("Графический калькулятор", url='https://www.geogebra.org/graphing?lang=ru')
    button5 = types.InlineKeyboardButton("Вольфрам", url='https://www.wolframalpha.com/')
    button6 = types.InlineKeyboardButton("MathDF", url='https://mathdf.com/ru/')
    button7 = types.InlineKeyboardButton("ChatGPT", url='https://trychatgpt.ru/')

    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    markup.add(button4)
    markup.add(button5)
    markup.add(button6)
    markup.add(button7)

    bot.send_message(message.chat.id, "Это может помочь в учебе".format(message.from_user), reply_markup=markup)

#кидает ссылку на упражнение для глаз и спины
def exercises(bot, message):
    markup = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton("Разминка для глаз", url='https://www.youtube.com/watch?v=mqXR8O2VJLo')
    button2 = types.InlineKeyboardButton("Разминка для спины", url='https://www.youtube.com/watch?v=rmXW0A2abSw')

    markup.add(button1)
    markup.add(button2)

    bot.send_message(message.chat.id, "Это будет полезно!".format(message.from_user), reply_markup=markup)

# отправление рандомного мема
def send_memes(bot, message):
    count = 79
    rnd = random.randint(1, 10)
    if rnd == 1:
        exercises(bot, message)
    num = random.randint(1, count)
    photo = open("memes_photo/memes" + str(num) + ".jpg", 'rb')
    return photo

#отправление песни для учебы
def send_playlist(bot, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    count = 11
    rnd = random.randint(1, count - 4)
    for i in range(5):
        num = rnd + i
        playlist = open("songs/playlist" + str(num) + ".mp3", 'rb')
        bot.send_audio(message.chat.id, playlist, reply_markup=markup)


# генерация рандомного имени для фото
def randomword(length) -> str:
    letters = string.ascii_lowercase
    ans = ''.join(random.choice(letters) for i in range(length))
    return ans
