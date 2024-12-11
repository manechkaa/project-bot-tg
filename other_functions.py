import telebot, string, random
from telebot import types

# отправление рандомного мема
def send_memes():
    count = 79
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
