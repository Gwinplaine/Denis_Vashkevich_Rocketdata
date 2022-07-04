from bs4 import BeautifulSoup
import requests
import json

url = 'https://dobronom.by/about/'
header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

session = requests.Session()
session.headers = header

page = session.get(url)

# применение BeautifulSoup к переменной page
data = BeautifulSoup(page.text, 'html.parser')

# поиск 8 элемента втэге script, в нем содержится информация о магазинах и приведение к виду словаря
scrp = data.find_all('script')[7]

scrp = scrp.text.strip().replace('var shopJson = [', '')

scrp = scrp[:scrp.index(']')]

shops_info = eval(scrp)

# пустой список для внесения в него результатов
dobronom_final_list = []

# счётчик порядкового номера магазина
number = 0

# итерация по каждому магазину, приведение в нужный формат и внесение в итоговый список
for shop in shops_info:
    number += 1
    final_voc = {"Number": number, "Shop type": shop['shop_type'], "Area": shop['oblast'], "City": shop['city'],
                 "Address": shop['shop_name'], "Working hours": shop['time'],
                 "Coordinates": shop['map']}
    dobronom_final_list.append(final_voc)

# сохранение результирующего списка в json-файл
with open('dobronom.json', 'w', encoding='utf-8') as file:
    json.dump(dobronom_final_list, file, ensure_ascii=False)

