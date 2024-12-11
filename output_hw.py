import json
import datetime
from telebot import types
import mydate

# вывод дз
def print_text(bot, message, day, prof, subject):
    homework = json.loads(open('./jsons/homeworks.json', 'r', encoding='utf-8').read())
    user_state = json.loads(open('./jsons/users_states.json', 'r', encoding='utf-8').read())
    hw = homework[day][prof]["texts"][subject]
    bot.send_message(message.chat.id,
                     text="<b> <u>" + (json.dumps(subject, ensure_ascii=False).format(message.from_user)).strip(
                         '"') + "</u></b>" + ": " + (
                              json.dumps(hw, ensure_ascii=False).format(message.from_user)).strip('"'),
                     parse_mode='HTML')


def print_photo(bot, message, day, prof, subject):
    homework = json.loads(open('./jsons/homeworks.json', 'r', encoding='utf-8').read())
    user_state = json.loads(open('./jsons/users_states.json', 'r', encoding='utf-8').read())
    if subject in homework[day][prof]["im"].keys():
        cnt = 1
        for photo in homework[day][prof]["im"][subject]:
            bot.send_photo(message.chat.id, photo=open("./photos/" + photo, 'rb').read())
            cnt += 1


def print_profile(bot, message, day, prof):
    homework = json.loads(open('./jsons/homeworks.json', 'r', encoding='utf-8').read())
    user_state = json.loads(open('./jsons/users_states.json', 'r', encoding='utf-8').read())
    for subject in homework[day][prof]["texts"]:
        print_text(bot, message, day, prof, subject)
        print_photo(bot, message, day, prof, subject)


def print_homework(bot, message, day):
    homework = json.loads(open('./jsons/homeworks.json', 'r', encoding='utf-8').read())
    user_state = json.loads(open('./jsons/users_states.json', 'r', encoding='utf-8').read())
    if not mydate.is_good_date(day):
        bot.send_message(message.chat.id, text="Введена некорректная дата.", parse_mode='HTML')
    else:
        if not (day in homework.keys()):
            homework[day] = {"both": {"texts": {}, "im": {}}, "inf": {"texts": {}, "im": {}},
                             "mat": {"texts": {}, "im": {}}}
        if len(homework[day]["both"]["texts"]) == 0 and len(homework[day]["inf"]["texts"]) == 0 and len(
                homework[day]["mat"]["texts"]) == 0:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_start_1 = types.KeyboardButton("Домашнее задание📚")
            btn_start_admin_1 = types.KeyboardButton("✨Редактировать домашнее задание✨")
            btn_start_2 = types.KeyboardButton("Музыка")
            btn_start_3 = types.KeyboardButton("Мемы")

            markup.add(btn_start_1, btn_start_admin_1)
            markup.add(btn_start_2, btn_start_3)
            user_state[str(message.chat.id)] = 'main menu'
            bot.send_message(message.chat.id,
                             text="<b> <i>Никому ничего не задали😁</i> </b>", parse_mode='HTML',
                             reply_markup=markup)
            if day in homework.keys():
                del homework[day]
        else:
            if len(homework[day]["both"]["texts"]) != 0:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn_start_1 = types.KeyboardButton("Домашнее задание📚")
                btn_start_admin_1 = types.KeyboardButton("✨Редактировать домашнее задание✨")
                btn_start_2 = types.KeyboardButton("Музыка")
                btn_start_3 = types.KeyboardButton("Мемы")

                markup.add(btn_start_1, btn_start_admin_1)
                markup.add(btn_start_2, btn_start_3)
                user_state[str(message.chat.id)] = 'main menu'
                print_profile(bot, message, day, "both")


def print_week(bot, message):
    homework = json.loads(open('./jsons/homeworks.json', 'r', encoding='utf-8').read())
    user_state = json.loads(open('./jsons/users_states.json', 'r', encoding='utf-8').read())
    number = datetime.datetime.today().weekday()
    for i in range(number % 6, 6):
        if i == 0:
            bot.send_message(message.chat.id, text="<b> ДЗ НА ПОНЕДЕЛЬНИК: </b>",
                                      parse_mode='HTML'), print_homework(bot, message, mydate.get_day_by_number(i + 1))
        if i == 1:
            bot.send_message(message.chat.id, text="<b> ДЗ НА ВТОРНИК: </b>",
                                      parse_mode='HTML'), print_homework(bot, message, mydate.get_day_by_number(i + 1))
        if i == 2:
            bot.send_message(message.chat.id, text="<b> ДЗ НА СРЕДУ: </b>",
                                      parse_mode='HTML'), print_homework(bot, message, mydate.get_day_by_number(i + 1))
        if i == 3:
            bot.send_message(message.chat.id, text="<b> ДЗ НА ЧЕТВЕРГ: </b>",
                                      parse_mode='HTML'), print_homework(bot, message, mydate.get_day_by_number(i + 1))
        if i == 4:
            bot.send_message(message.chat.id, text="<b> ДЗ НА ПЯТНИЦУ: </b>",
                                      parse_mode='HTML'), print_homework(bot, message, mydate.get_day_by_number(i + 1))
        if i == 5:
            bot.send_message(message.chat.id, text="<b> ДЗ НА СУББОТУ: </b>",
                                      parse_mode='HTML'), print_homework(bot, message, mydate.get_day_by_number(i + 1))
