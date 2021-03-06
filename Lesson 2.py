# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или
# через аргументы) с сайта superjob.ru и hh.ru. Приложение должно анализировать несколько страниц
# сайта(также вводим через input или аргументы). Получившийся список должен содержать в себе
# минимум:
# *Наименование вакансии
# *Предлагаемую зарплату (отдельно мин. и и отдельно макс.)
# *Ссылку на саму вакансию
# *Сайт откуда собрана вакансия
# По своему желанию можно добавить еще работодателя и расположение. Данная структура должна
# быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью
# dataFrame через pandas.


from bs4 import BeautifulSoup as bs
import requests
import re
import time
import random
import pandas as pd
from pprint import pprint

# search = input('Введите вакансию для поиска: ').replace(' ', '+')
search = 'python'

main_link = 'https://hh.ru'
link = main_link + '/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=' + search

print(link)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

html = requests.get(link, headers=headers).text
parsed_html = bs(html, 'lxml')

next_pager = parsed_html.find('a', {'data-qa': 'pager-next'})

i = 0
time_sleep = [0.1, 1, 0.5, 2, 0.8, 3, 1]
vacancies = []

while next_pager:
    i += 1
    print(i)
    link = main_link + next_pager['href']

    time.sleep(random.choice(time_sleep))

    html = requests.get(link, headers=headers).text
    parsed_html = bs(html, 'lxml')

    vacancy_bloc = parsed_html.find('div', {'class': 'vacancy-serp'})

    try:
        vacancy_list = vacancy_bloc.find_all('div', {'class': ['vacancy-serp-item', 'vacancy-serp-item_premium']})
    except:
        print('++++++++++')

    next_pager = parsed_html.find('a', {'data-qa': 'pager-next'})

    for vacancy in vacancy_list:

        vacancy_data = dict()

        vacancy_info = vacancy.find('a')

        vacancy_name = vacancy_info.getText()
        vacancy_link = vacancy_info['href']

        pay_currency = None
        pay_min = None
        pay_max = None

        try:

            vacancy_pay = vacancy.find('div', {'class': 'vacancy-serp-item__compensation'}).getText()

            if vacancy_pay:

                if not vacancy_pay.split()[-1].isdigit():
                    pay_currency = vacancy_pay.split()[-1]
                    vacancy_pay = vacancy_pay[:-len(pay_currency)]

                if re.search('-', vacancy_pay):
                    pay = vacancy_pay.split('-')
                    pay_min = int(pay[0].replace('\xa0', ''))
                    pay_max = int(pay[1].replace('\xa0', ''))

                elif re.search('от', vacancy_pay):
                    pay_min = int(vacancy_pay[3:].replace('\xa0', ''))

                elif re.search('до', vacancy_pay):
                    pay_max = int(vacancy_pay[3:].replace('\xa0', ''))

        except:
            pass

        site = 'hh.ru'

        vacancy_data['name'] = vacancy_name
        vacancy_data['site'] = site
        vacancy_data['link'] = vacancy_link
        vacancy_data['pay_currency'] = pay_currency
        vacancy_data['pay_min'] = pay_min
        vacancy_data['pay_max'] = pay_max

        vacancies.append(vacancy_data)


print(i, len(vacancies))
df = pd.DataFrame(vacancies)
df.to_csv('test.csv')
# pprint(vacancies)