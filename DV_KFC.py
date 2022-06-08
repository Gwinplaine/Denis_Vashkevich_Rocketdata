from bs4 import BeautifulSoup
import json
import requests

# пустой список для внесения результатов по каждому ресторану
KFC_final_list = []
# пустой список для проверки повторения одного и того же ресторана
KFC_names_check = []

# итерирование по url ресторанов
for i in range(1,2000):
    # сохранение URL в переменной url + /номер ресторана
    url = 'https://www.kfc.ru/restaurants/' + str(i)

    # отправка GET-запроса на сайт и сохранение полученного в переменной page
    page = requests.get(url)

    # применение BeautifulSoup к переменной page
    data = BeautifulSoup(page.text, 'html.parser')
    
    # присвоение переменной scrp 4 вхождения тэга script - в нём содержится вся необходимая информация
    scrp = data.find_all('script')[4]
    # приведение переменной scrp в вид json
    scrp = json.loads(scrp.text.strip().replace('window.__INITIAL_STATE__ = ', ''))

    # присвоение соответствующим переменным данных из переменной scrp
    KFC_name = scrp.get('geoLocation').get('restaurantsList')[0].get('title').get('ru')
    KFC_address = scrp.get('geoLocation').get('restaurantsList')[0].get('contacts').get('streetAddress').get('ru')
    KFC_open_or_closed = scrp.get('geoLocation').get('restaurantsList')[0].get('status')
    KFC_latlon = scrp.get('geoLocation').get('restaurantsList')[0].get('contacts').get('coordinates').get('geometry').get('coordinates')
    KFC_phone = scrp.get('geoLocation').get('restaurantsList')[0].get('contacts').get('phoneNumber')
    KFC_open_hour_monday_friday = scrp.get('geoLocation').get('restaurantsList')[0].get('openingHours').get('regularDaily')[0].get('timeFrom')[0:5]
    KFC_close_hour_monday_friday = scrp.get('geoLocation').get('restaurantsList')[0].get('openingHours').get('regularDaily')[0].get('timeTill')[0:5]
    KFC_open_hour_saturday_sunday = scrp.get('geoLocation').get('restaurantsList')[0].get('openingHours').get('regularDaily')[5].get('timeFrom')[0:5]
    KFC_close_hour_saturday_sunday = scrp.get('geoLocation').get('restaurantsList')[0].get('openingHours').get('regularDaily')[5].get('timeTill')[0:5]
    
    # проверка на временное закрытие ресторана
    if KFC_open_or_closed == 'Open':
        KFC_working_hours = []
        KFC_working_hours.append('пн - пт ' + KFC_open_hour_monday_friday + ' до ' + KFC_close_hour_monday_friday)
        KFC_working_hours.append('сб-вс ' + KFC_open_hour_saturday_sunday + '-' + KFC_close_hour_saturday_sunday)
    else:
        KFC_working_hours = 'closed'
    
    # проверка на повторность ресторана, создание результирующего элемента и его внесение в итоговый список
    if KFC_name in KFC_names_check:
        pass
    else:
        KFC_names_check.append(KFC_name)
        result = {"address": KFC_address, "latlon": KFC_latlon, "name": KFC_name, "phones": [KFC_phone], "working_hours": KFC_working_hours}
        KFC_final_list.append(result)

# сохранение списка результирующих элементов в json-файл
with open ('KFC.json', 'w', encoding='utf-8') as file:
    json.dump(KFC_final_list, file, ensure_ascii=False)
