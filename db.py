import  pymysql
from config import db_name, password, host,user
import datetime
# Создаёт таблицу логов
def create_table_log():
    conn = pymysql.connect(host=host, user=user, password=password,  db=db_name)
    cursor = conn.cursor()
    cursor.execute(
        f"""show tables"""
    )

    tables = cursor.fetchall()
    tables_names = [database[0] for database in tables]
    if 'log' in tables_names:
        print('Таблица log уже создана')
    else:

        cursor.execute(
            f"""
                    CREATE TABLE log
                            (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                username VARCHAR(255) NOT NULL,
                                text VARCHAR(255) NOT NULL,
                                `time` VARCHAR(255) NOT NULL);"""
        )
        conn.commit()
        # закрываем соединение
        conn.close()
        print('Таблица log создана')
# Создание таблицуы юзеров
def create_table_user():
    conn = pymysql.connect(host=host, user=user, password=password,  db=db_name)
    cursor = conn.cursor()
    cursor.execute(
        f"""show tables"""
    )
    tables = cursor.fetchall()
    tables_names = [database[0] for database in tables]
    print(tables_names)
    if 'user' in tables_names:
        print('Таблица user уже создана')
    else:

        cursor.execute(
            f"""
                    CREATE TABLE user
                            (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                username VARCHAR(255) NOT NULL,
                                tg_id VARCHAR(255) NOT NULL,
                                first_name VARCHAR(255) NOT NULL,
                                last_name VARCHAR(255) NOT NULL,
                                `group` VARCHAR(255));"""
        )
        conn.commit()
        # закрываем соединение
        conn.close()
        print('Таблица user создана')
# Создание таблицы ошибок
def create_table_mistake():
    conn = pymysql.connect(host=host, user=user, password=password,  db=db_name)
    cursor = conn.cursor()
    cursor.execute(
        f"""show tables"""
    )

    tables = cursor.fetchall()
    tables_names = [database[0] for database in tables]
    if 'mistake' in tables_names:
        print('Таблица mistake уже создана')
    else:
        cursor.execute(
            f"""
                    CREATE TABLE mistake
                            (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                username VARCHAR(255) NOT NULL,
                                tg_id VARCHAR(255) NOT NULL,
                                mistake VARCHAR(255) NOT NULL,
                                time_mess VARCHAR(255) NOT NULL)
                                """
        )
        conn.commit()
        # закрываем соединение
        conn.close()
        print('Таблица mistake создана')
# Создание таблицы предложений
def create_table_offer():
    conn = pymysql.connect(host=host, user=user, password=password,  db=db_name)
    cursor = conn.cursor()
    cursor.execute(
        f"""show tables"""
    )

    tables = cursor.fetchall()
    tables_names = [database[0] for database in tables]
    if 'offer' in tables_names:
        print('Таблица offer уже создана')
    else:
        cursor.execute(
            f"""
                    CREATE TABLE offer
                            (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                username VARCHAR(255) NOT NULL,
                                tg_id VARCHAR(255) NOT NULL,
                                offer VARCHAR(255) NOT NULL,
                                time_mess VARCHAR(255) NOT NULL)
                                """
        )
        conn.commit()
        # закрываем соединение
        conn.close()
        print('Таблица offer создана')
# Создание базы данных
def create_db():
    conn = pymysql.connect(host=host, user=user, password=password)
    cursor = conn.cursor()
    cursor.execute(
        f"""show databases"""
    )

    databases = cursor.fetchall()
    database_names = [database[0] for database in databases]
    if 'icm' in database_names:
        print('База ICM уже создана')
    else:
        # устанавливаем соединение
        conn = pymysql.connect(host=host, user=user, password=password)
        cursor = conn.cursor()

        cursor.execute(
            f"""CREATE DATABASE icm"""
        )
        conn.commit()

        #закрываем соединение
        conn.close()
        print('База ICM создана')
# Создание нового пользователя
def create_user(username,tg_id, first_name, last_name):
    conn = pymysql.connect(host=host, user=user, password=password, db=db_name)
    cursor = conn.cursor()
    cursor.execute(
        f"""INSERT INTO `user` (`username`, `tg_id`,`first_name`, `last_name`, `group`)
            VALUES ('{username}', '{tg_id}','{first_name}', '{last_name}', NULL);"""
    )

    conn.commit()
    # закрываем соединение
    conn.close()
# Проверка есть ли человек в базе
def check_user(tg_id):
    conn = pymysql.connect(host=host, user=user, password=password, db=db_name)
    cursor = conn.cursor()
    cursor.execute(
        f"""SELECT tg_id
            from user
            where tg_id = {tg_id}"""
    )
    # кладем результат в кортеж
    result_set = cursor.fetchall()
    tg_ids = [ids[0] for ids in result_set]
    tg_id = str(tg_id)
    if tg_id in tg_ids:
        return 'Yes'
    if tg_id not in tg_ids:
        return 'No'
    # закрываем соединение
    conn.close()
# Обновляет информацию о группе
def update_user_info_group(tg_id, name_group):
    name_group = name_group.upper()
    conn = pymysql.connect(host=host, user=user, password=password, db=db_name)
    cursor = conn.cursor()
    tg_id = str(tg_id)
    cursor.execute(
        f"""update `user` set `group` = '{name_group}'
            where `tg_id` = '{tg_id}'"""
    )

    conn.commit()
    # закрываем соединение
    conn.close()
# Заносит запись о новой ошибке
def new_mistake(tg_id,username, mistake):
    time = datetime.datetime.now()
    conn = pymysql.connect(host=host, user=user, password=password, db=db_name)
    cursor = conn.cursor()
    cursor.execute(
        f"""INSERT INTO `mistake` (`username`, `tg_id`, `mistake`, `time_mess`)
                VALUES ('{username}', '{tg_id}', '{mistake}', '{time}');"""
    )

    conn.commit()
    # закрываем соединение
    conn.close()
# Заносит запись о новом предложении
def new_offer(tg_id,username, offer):
    time = datetime.datetime.now()
    conn = pymysql.connect(host=host, user=user, password=password, db=db_name)
    cursor = conn.cursor()
    cursor.execute(
        f"""INSERT INTO `offer` (`username`, `tg_id`,`offer`, `time_mess`)
                VALUES ('{username}', '{tg_id}','{offer}', '{time}');"""
    )

    conn.commit()
    # закрываем соединение
    conn.close()
# Получить группу по  айти пользователя , даёт тг айди , получаешь группу человека
def get_group_for_tg_id(tg_id):
    conn = pymysql.connect(host=host, user=user, password=password, db=db_name)
    cursor = conn.cursor()
    cursor.execute(
        f"""SELECT `group`
                from user
                where tg_id = {tg_id}"""
    )
    # кладем результат в кортеж
    result_set = cursor.fetchall()

    return result_set[0][0]
    # закрываем соединение
    conn.close()
# Получение количества пользователей
def get_count_users():
    conn = pymysql.connect(host=host, user=user, password=password, db=db_name)
    cursor = conn.cursor()
    query = f"SELECT  * FROM `user`"
    cursor.execute(query)
    rows = cursor.fetchall()
    return (len(rows))
    # кладем результат в кортеж

    # закрываем соединение
    conn.close()

if __name__ == '__main__':
    # create_db()
    create_table_user()
    create_table_log()
    create_table_mistake()
    create_table_offer()

