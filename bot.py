import telebot
from telebot import types
import config
import db
import defs
import time
import buttons

bot = telebot.TeleBot(config.TOKEN_BOT)

rasp_week = types.KeyboardButton("Расп. неделя")
rasp_tomorrow = types.KeyboardButton("🗓Завтра")
rasp_today = types.KeyboardButton("🗓Сегодня")
profil = types.KeyboardButton("👤Профиль")
settings = types.KeyboardButton("⚙️Настройки")


@bot.message_handler(commands=['veronika'])
def start(message):
    msg = 'Я тебя люблю , моя зайка❤️'
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['admin'])
def start(message):
    tg_id = message.from_user.id
    if tg_id in config.admins:
        msg = 'Добавлена админ панель'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        admin = types.KeyboardButton("⛔️Админ-панель")
        markup.add(rasp_week, rasp_tomorrow, rasp_today)
        markup.add(profil, settings, admin)
        bot.send_message(message.chat.id, msg, reply_markup=markup)
    if tg_id not in config.admins:
        msg = 'Ты не одмен ('
        bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['start'])
def start(message):
    try:
        tg_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        if db.check_user(tg_id) == 'No':
            db.create_user(username, tg_id, first_name, last_name)
            msg = f'Новый пользователь:\nИмя: {first_name}\nID: {tg_id}\nСсылка: https://t.me/{username}'
            rif = 1212477490
            valek = 854686840
            bot.send_message(int(rif), msg)
            bot.send_message(int(valek), msg)
        mesg = bot.send_message(message.chat.id,
                                '👋Привет, я бот-помощник по поиску распписание👋 \n🔍Давай найдём трою группу🔎\n❕(Пример : ИБ-321)❕\nP.S. Бот находится разработке\nБудем благодарны помощи❤️')
        bot.register_next_step_handler(mesg, find_group)
    except Exception as ex:
        print(f'Ошибка в функции start: {ex}')


def new_offer(message):
    try:
        msg = f"Спасибо за предложение❤️"
        db.new_offer(message.from_user.id, message.from_user.username, message.text)
        markup = buttons.markup_menu(message.from_user.id)
        bot.send_message(message.chat.id, msg, reply_markup=markup)
    except Exception as ex:
        print(f'Ошибка в функции new_offer: {ex}')


def new_mistake(message):
    try:
        msg = f"Спасибо за обратную связь❤️"
        db.new_mistake(message.from_user.id, message.from_user.username, message.text)
        markup = buttons.markup_menu(message.from_user.id)
        bot.send_message(message.chat.id, msg, reply_markup=markup)
    except Exception as ex:
        print(f'Ошибка в функции start: {ex}')


