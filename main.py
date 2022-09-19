import requests
from bs4 import BeautifulSoup

hh_url = 'https://spb.hh.ru/search/vacancy?text=javaScript&items_on_page=100'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/71.0.3542.0 Safari/537.36',
}
hh_req = requests.get(hh_url, headers=headers)
hh_soup = BeautifulSoup(hh_req.text, 'html.parser')

#Находим блок с пагинацией
# Если есть возможность, то можно найти непосрественно элементы
# hh_pagination = hh_soup.find_all('span', {'class': 'pager-item-not-in-short-range'})
hh_pagination = hh_soup.find('div', {'class': 'bloko-gap bloko-gap_top'}).find_all('a', {'class': 'bloko-button'})

# В блоке с пагинацие ищем все ссылки на страницы
# pages = hh_pagination.find_all('a')
hh_pages = []

#Кусок черной магии. Так и не понял, как это сработало.
for page in hh_pagination:
    hh_pages.append(page.text)

hh_pages.pop() #удаляем слово далее
hh_pages = [int(x) for x in hh_pages] #переводим список из строк в числа
max_page = hh_pages[-1] #забираем последний элемент списка в котором указана последняя страница


print(max_page)
