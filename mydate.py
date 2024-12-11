import datetime

# получение даты по номеру дня
def get_day_by_number(number) -> str:  # 0 - вс
    current_time = datetime.datetime.today()
    weekday = current_time.weekday()
    if weekday == 6:
        ans_time = datetime.datetime.today() + datetime.timedelta(days=number)
    else:
        x = weekday - number + 1
        if x >= 0:
            ans_time = datetime.datetime.today() - datetime.timedelta(days=x)
        else:
            ans_time = datetime.datetime.today() + datetime.timedelta(days=abs(x))
    year = str(ans_time.year)
    month = str(ans_time.month)
    day = str(ans_time.day)
    if len(month) < 2:
        month = str("0" + month)
    if len(day) < 2:
        day = str("0" + day)
    return str(day + "." + month + "." + year)

# проверка даты на корректность
def is_good_date(date: datetime) -> bool:
    try:
        if len(date) != 10:
            return False
        if date[2] != '.' or date[5] != '.' or len(date.split('.')) != 3:
            return False
        day = int(date.split('.')[0])
        month = int(date.split('.')[1])
        year = int(date.split('.')[2])
        date_obj = datetime.datetime(year, month, day)
        if month == 2:
            if year % 400 == 0 or year % 100 != 0 and year % 4 == 0:
                if 1 <= day <= 29 and date_obj.weekday() != 6:
                    return True
                else:
                    return False
            else:
                if 1 <= day <= 28 and date_obj.weekday() != 6:
                    return True
                else:
                    return False
        elif month in [4, 6, 9, 11]:
            if 1 <= day <= 30 and date_obj.weekday() != 6:
                return True
            else:
                return False
        elif month in [1, 3, 5, 7, 8, 10, 12]:
            if 1 <= day <= 31 and date_obj.weekday() != 6:
                return True
            else:
                return False
    except:
        return False


# получение номера по дате
def get_number_by_date(cur_date: datetime):  # 0 - пн
    date = str(cur_date)
    year = int(date[6:10])
    month = int(date[3:5])
    day = int(date[0:2])
    date_obj = datetime.datetime(year, month, day)
    return date_obj.weekday()