def find_group(message):
    try:
        list_f_k_g = defs.find_info_for_group(message.text)
        faculty = list_f_k_g[0]
        kind = list_f_k_g[1]
        group = list_f_k_g[2]
        markup = types.InlineKeyboardMarkup()
        yes = types.InlineKeyboardButton(text='Да, всё верно!', callback_data=f"{'menu'}")
        no = types.InlineKeyboardButton(text='Нет, ты ошибся', callback_data=f"{'wrong_choicec'}")
        markup.add(yes, no)
        db.update_user_info_group(message.from_user.id, message.text)
        msg = f"Кажется я что-то нашёл\nФакультет {faculty} \nКурс {kind}\nГруппа {group}\nЯ правильно нашёл?"
        bot.send_message(message.chat.id, msg, reply_markup=markup)
    except Exception as ex:
        mesg = bot.send_message(message.chat.id, 'Ты ввел что-то неверное , введи еще раз.\n(Пример : ИБ-321)')
        bot.register_next_step_handler(mesg, find_group)


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback(callback):
    try:
        if callback.data == "menu":
            markup = buttons.markup_menu(callback.from_user.id)
            bot.send_message(callback.message.chat.id, 'Главное меню', reply_markup=markup)
        if callback.data == "wrong_choicec":
            mesg = bot.send_message(callback.message.chat.id, 'Поробуй ввести еще раз.\n(Пример ИБ-331)')
            bot.register_next_step_handler(mesg, find_group)
    except Exception as ex:
        print(f'Ошибка в функции check_callback: {ex}')


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Нечётная неделя"):
        markup = buttons.markup_week('not_even')
        bot.send_message(message.chat.id, f"Выберите день", reply_markup=markup)

    if (message.text == "Чётная неделя"):
        markup = buttons.markup_week('even')
        bot.send_message(message.chat.id, f"Выберите день",
                         reply_markup=markup)

    ################### Нечётная неделя ###################
    if (message.text == "Понедельник⭐️"):
        msg = defs.rasp_day(db.get_group_for_tg_id(message.from_user.id), 0, 'not_even')
        bot.send_message(message.chat.id, msg)
    if (message.text == "Вторник⭐️"):
        msg = defs.rasp_day(db.get_group_for_tg_id(message.from_user.id), 1, 'not_even')
        bot.send_message(message.chat.id, msg)
    if (message.text == "Среда⭐️"):
        msg = defs.rasp_day(db.get_group_for_tg_id(message.from_user.id), 2, 'not_even')
        bot.send_message(message.chat.id, msg)
    if (message.text == "Четверг⭐️"):
        msg = defs.rasp_day(db.get_group_for_tg_id(message.from_user.id), 3, 'not_even')
        bot.send_message(message.chat.id, msg)
    if (message.text == "Пятница⭐️"):
        msg = defs.rasp_day(db.get_group_for_tg_id(message.from_user.id), 4, 'not_even')
        bot.send_message(message.chat.id, msg)
    if (message.text == "Суббота⭐️"):
        msg = defs.rasp_day(db.get_group_for_tg_id(message.from_user.id), 5, 'not_even')
        bot.send_message(message.chat.id, msg)
    ################### Нечётная неделя ###################

    ################### Чётная неделя ###################
    if (message.text == "Понедельник🌟"):
        msg = defs.rasp_day(db.get_group_for_tg_id(message.from_user.id), 0, 'even')
        bot.send_message(message.chat.id, msg)
    if (message.text == "Вторник🌟"):
        msg = defs.rasp_day(db.get_group_for_tg_id(message.from_user.id), 1, 'even')
        bot.send_message(message.chat.id, msg)
    if (message.text == "Среда🌟"):
        msg = defs.rasp_day(db.get_group_for_tg_id(message.from_user.id), 2, 'even')
        bot.send_message(message.chat.id, msg)
    if (message.text == "Четверг🌟"):
        msg = defs.rasp_day(db.get_group_for_tg_id(message.from_user.id), 3, 'even')
        bot.send_message(message.chat.id, msg)
    if (message.text == "Пятница🌟"):
        msg = defs.rasp_day(db.get_group_for_tg_id(message.from_user.id), 4, 'even')
        bot.send_message(message.chat.id, msg)
    if (message.text == "Суббота🌟"):
        msg = defs.rasp_day(db.get_group_for_tg_id(message.from_user.id), 5, 'even')
        bot.send_message(message.chat.id, msg)
    ################### Нечётная неделя ###################

    if (message.text == "Информация о боте"):
        bot.send_message(message.chat.id,
                         f"""Бот разработан командой ICM\nСоздатели: Тимошев Рифат и Стокозов Валентин\nВерсия бота: {config.version_bot}""")

    if (message.text == "Расп. неделя"):
        markup = buttons.makup_type_week()
        bot.send_message(message.chat.id, f"Выберите тип недели", reply_markup=markup)

    if (message.text == "🗓Завтра"):
        try:
            msg = defs.rasp_tomorrow(db.get_group_for_tg_id(message.from_user.id))
            bot.send_message(message.chat.id, msg)
        except KeyError:
            bot.send_message(message.chat.id, 'На этот день пар нет, можно расслабиться')

    if (message.text == "🗓Сегодня"):
        try:
            msg = defs.rasp_today(db.get_group_for_tg_id(message.from_user.id))
            bot.send_message(message.chat.id, msg)

        except KeyError:
            bot.send_message(message.chat.id, 'На этот день пар нет, можно расслабиться')

    if (message.text == "Меню"):
        markup = buttons.markup_menu(message.from_user.id)
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=markup)

    if (message.text == "👤Профиль"):
        group = db.get_group_for_tg_id(message.from_user.id)
        markup = buttons.marup_profil()
        bot.send_message(message.chat.id, f"Ваша группа: {group}", reply_markup=markup)

    if (message.text == "Изменить группу"):
        mesg = bot.send_message(message.chat.id, 'Введи группу\n(Пример : ИБ-321)')
        bot.register_next_step_handler(mesg, find_group)

    if (message.text == "⚙️Настройки"):
        markup = buttons.markup_settings()
        bot.send_message(message.chat.id, f"Настройки", reply_markup=markup)

    if (message.text == "Предложение"):
        mesg = bot.send_message(message.chat.id, 'Введите Ваше предложение')
        bot.register_next_step_handler(mesg, new_offer)

    if (message.text == "Сообщить об ошибке"):
        mesg = bot.send_message(message.chat.id, 'Введите ошибку')
        bot.register_next_step_handler(mesg, new_mistake)

    if (message.text == "⛔️Админ-панель"):
        tg_id = message.from_user.id
        if tg_id in config.admins:
            msg = f'Всего пользователей: {db.get_count_users()}'
            bot.send_message(message.chat.id, msg)
        if tg_id not in config.admins:
            msg = 'Ты не одмен ('
            bot.send_message(message.chat.id, msg)


if __name__ == '__main__':
    while True:
        try:
            print('bot rolling')
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(2)
            print(e)
