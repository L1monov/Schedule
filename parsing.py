import requests
from bs4 import BeautifulSoup
import json

cookies = {
    'BITRIX_SM_GUEST_ID': '4463089',
    '_ym_uid': '1693307437682557780',
    '_ym_d': '1693307437',
    'BITRIX_CONVERSION_CONTEXT_s1': '%7B%22ID%22%3A11%2C%22EXPIRE%22%3A1693429140%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D',
    '_ym_isad': '1',
    'PHPSESSID': 'ZlgiB0X7JKlmRJnKkC4w6yw5Tg0IZetV',
    'BITRIX_SM_LAST_VISIT': '30.08.2023%2015%3A41%3A02',
    'BITRIX_SM_LAST_ADV': '7',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'BITRIX_SM_GUEST_ID=4463089; _ym_uid=1693307437682557780; _ym_d=1693307437; BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A11%2C%22EXPIRE%22%3A1693429140%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; _ym_isad=1; PHPSESSID=ZlgiB0X7JKlmRJnKkC4w6yw5Tg0IZetV; BITRIX_SM_LAST_VISIT=30.08.2023%2015%3A41%3A02; BITRIX_SM_LAST_ADV=7',
    'Origin': 'https://rsue.ru',
    'Referer': 'https://rsue.ru/raspisanie/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.3.823 Yowser/2.5 Safari/537.36',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "YaBrowser";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data_uuid = {
    1: 'q',
    2: 'qw',
    3: 'qwe',
    4: 'qwer',
    5: 'qwert',
    6: 'qwerty',
    7: 'qwertyu',
    8: 'qwertyui',
    9: 'qwertyuio',
    10:'qwertyuiop',
    11:'qwertyuiopa',
    12:'qwertyuiopas',
    13:'qwertyuiopasd',
    14:'qwertyuiopasdf',
    15:'qwertyuiopasdfg',
}


groups = []
groups_nice ={}
group_for_find = {}




# парсинг групп и помещение их в список
def group():
    for f in range(1,8):

        groups_nice[f] = {}
        if f in [1,2,6]:
            max_k = 6
        else:
            max_k = 5
        for k in range (1, max_k):

            groups_nice[f][k] = {}
            for g in range(1,15):


                data = {
                    'f': f,
                    'k': k,
                    'g': g,
                    'uuid': data_uuid[g],
                }
                res = requests.post('https://rsue.ru/raspisanie/',
                                                    cookies=cookies,
                                                    headers=headers,
                                                    data=data,
                                                    verify=False)

                result = res.text
                soup = BeautifulSoup(result, 'lxml')
                group = soup.find('h1')
                if group != None:
                    group = group.text.split('Группа ')[1]
                    groups.append(group)
                    groups_nice[f][k][g] = group
                    group_for_find[group] = f"{f},{k},{g}"
    with open('dict_group1.json', 'w', encoding='utf-8') as file:
        json.dump(groups_nice, file, indent=4, ensure_ascii=False)

    with open('dict_all_groups.json', 'w', encoding='utf-8') as file:
        json.dump(group_for_find, file, indent=4, ensure_ascii=False)
    return groups_nice # по
# Парсинг расписание на не чётную неделю , даёшь групппу получаешь расписание на неделю
def raspisanie_group_not_even(name_group):
    rasp_group = {}
    try:

        with open('dict_all_groups.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        list_f_k_g = data[f"{name_group}"].split(',')
        f = list_f_k_g[0]
        k = list_f_k_g[1]
        g = list_f_k_g[2]
        data = {
            'f': f,
            'k': k,
            'g': g,
            'uuid': data_uuid[int(g)],
        }
        res = requests.post('https://rsue.ru/raspisanie/',
                                            cookies=cookies,
                                            headers=headers,
                                            data=data,
                                            verify=False)

        result = res.text
        soup = BeautifulSoup(result, 'lxml')
        days = soup.find_all('div', {'class': 'container'})
        days = days[-1]
        days = days.find('div',{'class':'row'}).find_all('div', {'class':'col-lg-2 col-md-2 col-sm-2'})


        for day in days :
            name_day = day.find('div',{'class':'col-lg-12'})
            if name_day != None:
                rasp_group[name_day.text] = {}
            try:
                all_lesson = day.find_all('div', {'class':'col-lg-12 day'})
                count = 1
                for lesson in all_lesson:
                    rasp_group[name_day.text][count] = {}
                    time = lesson.find('span', {'class':'time'}).text
                    name_lesson = lesson.find('span', {'class':'lesson'}).text
                    prepod = lesson.find('span', {'class':'prepod'}).text
                    auditorium = lesson.find_all('span', {'class': 'aud'})[-1].text
                    type_lesson = lesson.find('span', {'class', 'type n-type'}).text
                    rasp_group[name_day.text][count] = {
                                                'name_lesson': name_lesson,
                                                'time_lesson': time,
                                                'prepod': prepod,
                                                'auditorium': auditorium,
                                                'type_lesson': type_lesson,
                                                    }
                    count = count + 1
            except IndexError:
                print(f'Нет пар')
    except Exception as ex:
        print(ex)
    return rasp_group
# Парсинг на чётную неделю , даёшь номер группу получаешь на неедлю расписание
def raspisanie_group_even(name_group):
    rasp_group = {}
    try:
        with open('dict_all_groups.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        list_f_k_g = data[f"{name_group}"].split(',')
        f = list_f_k_g[0]
        k = list_f_k_g[1]
        g = list_f_k_g[2]
        data = {
            'f': f,
            'k': k,
            'g': g,
            'uuid': data_uuid[int(g)],
        }
        res = requests.post('https://rsue.ru/raspisanie/',
                                            cookies=cookies,
                                            headers=headers,
                                            data=data,
                                            verify=False)

        result = res.text
        soup = BeautifulSoup(result, 'lxml')
        days = soup.find_all('div', {'class': 'container'})
        days = days[-1]
        days = days.findAllNext('h1')[-1]
        days = days.findNext('div')
        for day in days:
            name_day = day.find('div', {'class': 'col-lg-12'})
            if name_day != None:
                rasp_group[name_day.text] = {}
            try:
                all_lesson = day.find_all('div', {'class': 'col-lg-12 day'})
                count = 1
                for lesson in all_lesson:
                    rasp_group[name_day.text][count] = {}
                    time = lesson.find('span', {'class': 'time'}).text
                    name_lesson = lesson.find('span', {'class': 'lesson'}).text
                    prepod = lesson.find('span', {'class': 'prepod'}).text
                    auditorium = lesson.find_all('span', {'class': 'aud'})[-1].text
                    type_lesson = lesson.find('span', {'class', 'type n-type'}).text
                    rasp_group[name_day.text][count] = {
                        'name_lesson': name_lesson,
                        'time_lesson': time,
                        'prepod': prepod,
                        'auditorium': auditorium,
                        'type_lesson': type_lesson,
                    }
                    count = count + 1

            except IndexError:
                print(f'Нет пар')
    except Exception as ex:
        print(ex)
    return rasp_group


# МЕН-133 нет пар почему то )

if __name__ == '__main__':
    raspisanie ={}
    raspisanie['Нечётная неделя'] = {}
    with open('dict_all_groups.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    for i in data:
        print(f"-Группа {i} записывается")
        raspisanie['Нечётная неделя'][i] = raspisanie_group_not_even(i)
        print(f"+Группа {i} записана")
    raspisanie['Чётная неделя'] = {}
    for i in data:
        print(f"-Группа {i} записывается")
        raspisanie['Чётная неделя'][i] = raspisanie_group_even(i)
        print(f"+Группа {i} записана")
    with open('rasisanie.json', 'w', encoding='utf-8') as file:
        json.dump(raspisanie, file, indent=4, ensure_ascii=False)