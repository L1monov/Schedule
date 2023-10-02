import datetime
import json


info_faculty ={
    1:'Мип',
    2:'ТД',
    3:'КТиИБ',
    4:'УЭФ',
    5:'ЭИФ',
    6:'Юридический факультет',
    7:'ЛиЖ',
}

info_days = {
    0:'Понедельник',
    1:'Вторник',
    2:'Среда',
    3:'Четверг',
    4:'Пятница',
    5:'Суббота'
}
# Поиск инфы о группе , передаёшь ИБ-331 , выдаёт факультет курс и группу
def find_info_for_group(name_group):
    name_group = name_group.upper()
    with open('dict_all_groups.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    if name_group in data:
        list_f_k_g = data[name_group].split(',')
        return (info_faculty[int(list_f_k_g[0])], list_f_k_g[1], name_group)

# Расписание на сегодня
def rasp_today(name_group):
    # Получаем текущую дату
    current_date = datetime.datetime.now()
    # Получаем номер недели для текущей даты
    week_number = current_date.isocalendar()[1]
    # Проверяем, является ли номер недели четным

    if week_number % 2 == 0:
        type_week = 'Чётная неделя'
    else:
        type_week = 'Нечётная неделя'
    day = datetime.datetime.today().weekday()


    if day == 6:
        return 'Пар нет'
    msg = ''
    count = 1
    with open('rasisanie.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    for lesson in data[type_week][name_group][info_days[day]]:
        time_lesson = data[type_week][name_group][info_days[day]][lesson]['time_lesson']
        name_lesson = data[type_week][name_group][info_days[day]][lesson]['name_lesson']
        prepod = data[type_week][name_group][info_days[day]][lesson]['prepod']
        auditorium = data[type_week][name_group][info_days[day]][lesson]['auditorium']
        type_lesson = data[type_week][name_group][info_days[day]][lesson]['type_lesson']
        msg += f"""\n##########\nПара #{count}\n{time_lesson}\n{name_lesson}\n{auditorium}\n{type_lesson}\n{prepod}"""
        count += 1
    return msg

# Расписание на завтра
def rasp_tomorrow(name_group):
    # Получаем текущую дату
    current_date = datetime.datetime.now()
    # Получаем номер недели для текущей даты
    week_number = current_date.isocalendar()[1]
    # Проверяем, является ли номер недели четным

    if week_number % 2 == 0:
        type_week = 'Чётная неделя'
    else:
        type_week = 'Нечётная неделя'

    day = datetime.datetime.today().weekday() + 1

    if day == 6:
        return 'Пар нет'
    if day == 7:
        if type_week == 'Чётная неделя':
            type_week = 'Нечётная неделя'
            day = 0
        if type_week == 'Нечётная неделя':
            type_week = 'Чётная неделя'
            day = 0
    msg = ''
    count = 1
    with open('rasisanie.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    for lesson in data[type_week][name_group][info_days[day]]:
        time_lesson = data[type_week][name_group][info_days[day]][lesson]['time_lesson']
        name_lesson = data[type_week][name_group][info_days[day]][lesson]['name_lesson']
        prepod = data[type_week][name_group][info_days[day]][lesson]['prepod']
        auditorium = data[type_week][name_group][info_days[day]][lesson]['auditorium']
        type_lesson = data[type_week][name_group][info_days[day]][lesson]['type_lesson']
        msg += f"""\n##########\nПара #{count}\n{time_lesson}\n{name_lesson}\n{auditorium}\n{type_lesson}\n{prepod}"""
        count += 1
    return msg

# Расписание на определённые день
def rasp_day(name_group, day, type_week):
    try:
        if type_week == 'even':
            type_week = 'Чётная неделя'
        if type_week == 'not_even':
            type_week = 'Нечётная неделя'

        msg = ''
        count = 1
        with open('rasisanie.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        for lesson in data[type_week][name_group][info_days[day]]:
            time_lesson = data[type_week][name_group][info_days[day]][lesson]['time_lesson']
            name_lesson = data[type_week][name_group][info_days[day]][lesson]['name_lesson']
            prepod = data[type_week][name_group][info_days[day]][lesson]['prepod']
            auditorium = data[type_week][name_group][info_days[day]][lesson]['auditorium']
            type_lesson = data[type_week][name_group][info_days[day]][lesson]['type_lesson']
            msg += f"""\n##########\nПара #{count}\n{time_lesson}\n{name_lesson}\n{auditorium}\n{type_lesson}\n{prepod}"""
            count += 1
        return msg
    except KeyError:
        return 'На этот день пар нет, можно расслабиться'
