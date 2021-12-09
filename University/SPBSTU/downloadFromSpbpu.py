import base64

import pymongo
import requests
from bs4 import BeautifulSoup
import csv

from pymongo import MongoClient

URL_13 = 'https://imet.spbstu.ru/person/' #промыш менедж
URL_12 = 'https://et.spbstu.ru/person/' #электроники
URL_11 = 'https://immit.spbstu.ru/person/' #машиностроение
URL_10 = 'https://ibmst.spbstu.ru/person/' #биомед сист
URL_9 = 'https://physmech.spbstu.ru/person/' #физико-механ
URL_8 = 'https://ifkst.spbstu.ru/person/' #физ культуры
URL_7 = 'https://ice.spbstu.ru/person/' #инженер-строит
URL_6 = 'https://iets.spbstu.ru/person/' #энергетики
URL_5 = 'https://iamt.spbstu.ru/person/' #передовых произв тех
URL_4 = 'https://ic.spbstu.ru/person/' #кибербез
URL_3 = 'https://hum.spbstu.ru/directorate/'
URL_2 = 'https://icst.spbstu.ru/person/'
URL_1 = 'https://english.spbstu.ru/university/about-the-university/personalities/'
URL = 'https://www.spbstu.ru/university/about-the-university/personalities/'
#HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    #       'accept': '*/*'}

HOST_1 = 'https://icst.spbstu.ru/person/'
HOST = 'https://english.spbstu.ru'
FILE = 'people.csv'

def get_html(url, params = None) :
    r = requests.get(url,  params=params)
    # print(source.encoding)
    # prints out ISO-8859-1
    r.encoding = 'utf-8'
    return r

def get_html1(url, params = None) :
    r = requests.get(url,  params=params)
    # print(source.encoding)
    # prints out ISO-8859-1
    r.encoding = 'utf-8'
    return r


def hrt(html):
    html1 = get_html(html)
    soup1 = BeautifulSoup(html1.text, 'html.parser')
    items = soup1.find_all("div", {"class": "box current"})

    people = []
    for item in items:
       #print(soup1.find_all("div", {"class": "desc"}))
       # people.append({
        if item.find('div'):
        #print((item).get_text(strip=True))
            return item.get_text(strip=True)
        else:
            items1 = soup1.find_all("div", {"class": "desc"})
            for item1 in items1:
                if item1.find("div", {"class": "row"}):
                    return (item1.find("div", {"class": "row"}).get_text(strip=True))




def get_content(html) :
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("div", {"class": "ppl-card"})

    #print(items)
    people = []
    for item in items :

        items1 = item.find_all('div', {"class": "box"})

        for item1 in items1:
            #print(item1.find('div', {"class": "title"}))
            science_degree = item1.find('div', {"class": "title"})
            if science_degree:
                test = science_degree.get_text()
                if test == "Ученая степень":
                    #print(item1.find('div', {"class": "desc"}).get_text())
                    #print(science_degree.find('div', {"class": "desc"}))
                    science_degree = item1.find('div', {"class": "desc"}).get_text()
                    break

            science_degree = '-'

        items1 = item.find_all('div', {"class": "box"})
        for item1 in items1:
            cience_title = item1.find('div', {"class": "title"})
            if cience_title:
                test = cience_title.get_text()
                if test == "Ученое звание":
                    cience_title = item1.find('div', {"class": "desc"}).get_text(strip=True)
                    break

            cience_title = '-'

        items1 = item.find_all('div', {"class": "box"})
        for item1 in items1:
            position = item1.find('div', {"class": "title"})
            if position:
                test = position.get_text()
                if test == "Занимаемые должности":
                    position = item1.find('div', {"class": "desc"}).get_text(strip=True)
                    position_mass = position.split("-", 1) ###########################################
                    position = position_mass[0] ##################################################
                    #print(position)

                    break

            position = '-'
