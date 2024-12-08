import telebot, string, random
import json
import os
import sys
import datetime
import pytz
import random
import requests
from telebot import types
from datetime import date

token = open('file_token.txt').read()
bot = telebot.TeleBot(token)
print("Bot is online.")

homework = json.loads(open('./jsons/homeworks.json', 'r', encoding='utf-8').read())
user_state = json.loads(open('./jsons/users_states.json', 'r', encoding='utf-8').read())
helper = json.loads(open('./jsons/edithw.json', 'r', encoding='utf-8').read())

# отправление рандомного мема
def send_memes():
    count = 79
    num = random.randint(1, count)
    photo = open("memes_photo/memes" + str(num) + ".jpg", 'rb')
    return photo

#отправление песни для учебы
def send_playlist():
    count = 2
    num = random.randint(1, count)
    playlist = open("songs/playlist" + str(num) + ".mp3", 'rb')
    return playlist

# генерация рандомного имени для фото
def randomword(length):
    letters = string.ascii_lowercase
    ans = ''.join(random.choice(letters) for i in range(length))
    return ans

# получение даты по номеру дня
def get_day_by_number(number):  # 0 - вс
    current_time = datetime.datetime.today()
    weekday = current_time.weekday()
    day = "";
    month = "";
    year = ""
    if (weekday == 6):
        ans_time = datetime.datetime.today() + datetime.timedelta(days=number)
        year = str(ans_time.year)
        month = str(ans_time.month)
        day = str(ans_time.day)
    else:
        x = weekday - number + 1
        if (x >= 0):
            ans_time = datetime.datetime.today() - datetime.timedelta(days=x)
        else:
            ans_time = datetime.datetime.today() + datetime.timedelta(days=abs(x))
        year = str(ans_time.year)
        month = str(ans_time.month)
        day = str(ans_time.day)
    if (len(month) < 2): month = str("0" + month)
    if (len(day) < 2): day = str("0" + day)
    return str(day + "." + month + "." + year)

# проверка даты на корректность
def is_good_date(date):
    try:
        if (len(date) != 10): return False
        if (date[2] != '.' or date[5] != '.' or len(date.split('.')) != 3): return False
        day = ""
        month = ""
        year = ""
        day = int(date.split('.')[0])
        month = int(date.split('.')[1])
        year = int(date.split('.')[2])
        date_obj = datetime.datetime(year, month, day)
        if (month == 2):
            if (year % 400 == 0 or (year % 100 != 0 and year % 4 == 0)):
                if (1 <= day and day <= 29 and date_obj.weekday() != 6):
                    return True
                else:
                    return False
            else:
                if (1 <= day and day <= 28 and date_obj.weekday() != 6):
                    return True
                else:
                    return False
        elif (month in [4, 6, 9, 11]):
            if (1 <= day and day <= 30 and date_obj.weekday() != 6):
                return True
            else:
                return False
        elif (month in [1, 3, 5, 7, 8, 10, 12]):
            if (1 <= day and day <= 31 and date_obj.weekday() != 6):
                return True
            else:
                return False
    except:
        return False


