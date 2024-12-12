import telebot, string, random
import json
import os
import output_hw
import mydate
import other_functions
from telebot import types

token = open('file_token.txt').read()
bot = telebot.TeleBot(token)
print("Bot is online.")
myid = ""


@bot.message_handler(commands=['start'])
def start(message):
    global myid
    myid = str(message.from_user.id)

    file_name = "homework" + str(message.from_user.id) + ".json"
    open('./jsons/' + file_name, 'a', encoding='utf-8')
    a = open('./jsons/' + 'homework' + myid + ".json", 'r', encoding='utf-8').read()
    if len(a) == 0:
        with open('./jsons/' + file_name, 'w', encoding='utf-8') as f:
            json.dump({}, f)
        f.close()

    file_name = "user_state" + str(message.from_user.id) + ".json"
    #open('./jsons/' + file_name, 'w', encoding='utf-8')
    with open('./jsons/' + file_name, 'w', encoding='utf-8') as f:
        json.dump({str(message.from_user.id): "not found"}, f)
    f.close()

    user_state = json.loads(open('./jsons/' + file_name, 'r', encoding='utf-8').read())

    file_name = "helper" + str(message.from_user.id) + ".json"
    with open('./jsons/' + file_name, 'w', encoding='utf-8') as f:
        json.dump({"type": "", "day": "", "profile": "all", "sub": "", "cnt": 0}, f)
    f.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_start_1 = types.KeyboardButton("Домашнее задание📚")
    btn_start_admin_1 = types.KeyboardButton("✨Редактировать домашнее задание✨")
    btn_start_2 = types.KeyboardButton("Музыка")
    btn_start_3 = types.KeyboardButton("Мемы")
    btn_start_4 = types.KeyboardButton("Полезное")

    markup.add(btn_start_1, btn_start_admin_1)
    markup.add(btn_start_2, btn_start_3, btn_start_4)

    user_state[str(message.chat.id)] = 'main menu'
    open('./jsons/user_state' + myid + '.json', 'w', encoding='utf-8').write(json.dumps(user_state, ensure_ascii=False))
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я твой ассистент и могу ответить на вопросы, связанные со школой. Что тебе подсказать?".format(
                         message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text', 'photo'])
