from bs4 import BeautifulSoup
import geocoder
import requests
import json

# сохранение URL в переменной url
url = 'https://monomax.by/map'

# отправка GET-запроса на сайт и сохранение полученного в переменной page
page = requests.get(url, verify=False)

# применение BeautifulSoup к переменной page
data = BeautifulSoup(page.text, 'html.parser')

# поиск всех вхождений тэга p с классом name - в них содержится адрес 
alladresses = data.findAll('p', class_='name')
# поиск всех вхождений тэга p с классом phone - в них содержится телефон 
allphones = data.findAll('p', class_='phone')

# удаление пустых элементов
del allphones[2]
del allphones[1]

# создание результирующего элемента
result = [{"address": alladresses[i].text, "latlon": geocoder.arcgis('Минск, '+alladresses[i].text).latlng, "name": "Мономах",
    "phones": [allphones[i].text]} for i in range(0,len(alladresses))]

# сохранение результирующего элемента в json-файл
with open ('monomax.json', 'w', encoding='utf-8') as file:
    json.dump(result, file, ensure_ascii=False)