# получение номера по дате
def get_number_by_date(cur_date):  # 0 - пн
    date = str(cur_date)
    year = int(date[6:10])
    month = int(date[3:5])
    day = int(date[0:2])
    date_obj = datetime.datetime(year, month, day)
    return date_obj.weekday()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_start_1 = types.KeyboardButton("Домашнее задание📚")
    btn_start_admin_1 = types.KeyboardButton("✨Редактировать домашнее задание✨")
    btn_start_2 = types.KeyboardButton("Музыка")
    btn_start_3 = types.KeyboardButton("Мемы")

    markup.add(btn_start_1, btn_start_admin_1)
    markup.add(btn_start_2, btn_start_3)
    user_state[str(message.chat.id)] = 'main menu'
    open('./jsons/users_states.json', 'w', encoding='utf-8').write(json.dumps(user_state, ensure_ascii=False))
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я твой ассистент и могу ответить на вопросы, связанные со школой. Что тебе подсказать?".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text', 'photo'])
def func(message):

    mes_text = "-1"
    if (message.photo == None):
        mes_text = message.text
        mes_text = mes_text.lower()

    # вывод дз
    def print_text(day, prof, subject):
        hw = homework[day][prof]["texts"][subject]
        bot.send_message(message.chat.id,
                         text="<b> <u>" + (json.dumps(subject, ensure_ascii=False).format(message.from_user)).strip(
                             '"') + "</u></b>" + ": " + (
                                  json.dumps(hw, ensure_ascii=False).format(message.from_user)).strip('"'),
                         parse_mode='HTML')

    def print_photo(day, prof, subject):
        if (subject in homework[day][prof]["im"].keys()):
            cnt = 1
            for photo in homework[day][prof]["im"][subject]:
                bot.send_photo(message.chat.id, photo=open("./photos/" + photo, 'rb').read())
                cnt += 1

    def print_profile(day, prof):
        for subject in homework[day][prof]["texts"]:
            print_text(day, prof, subject)
            print_photo(day, prof, subject)

    def print_homework(day):
        if (not is_good_date(day)):
            bot.send_message(message.chat.id, text="Введена некорректная дата.", parse_mode='HTML')
        else:
            if (not (day in homework.keys())):
                homework[day] = {"both": {"texts": {}, "im": {}}, "inf": {"texts": {}, "im": {}},
                                 "mat": {"texts": {}, "im": {}}}
            if (len(homework[day]["both"]["texts"]) == 0 and len(homework[day]["inf"]["texts"]) == 0 and len(
                    homework[day]["mat"]["texts"]) == 0):
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn_start_1 = types.KeyboardButton("Домашнее задание📚")
                btn_start_admin_1 = types.KeyboardButton("✨Редактировать домашнее задание✨")
                btn_start_2 = types.KeyboardButton("Музыка")
                btn_start_3 = types.KeyboardButton("Мемы")

                markup.add(btn_start_1, btn_start_admin_1)
                markup.add(btn_start_2, btn_start_3)
                user_state[str(message.chat.id)] = 'main menu'
                bot.send_message(message.chat.id,
                                 text="<b> <i>Никому ничего не задали😁</i> </b>",parse_mode='HTML',
                                 reply_markup=markup)
                if (day in homework.keys()):
                    del homework[day]
            else:
                if (len(homework[day]["both"]["texts"]) != 0):
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn_start_1 = types.KeyboardButton("Домашнее задание📚")
                    btn_start_admin_1 = types.KeyboardButton("✨Редактировать домашнее задание✨")
                    btn_start_2 = types.KeyboardButton("Музыка")
                    btn_start_3 = types.KeyboardButton("Мемы")

                    markup.add(btn_start_1, btn_start_admin_1)
                    markup.add(btn_start_2, btn_start_3)
                    user_state[str(message.chat.id)] = 'main menu'
                    print_profile(day, "both")


    def print_week():
        number = datetime.datetime.today().weekday()
        if (number == 6):
            for i in range(0, 6):
                if (i == 0): bot.send_message(message.chat.id, text="<b> ДЗ НА ПОНЕДЕЛЬНИК: </b>",
                                              parse_mode='HTML'), print_homework(get_day_by_number(i + 1))
                if (i == 1): bot.send_message(message.chat.id, text="<b> ДЗ НА ВТОРНИК: </b>",
                                              parse_mode='HTML'), print_homework(get_day_by_number(i + 1))
                if (i == 2): bot.send_message(message.chat.id, text="<b> ДЗ НА СРЕДУ: </b>",
                                              parse_mode='HTML'), print_homework(get_day_by_number(i + 1))
                if (i == 3): bot.send_message(message.chat.id, text="<b> ДЗ НА ЧЕТВЕРГ: </b>",
                                              parse_mode='HTML'), print_homework(get_day_by_number(i + 1))
                if (i == 4): bot.send_message(message.chat.id, text="<b> ДЗ НА ПЯТНИЦУ: </b>",
                                              parse_mode='HTML'), print_homework(get_day_by_number(i + 1))
                if (i == 5): bot.send_message(message.chat.id, text="<b> ДЗ НА СУББОТУ: </b>",
                                              parse_mode='HTML'), print_homework(get_day_by_number(i + 1))
        for i in range(number, 6):
            if (i == 0): bot.send_message(message.chat.id, text="<b> ДЗ НА ПОНЕДЕЛЬНИК: </b>",
                                          parse_mode='HTML'), print_homework(get_day_by_number(i + 1))
            if (i == 1): bot.send_message(message.chat.id, text="<b> ДЗ НА ВТОРНИК: </b>",
                                          parse_mode='HTML'), print_homework(get_day_by_number(i + 1))
            if (i == 2): bot.send_message(message.chat.id, text="<b> ДЗ НА СРЕДУ: </b>",
                                          parse_mode='HTML'), print_homework(get_day_by_number(i + 1))
            if (i == 3): bot.send_message(message.chat.id, text="<b> ДЗ НА ЧЕТВЕРГ: </b>",
                                          parse_mode='HTML'), print_homework(get_day_by_number(i + 1))
            if (i == 4): bot.send_message(message.chat.id, text="<b> ДЗ НА ПЯТНИЦУ: </b>",
                                          parse_mode='HTML'), print_homework(get_day_by_number(i + 1))
            if (i == 5): bot.send_message(message.chat.id, text="<b> ДЗ НА СУББОТУ: </b>",
                                          parse_mode='HTML'), print_homework(get_day_by_number(i + 1))



    # кнопка вернуться назад
    if (mes_text == "вернуться назад" or mes_text == "нет❌" or user_state[str(message.chat.id)] in "not found"):
        if (user_state[str(message.chat.id)] in ["not found", "homework", "redakt hw"]):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_start_1 = types.KeyboardButton("Домашнее задание📚")
            btn_start_admin_1 = types.KeyboardButton("✨Редактировать домашнее задание✨")
            btn_start_2= types.KeyboardButton("Музыка")
            btn_start_3= types.KeyboardButton("Мемы")

            markup.add(btn_start_1, btn_start_admin_1)
            markup.add(btn_start_2, btn_start_3)
            user_state[str(message.chat.id)] = 'main menu'
            bot.send_message(message.chat.id,
                             text="Ты вернулся в главное меню. С чем тебе помочь?".format(message.from_user),
                             reply_markup=markup)
        elif (user_state[str(message.chat.id)] in ["add_hw", "del_hw", "del_all_day", "del_all_hw"]):
            user_state[str(message.chat.id)] = 'redakt hw'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_hw_1 = types.KeyboardButton("Добавить дз")
            btn_hw_3 = types.KeyboardButton("Удалить дз")
            btn_hw_4 = types.KeyboardButton("Удалить все дз")
            btn_hw_5 = types.KeyboardButton("Удалить дз на день")
            markup.add(btn_hw_1, btn_hw_3)
            markup.add(btn_hw_4, btn_hw_5)
            btn_back = types.KeyboardButton("Вернуться назад")
            markup.add(btn_back)
            bot.send_message(message.chat.id, text="Выбери действие, которое ты хочешь сделать.", reply_markup=markup)
        elif (user_state[str(message.chat.id)] in ["read_add_hw"]):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_back = types.KeyboardButton("Вернуться назад")
            markup.add(btn_back)
            user_state[str(message.chat.id)] = 'add_hw'
            helper["type"] = ""
            helper["cnt"] = 0
            bot.send_message(message.chat.id,
                             text="Напиши дату в формате ДД.ММ.ГГГГ, на который ты хочешь добавить дз.",
                             reply_markup=markup)
        elif (user_state[str(message.chat.id)] in ["read_del_hw"]):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_back = types.KeyboardButton("Вернуться назад")
            markup.add(btn_back)
            user_state[str(message.chat.id)] = 'del_hw'
            bot.send_message(message.chat.id, text="Напиши дату в формате ДД.ММ.ГГГГ, в который ты хочешь удалить дз.",
                             reply_markup=markup)
        elif (user_state[str(message.chat.id)] in ["watch_hw"]):
            user_state[str(message.chat.id)] = 'homework'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_schedule_1 = types.KeyboardButton("ДЗ на понедельник")
            btn_schedule_2 = types.KeyboardButton("ДЗ на вторник")
            btn_schedule_3 = types.KeyboardButton("ДЗ на среду")
            btn_schedule_4 = types.KeyboardButton("ДЗ на четверг")
            btn_schedule_5 = types.KeyboardButton("ДЗ на пятницу")
            btn_schedule_6 = types.KeyboardButton("ДЗ на субботу")
            btn_schedule_7 = types.KeyboardButton("ДЗ на другой день")
            btn_schedule_8 = types.KeyboardButton("ДЗ до конца недели")
            back = types.KeyboardButton("Вернуться назад")
            markup.add(btn_schedule_1, btn_schedule_2)
            markup.add(btn_schedule_3, btn_schedule_4)
            markup.add(btn_schedule_5, btn_schedule_6)
            markup.add(btn_schedule_7, btn_schedule_8)
            markup.add(back)
            bot.send_message(message.chat.id, text="На какой день тебя интересует домашнее задание?",
                             reply_markup=markup)
        elif (user_state[str(message.chat.id)] in ["del_all_day_is_correct"]):
            user_state[str(message.chat.id)] = "del_all_day"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_back = types.KeyboardButton("Вернуться назад")
            markup.add(btn_back)
            bot.send_message(message.chat.id, text="Отправь день в формате ДД.ММ.ГГГГ, дз в который ты хочешь удалить.",
                             reply_markup=markup)
        elif (user_state[str(message.chat.id)] in ["text_sch"]):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_back = types.KeyboardButton("Вернуться назад")
            markup.add(btn_back)
            bot.send_message(message.chat.id,
                             text="Напиши дату в формате ДД.ММ.ГГГГ, на которую ты хочешь добавить/удалить расписание.",
                             reply_markup=markup)
            user_state[str(message.chat.id)] = "add_text_sch"
        elif (user_state[str(message.chat.id)] in ["photo_sch"]):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_back = types.KeyboardButton("Вернуться назад")
            markup.add(btn_back)
            bot.send_message(message.chat.id,
                             text="Напиши дату в формате ДД.ММ.ГГГГ, на которую ты хочешь добавить расписание с фото (чтобы удалить фото, вернись в удаление текста).",
                             reply_markup=markup)
            user_state[str(message.chat.id)] = "add_photo_sch"
        elif (user_state[str(message.chat.id)] in ["add_text_sch", "add_photo_sch"]):
            user_state[str(message.chat.id)] = 'redakt sch'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_sch_1 = types.KeyboardButton("Изменить текст/удалить")
            btn_sch_2 = types.KeyboardButton("Изменить фото")
            markup.add(btn_sch_1, btn_sch_2)
            btn_back = types.KeyboardButton("Вернуться назад")
            markup.add(btn_back)
            bot.send_message(message.chat.id, text="Выбери действие, которое ты хочешь сделать.", reply_markup=markup)

    # вывод дз
    elif (user_state[str(message.chat.id)] == 'homework' and mes_text == "дз на понедельник"):
        print_homework(get_day_by_number(1))
    elif (user_state[str(message.chat.id)] == 'homework' and mes_text == "дз на вторник"):
        print_homework(get_day_by_number(2))
    elif (user_state[str(message.chat.id)] == 'homework' and mes_text == "дз на среду"):
        print_homework(get_day_by_number(3))
    elif (user_state[str(message.chat.id)] == 'homework' and mes_text == "дз на четверг"):
        print_homework(get_day_by_number(4))
    elif (user_state[str(message.chat.id)] == 'homework' and mes_text == "дз на пятницу"):
        print_homework(get_day_by_number(5))
    elif (user_state[str(message.chat.id)] == 'homework' and mes_text == "дз на субботу"):
        print_homework(get_day_by_number(6))
    elif (user_state[str(message.chat.id)] == 'homework' and mes_text == "дз до конца недели"):
        print_week()
    elif (user_state[str(message.chat.id)] == 'watch_hw'):
        print_homework(mes_text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
    elif (user_state[str(message.chat.id)] == 'homework' and mes_text == "дз на другой день"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
        bot.send_message(message.chat.id, text="Напиши дату в формате ДД.ММ.ГГГГ, на которую ты хочешь посмотреть дз",
                         reply_markup=markup)
        user_state[str(message.chat.id)] = "watch_hw"

    # кнопки для вывода дз
    elif (user_state[str(message.chat.id)] == 'homework' or (
            user_state[str(message.chat.id)] == 'main menu' and mes_text == "домашнее задание📚")):
        user_state[str(message.chat.id)] = 'homework'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_schedule_1 = types.KeyboardButton("ДЗ на понедельник")
        btn_schedule_2 = types.KeyboardButton("ДЗ на вторник")
        btn_schedule_3 = types.KeyboardButton("ДЗ на среду")
        btn_schedule_4 = types.KeyboardButton("ДЗ на четверг")
        btn_schedule_5 = types.KeyboardButton("ДЗ на пятницу")
        btn_schedule_6 = types.KeyboardButton("ДЗ на субботу")
        btn_schedule_7 = types.KeyboardButton("ДЗ на другой день")
        btn_schedule_8 = types.KeyboardButton("ДЗ до конца недели")
        back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_schedule_1, btn_schedule_2)
        markup.add(btn_schedule_3, btn_schedule_4)
        markup.add(btn_schedule_5, btn_schedule_6)
        markup.add(btn_schedule_7, btn_schedule_8)
        markup.add(back)
        bot.send_message(message.chat.id, text="На какой день тебя интересует домашнее задание?", reply_markup=markup)



    # кнопка музыка
    elif (user_state[str(message.chat.id)] == 'main menu' and mes_text == "музыка"):
        playlist = send_playlist()
        bot.send_photo(message.chat.id, playlist)

    # кнопка мемы
    elif (user_state[str(message.chat.id)] == 'main menu' and mes_text == "мемы"):
        photo = send_memes()
        bot.send_photo(message.chat.id, photo)

    # добавить дз
    elif (user_state[str(message.chat.id)] == 'redakt hw' and mes_text == "добавить дз"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
        bot.send_message(message.chat.id, text="Напиши дату в формате ДД.ММ.ГГГГ, на которую ты хочешь добавить дз.",
                         reply_markup=markup)
        user_state[str(message.chat.id)] = "add_hw"
    # считывание фото для дз
    elif (helper["type"] == "add" and user_state[str(message.chat.id)] == "read_add_hw"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        name_of_new_file = randomword(20) + ".jpg"
        src = './photos/' + name_of_new_file
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        if (not (helper["sub"] in homework[helper["day"]][helper["profile"]]["im"].keys())):
            homework[helper["day"]][helper["profile"]]["im"][helper["sub"]] = []
        homework[helper["day"]][helper["profile"]]["im"][helper["sub"]].append(name_of_new_file)
        helper["cnt"] = (helper["cnt"] - 1)
        if (helper["cnt"] == 0):
            user_state[str(message.chat.id)] = 'redakt hw'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_hw_1 = types.KeyboardButton("Добавить дз")
            btn_hw_3 = types.KeyboardButton("Удалить дз")
            btn_hw_4 = types.KeyboardButton("Удалить все дз")
            btn_hw_5 = types.KeyboardButton("Удалить дз на день")
            markup.add(btn_hw_1, btn_hw_3)
            markup.add(btn_hw_4, btn_hw_5)
            btn_back = types.KeyboardButton("Вернуться назад")
            markup.add(btn_back)
            bot.send_message(message.chat.id, text="Домашнее задание успешно добавлено!", reply_markup=markup)
            helper["type"] = ""

    # вывод дз для добавления
    elif (user_state[str(message.chat.id)] == "add_hw"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
        if (not is_good_date(mes_text)):
            bot.send_message(message.chat.id, text="Ты ввел дату не в том формате. Пожалуйста, повтори попытку.")
        else:
            print_homework(mes_text)
            helper["day"] = mes_text
            user_state[str(message.chat.id)] = "read_add_hw"
            bot.send_message(message.chat.id,
                             text="Напиши запрос в формате: *предмет* *кому* с *фото* фото и само дз.\n*предмет* - предмет, записанный одним словом в именительном падеже.\n*кому* - подгруппе или всем.\n*фото* - с х фото, где х - кол-во фото дз на этот предмет (Если фото есть, то отправь его(их) следуюущим(-и) сообщением. Если есть только фото, то напиши текстом, что всё задание на фото.)",
                             reply_markup=markup)
    # считывание дз для добавления
    elif (user_state[str(message.chat.id)] == "read_add_hw"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        sub = mes_text.split()[0]
        profile = "both"
        if (mes_text.split()[1][0:2] == "ин"): profile = "inf"
        if (mes_text.split()[1][0:2] == "ма"): profile = "mat"
        cnt = int(mes_text.split()[3])
        type = "add"
        hw = ""
        for x in message.text.split()[5::]:
            hw = hw + x + " "
        if (not (helper["day"] in homework.keys())):
            homework[helper["day"]] = {"both": {"texts": {}, "im": {}}, "inf": {"texts": {}, "im": {}},
                                       "mat": {"texts": {}, "im": {}}}
        else:
            if (len(homework[helper["day"]][profile]["texts"]) != 0 and sub in homework[helper["day"]][profile][
                "texts"].keys()):
                del homework[helper["day"]][profile]["texts"][sub]
            if (len(homework[helper["day"]][profile]["im"]) != 0 and sub in homework[helper["day"]][profile][
                "im"].keys()):
                for x in homework[helper["day"]][profile]["im"][sub]:
                    os.remove("./photos/" + x)
                del homework[helper["day"]][profile]["im"][sub]
        homework[helper["day"]][profile]["texts"][sub] = hw
        if (cnt == 0):
            user_state[str(message.chat.id)] = 'redakt hw'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_hw_1 = types.KeyboardButton("Добавить дз")
            btn_hw_3 = types.KeyboardButton("Удалить дз")
            btn_hw_4 = types.KeyboardButton("Удалить все дз")
            btn_hw_5 = types.KeyboardButton("Удалить дз на день")
            markup.add(btn_hw_1, btn_hw_3)
            markup.add(btn_hw_4, btn_hw_5)
            btn_back = types.KeyboardButton("Вернуться назад")
            markup.add(btn_back)
            bot.send_message(message.chat.id, text="Домашнее задание успешно добавлено!", reply_markup=markup)
            helper["type"] = ""
        else:
            helper["type"] = type
            helper["profile"] = profile
            helper["sub"] = sub
            helper["cnt"] = cnt

    # удалить дз
    elif (user_state[str(message.chat.id)] == 'redakt hw' and mes_text == "удалить дз"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
        bot.send_message(message.chat.id, text="Напиши дату в формате ДД.ММ.ГГГГ, в которую ты хочешь удалить дз.",
                         reply_markup=markup)
        user_state[str(message.chat.id)] = "del_hw"
    # вывод дз для удаления
    elif (user_state[str(message.chat.id)] == "del_hw"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
        day = mes_text
        if (not is_good_date(mes_text)):
            bot.send_message(message.chat.id, text="Ты ввел дату не в том формате. Пожалуйста, повтори попытку.")
        else:
            print_homework(day)
            helper["day"] = day
            bot.send_message(message.chat.id,
                             text='Напиши запрос в формате: *предмет* всем *что удалить*\n*предмет* - предмет так, как он записан выше.\n*что удалить* - текст/фото и перечесление номеров фото через пробел, которые надо удалить(или просто "фото" для удаления всех фото/все\n',
                             reply_markup=markup)
            user_state[str(message.chat.id)] = "read_del_hw"
    # считывание дз для удаления
    elif (user_state[str(message.chat.id)] == "read_del_hw"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
        sub = mes_text.split()[0]
        profile = "both"
        if (mes_text.split()[1][0:2] == "ин"): profile = "inf"
        if (mes_text.split()[1][0:2] == "ма"): profile = "mat"
        day = helper["day"]
        if (mes_text.split()[2] == "все"):
            if (not sub in homework[day][profile]["texts"].keys()):
                bot.send_message(message.chat.id, text="Такого предмета нет. Пожалуйста, повтори запрос.",
                                 reply_markup=markup)
            else:
                helper["type"] = ""
                if (len(homework[day][profile]["texts"]) != 0):
                    del homework[day][profile]["texts"][sub]
                if (len(homework[day][profile]["im"]) != 0):
                    for x in homework[day][profile]["im"][sub]:
                        os.remove("./photos/" + x)
                user_state[str(message.chat.id)] = 'redakt hw'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn_hw_1 = types.KeyboardButton("Добавить дз")
                btn_hw_3 = types.KeyboardButton("Удалить дз")
                btn_hw_4 = types.KeyboardButton("Удалить все дз")
                btn_hw_5 = types.KeyboardButton("Удалить дз на день")
                markup.add(btn_hw_1, btn_hw_3)
                markup.add(btn_hw_4, btn_hw_5)
                btn_back = types.KeyboardButton("Вернуться назад")
                markup.add(btn_back)
                bot.send_message(message.chat.id, text="Домашнее задание успешно удалено!", reply_markup=markup)
        elif (mes_text.split()[2] == "текст"):
            if (not sub in homework[day][profile]["texts"].keys()):
                bot.send_message(message.chat.id, text="Такого предмета нет. Пожалуйста, повтори запрос.",
                                 reply_markup=markup)
            else:
                del homework[day][profile]["texts"][sub]
                user_state[str(message.chat.id)] = 'redakt hw'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn_hw_1 = types.KeyboardButton("Добавить дз")
                btn_hw_3 = types.KeyboardButton("Удалить дз")
                btn_hw_4 = types.KeyboardButton("Удалить все дз")
                btn_hw_5 = types.KeyboardButton("Удалить дз на день")
                markup.add(btn_hw_1, btn_hw_3)
                markup.add(btn_hw_4, btn_hw_5)
                btn_back = types.KeyboardButton("Вернуться назад")
                markup.add(btn_back)
                bot.send_message(message.chat.id,
                                 text="Домашнее задание успешно удалено! Не забудь добавить текстовое домашнее задание!",
                                 reply_markup=markup)
        else:
            if (not sub in homework[day][profile]["im"].keys()):
                bot.send_message(message.chat.id, text="Такого предмета нет. Пожалуйста, повтори запрос.",
                                 reply_markup=markup)
            else:
                if (mes_text.split()[-1] == "фото"):
                    for x in homework[day][profile]["im"][sub]:
                        os.remove("./photos/" + x)
                    del homework[day][profile]["im"][sub]
                else:
                    new_photos = []
                    for i in range(0, len(homework[day][profile]["im"][sub])):
                        if (not (str(i + 1) in mes_text)):
                            new_photos.append(homework[day][profile]["im"][sub][i])
                    for x in homework[day][profile]["im"][sub]:
                        if (not x in new_photos):
                            os.remove("./photos/" + x)
                    homework[day][profile]["im"][sub] = new_photos
                user_state[str(message.chat.id)] = 'redakt hw'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn_hw_1 = types.KeyboardButton("Добавить дз")
                btn_hw_3 = types.KeyboardButton("Удалить дз")
                btn_hw_4 = types.KeyboardButton("Удалить все дз")
                btn_hw_5 = types.KeyboardButton("Удалить дз на день")
                markup.add(btn_hw_1, btn_hw_3)
                markup.add(btn_hw_4, btn_hw_5)
                btn_back = types.KeyboardButton("Вернуться назад")
                markup.add(btn_back)
                bot.send_message(message.chat.id, text="Домашнее задание успешно удалено!", reply_markup=markup)
        ch = 1 - 1
        for profile in homework[day]:
            if (len(homework[day][profile]["texts"]) != 0):
                ch += 1
        if (ch == 0):
            del homework[day]

    # очистка всего дз
    elif (user_state[str(message.chat.id)] == 'redakt hw' and mes_text == "удалить все дз"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_yes = types.KeyboardButton("Да✅")
        btn_no = types.KeyboardButton("Нет❌")
        markup.add(btn_yes, btn_no)
        bot.send_message(message.chat.id, text="Ты уверен?", reply_markup=markup)
        user_state[str(message.chat.id)] = "del_all_hw"
    elif (mes_text == "да✅" and user_state[str(message.chat.id)] == "del_all_hw"):
        texts = []
        days = []
        for day in homework:
            days.append(day)
            for profile in homework[day]:
                if (len(homework[day][profile]["texts"]) != 0):
                    for subject in homework[day][profile]["texts"]:
                        texts.append(day + " " + profile + " " + subject + " texts")
                if (len(homework[day][profile]["im"]) != 0):
                    for subject in homework[day][profile]["im"]:
                        texts.append(day + " " + profile + " " + subject + " im")
        for x in texts:
            day = x.split()[0]
            profile = x.split()[1]
            subject = x.split()[2]
            wh = x.split()[3]
            if (wh == "texts"):
                del homework[day][profile]["texts"][subject]
            else:
                if (len(homework[day][profile]["im"]) != 0):
                    if (subject in homework[day][profile]["im"].keys()):
                        for y in homework[day][profile]["im"][subject]:
                            os.remove("./photos/" + y)
                    del homework[day][profile]["im"][subject]
        for cur_day in days:
            del homework[cur_day]
        user_state[str(message.chat.id)] = 'redakt hw'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_hw_1 = types.KeyboardButton("Добавить дз")
        btn_hw_3 = types.KeyboardButton("Удалить дз")
        btn_hw_4 = types.KeyboardButton("Удалить все дз")
        btn_hw_5 = types.KeyboardButton("Удалить дз на день")
        markup.add(btn_hw_1, btn_hw_3)
        markup.add(btn_hw_4, btn_hw_5)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
        bot.send_message(message.chat.id, text="Домашнее задание успешно удалено.", reply_markup=markup)


    # очистка одного дня
    elif (user_state[str(message.chat.id)] == 'redakt hw' and mes_text == "удалить дз на день"):
        user_state[str(message.chat.id)] = "del_all_day"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
        bot.send_message(message.chat.id, text="Отправь день в формате ДД.ММ.ГГГГ, дз в который ты хочешь удалить.",
                         reply_markup=markup)
    elif (user_state[str(message.chat.id)] == "del_all_day"):
        if (not is_good_date(mes_text)):
            bot.send_message(message.chat.id, text="Ты ввел дату не в том формате. Пожалуйста, повтори попытку.")
        else:
            print_homework(mes_text)
            if ((not (mes_text in homework.keys())) or (len(homework[mes_text]["both"]["texts"]) == 0 and len(
                    homework[mes_text]["inf"]["texts"]) == 0 and len(homework[mes_text]["mat"]["texts"]) == 0)):
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn_back = types.KeyboardButton("Вернуться назад")
                markup.add(btn_back)
                return
            user_state[str(message.chat.id)] = "del_all_day_is_correct"
            helper["day"] = mes_text
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_yes = types.KeyboardButton("Да✅")
            btn_no = types.KeyboardButton("Нет❌")
            markup.add(btn_yes, btn_no)
            bot.send_message(message.chat.id, text="Ты уверен?", reply_markup=markup)
    elif (mes_text == "да✅" and user_state[str(message.chat.id)] == "del_all_day_is_correct"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
        texts = []
        cur_date = helper["day"]
        helper["day"] = ""
        if (not (cur_date in homework.keys())):
            bot.send_message(message.chat.id, text="На этот день ничего не задали, выбери другой день.",
                             reply_markup=markup)
            user_state[str(message.chat.id)] = "del_all_day"
        else:
            for profile in homework[cur_date]:
                if (len(homework[cur_date][profile]["texts"]) != 0):
                    for subject in homework[cur_date][profile]["texts"]:
                        texts.append(cur_date + " " + profile + " " + subject + " texts")
                if (len(homework[cur_date][profile]["im"]) != 0):
                    for subject in homework[cur_date][profile]["im"]:
                        texts.append(cur_date + " " + profile + " " + subject + " im")
            for x in texts:
                day = x.split()[0]
                profile = x.split()[1]
                subject = x.split()[2]
                wh = x.split()[3]
                if (wh == "texts"):
                    del homework[day][profile]["texts"][subject]
                else:
                    if (len(homework[day][profile]["im"]) != 0):
                        if (subject in homework[day][profile]["im"].keys()):
                            for y in homework[day][profile]["im"][subject]:
                                os.remove("./photos/" + y)
                        del homework[day][profile]["im"][subject]
            del homework[day]
            user_state[str(message.chat.id)] = 'redakt hw'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_hw_1 = types.KeyboardButton("Добавить дз")
            btn_hw_3 = types.KeyboardButton("Удалить дз")
            btn_hw_4 = types.KeyboardButton("Удалить все дз")
            btn_hw_5 = types.KeyboardButton("Удалить дз на день")
            markup.add(btn_hw_1, btn_hw_3)
            markup.add(btn_hw_4, btn_hw_5)
            btn_back = types.KeyboardButton("Вернуться назад")
            markup.add(btn_back)
            bot.send_message(message.chat.id, text="Домашнее задание успешно удалено.", reply_markup=markup)


    # кнопки редактирования дз
    elif (user_state[str(message.chat.id)] == 'redakt hw' or (user_state[str(message.chat.id)] == 'main menu' and mes_text == "✨редактировать домашнее задание✨")):
        user_state[str(message.chat.id)] = 'redakt hw'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_hw_1 = types.KeyboardButton("Добавить дз")
        # btn_hw_2 = types.KeyboardButton("Изменить дз")
        btn_hw_3 = types.KeyboardButton("Удалить дз")
        btn_hw_4 = types.KeyboardButton("Удалить все дз")
        btn_hw_5 = types.KeyboardButton("Удалить дз на день")
        markup.add(btn_hw_1, btn_hw_3)
        markup.add(btn_hw_4, btn_hw_5)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
        bot.send_message(message.chat.id, text="Выбери действие, которое ты хочешь сделать.", reply_markup=markup)


    open('./jsons/users_states.json', 'w', encoding='utf-8').write(json.dumps(user_state, ensure_ascii=False))
    open('./jsons/homeworks.json', 'w', encoding='utf-8').write(json.dumps(homework, ensure_ascii=False))
    open('./jsons/edithw.json', 'w', encoding='utf-8').write(json.dumps(helper, ensure_ascii=False))


# для локальных тестов
bot.polling(none_stop=True)

# для сервера:
# while(True):
#     try:
#         bot.polling(none_stop=True)
#     except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
#         print("Telegram bot module went out, try to relaunch...")