####################################### new kysok
        items1 = item.find_all('div', {"class": "box"})
        for item1 in items1:
            position_mest = item1.find('div', {"class": "title"})
            if position_mest:
                test = position_mest.get_text()
                if test == "Занимаемые должности":
                    position_mest = item1.find('div', {"class": "desc"}).get_text(strip=True)
                    position_mass = position_mest.split("-", 1) ###########################################
                    #print(len(position_mass))
                    if len(position_mass)>1:
                        position_mest = position_mass[1] ##################################################

                        break

            position_mest = '-'
###########################################################################
        items1 = item.find_all('div', {"class": "box"})
        for item1 in items1:
            duties = item1.find('div', {"class": "title"})
            if duties:
                test = duties.get_text()
                if test == "Обязанности":
                    duties = item1.find('div', {"class": "desc"}).get_text(strip=True)

                    break

            duties = '-'

        items1 = item.find_all('div',  {"class": "box"})
        #print(item1)
        for item1 in items1:
            #print(item1.find('a'))
            contact_details = ''
            contact_details = item1.select("ul:nth-of-type(1)")
            #print(contact_details)


            t = contact_details[0].find('a')
            #print(t)
            if t:
                tt = contact_details[0].find('a').get("href")
                if tt[0] != 'h':
                    contact_details = contact_details[0].find('a')
                else:
                    contact_details = item1.select("ul:nth-of-type(2)")
                    contact_details = contact_details[0].find('a')
            else:
                contact_details = item1.select("ul:nth-of-type(2)")
                if contact_details:
                    contact_details = contact_details[0].find('a')
            #print(contact_details)
            if contact_details:

                    contact_details = '+'
                    #print(contact_details)
                    break

            contact_details = '-'
            #print(contact_details)

        titl = hrt(item.find('a').get('href'))
        if titl == None:
            titl = '-'

        people.append({
                'title' : item.find('a').get_text(strip=True),
                'linck': item.find('a').get('href'),

                'Science degree': science_degree,

                'Science title': cience_title,
                #'Academic title': academic_title,
                'Position': position,
	  	        'Position_mest': position_mest,
                'Duties': duties,

                'Contact details': contact_details,

                'titl': titl

            })#условие title и потом ввод туда инфы

    #print(people)
    return people

def insert_document(collection, data):
    """ Function to insert a document into a collection and
    return the document's id.
    """
    return collection.insert_one(data).inserted_id

def find_document(collection, elements, multiple=False):
    """ Function to retrieve single or multiple documents from a provided
    Collection using a dictionary containing a document's elements.
    """
    if multiple:
        results = collection.find()
        return [r for r in results]
    else:
        return collection.find_one()


def save_file(items, path) :
    client = MongoClient('localhost', 27017)


    db = client['SeriesDB']


    series_collection = db['series']




    #with open(path, 'w', newline='', encoding="cp1251") as file:
     #   writer = csv.writer(file, delimiter = ';')
      #  writer.writerow(['title', 'linck', 'Science degree', 'Science title', 'Position', 'Position_mest', 'Duties', 'Contact details', 'titl'])



    for item in items:

        print(item['title'])
        new_show = {
            "title": item['title'],
            "linck": item['linck'],
            "Science degree": item['Science degree'],
            "Science title": item['Science title'],
            "Position": item['Position'],
            "Position_mest": item['Position_mest'],
            "Duties": item['Duties'],
            "Contact details": item['Contact details'],
            "titl":item['titl']
        }

    print(insert_document(series_collection, new_show))

    result = find_document(series_collection, {'title': 'FRIENDS'})
    print(result)
        #     writer.writerow(
        #        [item['title'], item['linck'], item['Science degree'], item['Science title'], item['Position'], item['Position_mest'], item['Duties'],
         #        item['Contact details'], item['titl']])


def parse() :



    html = get_html(URL_13)
    if html.status_code == 200:
        people = []
        for page in range(1, 5):
            print(f'Парсиниг страницы {page} из {65}...')
            html = get_html(URL_13, params={'paging': page})
            people.extend(get_content(html.text))
            #print(html.text)
        save_file(people, FILE)
        print(f'Получено {len(people)} людей')
    else:
        print('Error')

parse()