def func(message):

    myid = str(message.from_user.id)
    homework = json.loads(open('./jsons/' + 'homework' + myid + ".json", 'r', encoding='utf-8').read())
    user_state = json.loads(open('./jsons/' + "user_state" + myid + ".json", 'r', encoding='utf-8').read())
    helper = json.loads(open('./jsons/' + "helper" + myid + ".json", 'r', encoding='utf-8').read())

    print(user_state)
    mes_text = "-1"
    if message.photo == None:
        mes_text = message.text
        mes_text = mes_text.lower()

    # кнопка вернуться назад
    if mes_text == "вернуться назад" or mes_text == "нет❌" or user_state[myid] in "not found":
        if user_state[str(message.chat.id)] in ["not found", "homework", "redakt hw"]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_start_1 = types.KeyboardButton("Домашнее задание📚")
            btn_start_admin_1 = types.KeyboardButton("✨Редактировать домашнее задание✨")
            btn_start_2 = types.KeyboardButton("Музыка")
            btn_start_3 = types.KeyboardButton("Мемы")
            btn_start_4 = types.KeyboardButton("Полезное")

            markup.add(btn_start_1, btn_start_admin_1)
            markup.add(btn_start_2, btn_start_3, btn_start_4)

            user_state[str(message.chat.id)] = 'main menu'
            bot.send_message(message.chat.id,
                             text="Ты вернулся в главное меню. С чем тебе помочь?".format(message.from_user),
                             reply_markup=markup)
        elif user_state[str(message.chat.id)] in ["add_hw", "del_hw", "del_all_day", "del_all_hw"]:
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
        elif user_state[str(message.chat.id)] in ["read_add_hw"]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_back = types.KeyboardButton("Вернуться назад")
            markup.add(btn_back)
            user_state[str(message.chat.id)] = 'add_hw'
            helper["type"] = ""
            helper["cnt"] = 0
            bot.send_message(message.chat.id,
                             text="Напиши дату в формате ДД.ММ.ГГГГ, на который ты хочешь добавить дз.",
                             reply_markup=markup)
        elif user_state[str(message.chat.id)] in ["read_del_hw"]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_back = types.KeyboardButton("Вернуться назад")
            markup.add(btn_back)
            user_state[str(message.chat.id)] = 'del_hw'
            bot.send_message(message.chat.id, text="Напиши дату в формате ДД.ММ.ГГГГ, в который ты хочешь удалить дз.",
                             reply_markup=markup)
        elif user_state[str(message.chat.id)] in ["watch_hw"]:
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
        elif user_state[str(message.chat.id)] in ["del_all_day_is_correct"]:
            user_state[str(message.chat.id)] = "del_all_day"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_back = types.KeyboardButton("Вернуться назад")
            markup.add(btn_back)
            bot.send_message(message.chat.id, text="Отправь день в формате ДД.ММ.ГГГГ, дз в который ты хочешь удалить.",
                             reply_markup=markup)
        elif user_state[str(message.chat.id)] in ["text_sch"]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_back = types.KeyboardButton("Вернуться назад")
            markup.add(btn_back)
            bot.send_message(message.chat.id,
                             text="Напиши дату в формате ДД.ММ.ГГГГ, на которую ты хочешь добавить/удалить расписание.",
                             reply_markup=markup)
            user_state[str(message.chat.id)] = "add_text_sch"
        elif user_state[str(message.chat.id)] in ["photo_sch"]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_back = types.KeyboardButton("Вернуться назад")
            markup.add(btn_back)
            bot.send_message(message.chat.id,
                             text="Напиши дату в формате ДД.ММ.ГГГГ, на которую ты хочешь добавить расписание с фото (чтобы удалить фото, вернись в удаление текста).",
                             reply_markup=markup)
            user_state[str(message.chat.id)] = "add_photo_sch"
        elif user_state[str(message.chat.id)] in ["add_text_sch", "add_photo_sch"]:
            user_state[str(message.chat.id)] = 'redakt sch'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_sch_1 = types.KeyboardButton("Изменить текст/удалить")
            btn_sch_2 = types.KeyboardButton("Изменить фото")
            markup.add(btn_sch_1, btn_sch_2)
            btn_back = types.KeyboardButton("Вернуться назад")
            markup.add(btn_back)
            bot.send_message(message.chat.id, text="Выбери действие, которое ты хочешь сделать.", reply_markup=markup)

    # вывод дз
    elif user_state[str(message.chat.id)] == 'homework' and mes_text == "дз на понедельник":
        user_state[str(message.chat.id)] = output_hw.print_homework(bot, message, mydate.get_day_by_number(1))
    elif user_state[str(message.chat.id)] == 'homework' and mes_text == "дз на вторник":
        user_state[str(message.chat.id)] = output_hw.print_homework(bot, message, mydate.get_day_by_number(2))
    elif user_state[str(message.chat.id)] == 'homework' and mes_text == "дз на среду":
        user_state[str(message.chat.id)] = output_hw.print_homework(bot, message, mydate.get_day_by_number(3))
    elif user_state[str(message.chat.id)] == 'homework' and mes_text == "дз на четверг":
        user_state[str(message.chat.id)] = output_hw.print_homework(bot, message, mydate.get_day_by_number(4))
    elif user_state[str(message.chat.id)] == 'homework' and mes_text == "дз на пятницу":
        user_state[str(message.chat.id)] = output_hw.print_homework(bot, message, mydate.get_day_by_number(5))
    elif user_state[str(message.chat.id)] == 'homework' and mes_text == "дз на субботу":
        user_state[str(message.chat.id)] = output_hw.print_homework(bot, message, mydate.get_day_by_number(6))
    elif user_state[str(message.chat.id)] == 'homework' and mes_text == "дз до конца недели":
        user_state[str(message.chat.id)] = output_hw.print_week(bot, message)
    elif user_state[str(message.chat.id)] == 'watch_hw':
        user_state[str(message.chat.id)] = output_hw.print_homework(bot, message, mes_text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
    elif user_state[str(message.chat.id)] == 'homework' and mes_text == "дз на другой день":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
        bot.send_message(message.chat.id, text="Напиши дату в формате ДД.ММ.ГГГГ, на которую ты хочешь посмотреть дз",
                         reply_markup=markup)
        user_state[str(message.chat.id)] = "watch_hw"

    # кнопки для вывода дз
    elif user_state[str(message.chat.id)] == 'homework' or user_state[str(message.chat.id)] == 'main menu' and mes_text == "домашнее задание📚":
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

    # кнопка полезное
    elif (user_state[str(message.chat.id)] == 'main menu' and mes_text == "полезное"):
        other_functions.more_information(bot, message)

    # кнопка музыка
    elif user_state[str(message.chat.id)] == 'main menu' and mes_text == "музыка":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, text="🎧5 треков для учебы уже отправляются!", reply_markup=markup)
        other_functions.send_playlist(bot, message)

    # кнопка мемы
    elif user_state[str(message.chat.id)] == 'main menu' and mes_text == "мемы":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        photo = other_functions.send_memes(bot, message)
        bot.send_photo(message.chat.id, photo, reply_markup=markup)

    # добавить дз
    elif user_state[str(message.chat.id)] == 'redakt hw' and mes_text == "добавить дз":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
        bot.send_message(message.chat.id, text="Напиши дату в формате ДД.ММ.ГГГГ, на которую ты хочешь добавить дз.",
                         reply_markup=markup)
        user_state[str(message.chat.id)] = "add_hw"

    # считывание фото для дз
    elif helper["type"] == "add" and user_state[str(message.chat.id)] == "read_add_hw":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        name_of_new_file = other_functions.randomword(20) + ".jpg"
        src = './photos/' + name_of_new_file
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        if not (helper["sub"] in homework[helper["day"]][helper["profile"]]["im"].keys()):
            homework[helper["day"]][helper["profile"]]["im"][helper["sub"]] = []
        homework[helper["day"]][helper["profile"]]["im"][helper["sub"]].append(name_of_new_file)
        helper["cnt"] = (helper["cnt"] - 1)
        if helper["cnt"] == 0:
            user_state[str(message.chat.id)] = 'redakt hw'
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
    elif user_state[str(message.chat.id)] == "add_hw":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
        if not mydate.is_good_date(mes_text):
            bot.send_message(message.chat.id, text="Ты ввел дату не в том формате. Пожалуйста, повтори попытку.")
        else:
            user_state[str(message.chat.id)] = output_hw.print_homework(bot, message, mes_text)
            helper["day"] = mes_text
            user_state[str(message.chat.id)] = "read_add_hw"
            bot.send_message(message.chat.id,
                             text="Напиши запрос в формате: *предмет* с *х* фото и само дз.\n*предмет* - предмет, записанный одним словом в именительном падеже.\nс х фото, где х - кол-во фото дз на этот предмет, 0<=x<=10 (Если фото есть, то отправь его(их) следующим(-и) сообщением. Если есть только фото, то напиши текстом, что все задание на фото.)",
                             reply_markup=markup)
    # считывание дз для добавления
    elif user_state[str(message.chat.id)] == "read_add_hw":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #btn_back = types.KeyboardButton("Вернуться назад")
        check = list(mes_text.split())
        if len(check) < 4 or check[1] != 'с' or not(check[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']) or check[3] != 'фото':
            bot.send_message(message.chat.id,
                             text="Введен некорректный запрос. Напиши его в формате: *предмет* с *x* фото и само дз.\n*предмет* - предмет, записанный одним словом в именительном падеже.\nс х фото, где х - кол-во фото дз на этот предмет, 0<=x<=10 (Если фото есть, то отправь его(их) следуюущим(-и) сообщением. Если есть только фото, то напиши текстом, что всё задание на фото.)",
                             reply_markup=markup)
        else:
            sub = mes_text.split()[0]
            profile = "all"
            cnt = int(mes_text.split()[2])
            type = "add"
            hw = ""
            for x in message.text.split()[4::]:
                hw = hw + x + " "
            if not (helper["day"] in homework.keys()):
                homework[helper["day"]] = {"all": {"texts": {}, "im": {}}}
            else:
                if len(homework[helper["day"]][profile]["texts"]) != 0 and sub in homework[helper["day"]][profile]["texts"].keys():
                    del homework[helper["day"]][profile]["texts"][sub]
                if len(homework[helper["day"]][profile]["im"]) != 0 and sub in homework[helper["day"]][profile]["im"].keys():
                    for x in homework[helper["day"]][profile]["im"][sub]:
                        os.remove("./photos/" + x)
                    del homework[helper["day"]][profile]["im"][sub]
            homework[helper["day"]][profile]["texts"][sub] = hw
            if cnt == 0:
                user_state[str(message.chat.id)] = 'redakt hw'
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
    elif user_state[str(message.chat.id)] == 'redakt hw' and mes_text == "удалить дз":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
        bot.send_message(message.chat.id, text="Напиши дату в формате ДД.ММ.ГГГГ, в которую ты хочешь удалить дз.",
                         reply_markup=markup)
        user_state[str(message.chat.id)] = "del_hw"

    # вывод дз для удаления
    elif user_state[str(message.chat.id)] == "del_hw":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
        day = mes_text
        if not mydate.is_good_date(mes_text):
            bot.send_message(message.chat.id, text="Ты ввел дату не в том формате. Пожалуйста, повтори попытку.")
        else:
            user_state[str(message.chat.id)] = output_hw.print_homework(bot, message, day)
            helper["day"] = day
            bot.send_message(message.chat.id,
                             text='Напиши запрос в формате: *предмет* *что удалить*\n*предмет* - предмет так, как он записан выше.\n*что удалить* - текст/фото и перечесление номеров фото через пробел, которые надо удалить(или просто "фото" для удаления всех фото), "все", если надо удалить всю домашку на данный предмет\n',
                             reply_markup=markup)
            user_state[str(message.chat.id)] = "read_del_hw"

    # считывание дз для удаления
    elif user_state[str(message.chat.id)] == "read_del_hw":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
        if len(list(mes_text.split())) != 2:
            bot.send_message(message.chat.id, text="Ты ввел запрос не в том формате. Пожалуйста, повтори попытку.")
        else:
            sub = mes_text.split()[0]
            profile = "all"
            day = helper["day"]
            if mes_text.split()[2] == "все":
                if not(sub in homework[day][profile]["texts"].keys()):
                    bot.send_message(message.chat.id, text="Такого предмета нет. Пожалуйста, повтори запрос.",
                                    reply_markup=markup)
                else:
                    helper["type"] = ""
                    if len(homework[day][profile]["texts"]) != 0:
                        del homework[day][profile]["texts"][sub]
                    if len(homework[day][profile]["im"]) != 0:
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
            elif mes_text.split()[2] == "текст":
                if not(sub in homework[day][profile]["texts"].keys()):
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
                if not(sub in homework[day][profile]["im"].keys()):
                    bot.send_message(message.chat.id, text="Такого предмета нет. Пожалуйста, повтори запрос.",
                                     reply_markup=markup)
                else:
                    if mes_text.split()[-1] == "фото":
                        for x in homework[day][profile]["im"][sub]:
                            os.remove("./photos/" + x)
                        del homework[day][profile]["im"][sub]
                    else:
                        new_photos = []
                        for i in range(0, len(homework[day][profile]["im"][sub])):
                            if not (str(i + 1) in mes_text):
                                new_photos.append(homework[day][profile]["im"][sub][i])
                        for x in homework[day][profile]["im"][sub]:
                            if not x in new_photos:
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
            ch = 0
            for profile in homework[day]:
                if len(homework[day][profile]["texts"]) != 0:
                    ch += 1
            if ch == 0:
                del homework[day]

    # очистка всего дз
    elif user_state[str(message.chat.id)] == 'redakt hw' and mes_text == "удалить все дз":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_yes = types.KeyboardButton("Да✅")
        btn_no = types.KeyboardButton("Нет❌")
        markup.add(btn_yes, btn_no)
        bot.send_message(message.chat.id, text="Ты уверен?", reply_markup=markup)
        user_state[str(message.chat.id)] = "del_all_hw"
    elif mes_text == "да✅" and user_state[str(message.chat.id)] == "del_all_hw":
        texts = []
        days = []
        profile = "all"
        for day in homework:
            days.append(day)
            if len(homework[day][profile]["texts"]) != 0:
                for subject in homework[day][profile]["texts"]:
                    texts.append(day + " " + profile + " " + subject + " texts")
            if len(homework[day][profile]["im"]) != 0:
                for subject in homework[day][profile]["im"]:
                    texts.append(day + " " + profile + " " + subject + " im")
        for x in texts:
            day = x.split()[0]
            profile = "all"
            subject = x.split()[2]
            wh = x.split()[3]
            if wh == "texts":
                del homework[day][profile]["texts"][subject]
            else:
                if len(homework[day][profile]["im"]) != 0:
                    if subject in homework[day][profile]["im"].keys():
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
    elif user_state[str(message.chat.id)] == 'redakt hw' and mes_text == "удалить дз на день":
        user_state[str(message.chat.id)] = "del_all_day"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
        bot.send_message(message.chat.id, text="Отправь день в формате ДД.ММ.ГГГГ, дз в который ты хочешь удалить.",
                         reply_markup=markup)
    elif user_state[str(message.chat.id)] == "del_all_day":
        if not mydate.is_good_date(mes_text):
            bot.send_message(message.chat.id, text="Ты ввел дату не в том формате. Пожалуйста, повтори попытку.")
        else:
            user_state[str(message.chat.id)] = output_hw.print_homework(bot, message, mes_text)
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
    elif mes_text == "да✅" and user_state[str(message.chat.id)] == "del_all_day_is_correct":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("Вернуться назад")
        markup.add(btn_back)
        texts = []
        profile = "all"
        cur_date = helper["day"]
        helper["day"] = ""
        if not(cur_date in homework.keys()) or not(profile in homework[cur_date].keys()):
            bot.send_message(message.chat.id, text="На этот день ничего не задали, выбери другой день.",
                             reply_markup=markup)
            user_state[str(message.chat.id)] = "del_all_day"
        else:
            if len(homework[cur_date][profile]["texts"]) != 0:
                for subject in homework[cur_date][profile]["texts"]:
                    texts.append(cur_date + " " + profile + " " + subject + " texts")
            if len(homework[cur_date][profile]["im"]) != 0:
                for subject in homework[cur_date][profile]["im"]:
                    texts.append(cur_date + " " + profile + " " + subject + " im")
            for x in texts:
                day = x.split()[0]
                subject = x.split()[2]
                wh = x.split()[3]
                if wh == "texts":
                    del homework[day][profile]["texts"][subject]
                else:
                    if len(homework[day][profile]["im"]) != 0:
                        if subject in homework[day][profile]["im"].keys():
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
    elif (user_state[str(message.chat.id)] == 'redakt hw' or (
            user_state[str(message.chat.id)] == 'main menu' and mes_text == "✨редактировать домашнее задание✨")):
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


    open('./jsons/' + "user_state" + myid + ".json", 'w', encoding='utf-8').write(json.dumps(user_state, ensure_ascii=False))
    open('./jsons/homework' + myid + ".json", 'w', encoding='utf-8').write(json.dumps(homework, ensure_ascii=False))
    open('./jsons/' + "helper" + myid + ".json", 'w', encoding='utf-8').write(json.dumps(helper, ensure_ascii=False))

bot.polling(none_stop=True)
