import base64

import requests
from bs4 import BeautifulSoup
import csv

URL_1 = 'https://itmo.ru/ru/personlist'
URL = 'https://itmo.ru/ru/personlist/personalii.htm'
HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
           'accept': '*/*'}#для того что бы сайт не посчитал тебя ботом (примерно так)

HOST = 'https://english.spbstu.ru'
FILE = 'people_itmo.csv'

#выводит статус входа 200 при успехе
def get_html(url, params = None) :
    r = requests.get(url, headers=HEADERS, params=params)
    # print(source.encoding)
    # prints out ISO-8859-1
    r.encoding = 'utf-8'
    return r

#отдельный вывод для инфы в доп старинцы
def hrt_1(html):
    html1 = get_html(html)
    soup1 = BeautifulSoup(html1.text, 'html.parser')
    items = soup1.find_all("dl")

    for item in items:

        test = item.find("dt")
        if (test):

            if test.get_text() == "Должность:":

                item = item.find("dd")

                if item:
                    return  (item.get_text(strip=True))
    return "-"

def hrt_2(html):
    html1 = get_html(html)
    soup1 = BeautifulSoup(html1.text, 'html.parser')
    items = soup1.find_all("dl")

    for item in items:

        test = item.find("dt")
        if (test):
            #print(test)
            if test.get_text() == "Ученое звание:":

                item = item.find("dd")

                if item:
                    return  (item.get_text(strip=True))
    return "-"

def hrt_3(html):
    html1 = get_html(html)
    soup1 = BeautifulSoup(html1.text, 'html.parser')
    items = soup1.find_all("dl")

    for item in items:

        test = item.find("dt")
        if (test):
            #print(test)
            if test.get_text() == "Ученая степень:":

                item = item.find("dd")

                if item:
                    return  (item.get_text(strip=True))
    return "-"

def hrt_4(html):
    html1 = get_html(html)
    soup1 = BeautifulSoup(html1.text, 'html.parser')
    items = soup1.find_all("div", {"class": "tab-pane fade in active"})

    for item in items:

        test = item.find_all("p")
        test1 = item.find("ul")
        for item1 in test:
            if item1.get_text() == "Служебные обязанности" and test1:
                #print(test1.get_text(strip=True))
                return (test1.get_text(strip=True))
        #if (test):
           # return  (test.get_text(strip=True))
    return "-"

def hrt_5(html):
    html1 = get_html(html)
    soup1 = BeautifulSoup(html1.text, 'html.parser')
    items = soup1.find_all("ul", {"class": "contacts rowFlex rowFlex--space"})

    for item in items:

        test = item.find_all("dt")

        for item1 in test:
            if(item1.get_text() == "Почта"):
                return "+"

    return "-"

def hrt_6(html):
    html1 = get_html(html)
    soup1 = BeautifulSoup(html1.text, 'html.parser')
    soup1 = soup1.find("div", {"id": "tabPublications"})
    people = []
    if soup1:
        test = soup1.find_all("div")
        #print(test)
        #print("========================================")
        for item1 in test:
            people.append(item1.get_text(strip=True))
        #print(' '.join(map(str, people)))
        return ' '.join(map(str, people))
    else:
        return "-"

#основой вывод инфы
def get_content(html) :
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("article", {"class": "rowFlex-col"}) # вывод все групп с определеным названием класса "class": "rowFlex-col"

    people = []
    for item in items :# вывод из этих групп интересующей инфы
        people.append({
                'title' : item.find('h4').get_text(strip=True),
                'linck': "https://itmo.ru" + item.find('a').get('href'),

                'Science degree':  hrt_3("https://itmo.ru" + item.find('a').get('href')), #Ученая степень:

                'Science title':  hrt_2("https://itmo.ru" + item.find('a').get('href')),  #Ученое звание:
                'Academic title': "-",
                'Position': hrt_1("https://itmo.ru" + item.find('a').get('href')),               #должность
               'Duties': hrt_4("https://itmo.ru" + item.find('a').get('href')), #обязаности возможный косяк

                'Contact details': hrt_5("https://itmo.ru" + item.find('a').get('href')),

                'titl': hrt_6("https://itmo.ru" + item.find('a').get('href'))

            })#условие title и потом ввод туда инфы

    #print(people)
    return people

#сохраненив в cvs файл
def save_file(items, path) :
    with open(path, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter = ';')
        writer.writerow(['title', 'linck', 'Science degree', 'Science title', 'Position', 'Duties', 'Contact details', 'titl'])
        for item in items:
           # print(item['Duties'])
            writer.writerow(
                [item['title'], item['linck'], item['Science degree'], item['Science title'], item['Position'], item['Duties'],
                 item['Contact details'], item['titl']])

#основной код для парсинга с проверкой на вход в сайт (html.status_code == 200)
def parse() :

    html = get_html(URL)
    print(html.status_code)
    if html.status_code == 200:
        people = []
        for page in range(192, 201):
            print(f'Парсиниг страницы {page} из {201}...')
#
            html = get_html(URL_1 + '/' + str(page) + ' /letter_' + str(page) + '.htm')
            people.extend(get_content(html.text))
            #print(html.text)

        for page in range(202, 218):
            print(f'Парсиниг страницы {page} из {218}...')

            html = get_html(URL_1 + '/' + str(page) + ' /letter_' + str(page) + '.htm')
            people.extend(get_content(html.text))
            #print(html.text)

        for page in range(221, 224):
            print(f'Парсиниг страницы {page} из {223}...')
#
            html = get_html(URL_1 + '/' + str(page) + ' /letter_' + str(page) + '.htm')
            people.extend(get_content(html.text))
            #print(html.text)

        save_file(people, FILE)
        print(f'Получено {len(people)} людей')
    else:
        print('Error')

parse()
