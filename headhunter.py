import requests
from bs4 import BeautifulSoup

ITEMS = 100
SEARCH_VACANCY = "javaScript"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 YaBrowser/20.6.0.905 Yowser/2.5 Yptp/1.23 Safari/537.36',
}
hh_url = f'https://spb.hh.ru/search/vacancy?text={SEARCH_VACANCY}&items_on_page={ITEMS}'

def extract_max_page():
    hh_req = requests.get(hh_url, headers=headers)
    hh_soup = BeautifulSoup(hh_req.text, 'html.parser')

    #Находим блок с пагинацией
    # Если есть возможность, то можно найти непосрественно элементы
    # hh_pagination = hh_soup.find_all('span', {'class': 'pager-item-not-in-short-range'})
    hh_pagination = hh_soup.find('div', {'class': 'bloko-gap bloko-gap_top'}).find_all('a', {'class': 'bloko-button'})

    # В блоке с пагинацией ищем все ссылки на страницы
    # pages = hh_pagination.find_all('a')
    hh_pages = []

    #Кусок черной магии. Так и не понял, как это сработало.
    for page in hh_pagination:
        hh_pages.append(page.text)

    hh_pages.pop() #удаляем слово далее
    hh_pages = [int(x) for x in hh_pages] #переводим список из строк в числа
    return hh_pages[-1] #забираем последний элемент списка в котором указана последняя страница
                        #это и будет агрументом для функции которая проходит по всем страницам


#Функция по сбору вакансий со страницы
def extract_text_vacancy(last_page):
    jobs = []
    # for page in range(last_page):  # находим все страницы
    result = requests.get(f'{hh_url}&page=0', headers=headers)# находим все страницы
    soup = BeautifulSoup(result.text, 'html.parser') #парсим полученные страницы
    results_head = soup.find_all('div', {"class": 'vacancy-serp-item-body'}) #находим все блоки с заголовками
    # results_body = soup.find_all('div', {"class": 'vacancy-serp-item__info'})
    # print(results_body)

    for result in results_head: #В блоках находим все заголовки
        title_job = (result.find('a').text) #текст заголовка
        print(title_job)

    return jobs