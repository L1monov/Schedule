import telebot
from telebot import types

admins = [1212477490, 854686840]

def markup_menu(tg_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rasp_week = types.KeyboardButton("Расп. неделя")
    rasp_tomorrow = types.KeyboardButton("🗓Завтра")
    rasp_today = types.KeyboardButton("🗓Сегодня")
    profil = types.KeyboardButton("👤Профиль")
    settings = types.KeyboardButton("⚙️Настройки")
    admin = types.KeyboardButton("⛔️Админ-панель")
    markup.add(rasp_week, rasp_tomorrow, rasp_today)
    if tg_id in admins:
        markup.add(profil, settings, admin)
    else:
        markup.add(profil, settings)
    return markup

def markup_week(type_week):
    if type_week == 'not_even':
        symbol = '⭐️'
    if type_week == 'even':
        symbol = '🌟'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    day_1 = types.KeyboardButton(f"Понедельник{symbol}")
    day_2 = types.KeyboardButton(f"Вторник{symbol}")
    day_3 = types.KeyboardButton(f"Среда{symbol}")
    day_4 = types.KeyboardButton(f"Четверг{symbol}")
    day_5 = types.KeyboardButton(f"Пятница{symbol}")
    day_6 = types.KeyboardButton(f"Суббота{symbol}")
    menu = types.KeyboardButton("Меню")

    markup.add(day_1, day_2, day_3)
    markup.add(day_4, day_5, day_6)
    markup.add(menu)
    return markup

def makup_type_week():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    day_1 = types.KeyboardButton("Чётная неделя")
    day_2 = types.KeyboardButton("Нечётная неделя")
    menu = types.KeyboardButton("Меню")

    markup.add(day_1, day_2)
    markup.add(menu)
    return markup

def marup_profil():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu = types.KeyboardButton("Меню")
    change_group = types.KeyboardButton("Изменить группу")
    markup.add(menu, change_group)
    return markup

def markup_settings():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ofers = types.KeyboardButton("Предложение")
    mistake = types.KeyboardButton("Сообщить об ошибке")
    info = types.KeyboardButton("Информация о боте")
    menu = types.KeyboardButton("Меню")
    markup.add(ofers)
    markup.add(mistake)
    markup.add(info)
    markup.add(menu)
    return markup
