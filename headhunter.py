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

    # Находим блок с пагинацией
    # Если есть возможность, то можно найти непосрественно элементы
    # hh_pagination = hh_soup.find_all('span', {'class': 'pager-item-not-in-short-range'})
    hh_pagination = hh_soup.find('div', {'class': 'bloko-gap bloko-gap_top'}).find_all('a', {'class': 'bloko-button'})

    # В блоке с пагинацией ищем все ссылки на страницы
    # pages = hh_pagination.find_all('a')
    hh_pages = []

    # Кусок черной магии. Так и не понял, как это сработало.
    for page in hh_pagination:
        hh_pages.append(page.text)

    hh_pages.pop()  # удаляем слово далее
    hh_pages = [int(x) for x in hh_pages]  # переводим список из строк в числа
    return hh_pages[-1]  # забираем последний элемент списка в котором указана последняя страница
    # это и будет агрументом для функции которая проходит по всем страницам


def extract_job(html):  # Создали функцию чтобы код был более читаемым. Функция работает с блоком описания вакансии
    link = html.find('a')['href']  # получаем значение по атрибуту
    title_job = html.find('a').text  # текст заголовка
    # company_name в переменой храним все названия компании из вакансии
    company_name = html.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).find('a').text
    company_name = company_name.strip()
    location = html.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text  # поиск тега по атрибуту
    location = location.partition(',')[0]  # разбиваем строку с адресом и забираем только город
    # функция возвращает словарь где хранятся названия вакансии, название компании
    return {'title': title_job, 'company': company_name, 'location': location, 'link': link}


# Функция по сбору вакансий со страницы
def extract_block_vacancy(last_page):
    jobs = []
    for page in range(last_page):  # находим все страницы
        print(f"парсинг страницы {page}")
        result = requests.get(f'{hh_url}&page={page}', headers=headers)  # находим все страницы
        soup = BeautifulSoup(result.text, 'html.parser')  # парсим полученные страницы
        results_head = soup.find_all('div', {"class": 'vacancy-serp-item-body'})  # находим все блоки с заголовками

        # В блоках находим все заголовки. Каждая переменная result содержит в себе блок вакансии
        for result_block_vacancy in results_head:
            job = extract_job(result_block_vacancy)
            jobs.append(job)  # добавляем каждый словарь в список

    return jobs


def hh_get_jobs():
    hh_max_page = extract_max_page()
    hh_jobs = extract_block_vacancy(2)  # результат присвоили в переменную чтобы вывести его
    return hh_jobs
