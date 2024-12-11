import telebot, string, random
from telebot import types


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
def randomword(length):
    letters = string.ascii_lowercase
    ans = ''.join(random.choice(letters) for i in range(length))
    return ans
