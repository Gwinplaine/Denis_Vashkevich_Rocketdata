from bs4 import BeautifulSoup
import requests
import geocoder
import json

# сохранение URL в переменной url
url = 'https://www.ziko.pl/lokalizator/'

# отправка GET-запроса на сайт и сохранение полученного в переменной page
page = requests.get(url)

# применение BeautifulSoup к переменной page
data = BeautifulSoup(page.text, 'html.parser')

# поиск всех вхождений тэга td с классом mp-table-address - в них содержится адрес и телефон аптек
alladdresses = data.findAll("td", class_="mp-table-address")
# поиск всех вхождений тэга span с классом mp-pharmacy-head - в них содержится название аптек
allnames = data.findAll('span', class_="mp-pharmacy-head")
# поиск всех вхождений тэга td с классом mp-table-hours - в них содержится время работы
allhours = data.findAll('td', class_='mp-table-hours')

# пустой список для внесения неотформатированный строки времени работы аптек
list_for_time = []

#внесение в пустой список часов работы каждой аптеки
for hours in allhours:
    list_for_time.append(hours.text.split(' ')[0:-1])

#пустой список для внесения итогового отформатированного времени работы аптек
working_time_list = []

#итерирование по списку неотформатированного времени, форматирование времени, внесение его в список итогового отформатированного времени
for time in list_for_time:
    lst_time_final = []
    if len(time) == 8:
        letter = time[0] + ' ' + time[1] + '-' + time[3] + ' ' + time[4][0:3] + ' ' + time[5] + ' ' + '-' + ' '+time[7]
        lst_time_final.append(time[0] + ' ' + time[1] + '-' + time[3])
        lst_time_final.append(time[4][0:3] + ' ' + time[5] + ' ' + '-' + ' '+time[7])
    elif len(time) == 13:
        lst_time_final.append(time[0] + ' ' + time[1] + '-' + time[3])
        lst_time_final.append(time[4][0:3] + ' ' + time[5] + ' ' + '-' + ' '+time[7])
        lst_time_final.append(time[8][0:3] + ' ' + time[9] + ' ' + time[10] + '-' + time[12])
    elif len(time) == 18:
        lst_time_final.append(time[0] + ' ' + time[1] + '-' + time[3])
        lst_time_final.append(time[4][0:3] + ' ' + time[5] + ' ' + '-' + ' '+time[7])
        lst_time_final.append(time[8][0:3] + ' ' + time[9] + ' ' + time[10] + '-' + time[12])
        lst_time_final.append(time[13][0:3] + ' ' + time[14] + ' ' + time[15] + '-' + time[17])
    working_time_list.append(lst_time_final)

# пустой список для внесения итогового отформатированного адреса аптек
final_addresses_list = []
# итерирование по всем строкам с адресами и телефонами
for addresses in alladdresses:
    splitted_address = addresses.text.split(' ')
    # пустой список для внесения элементов адреса
    addresses_list = []
    for splitted_address_element in splitted_address:
        # поиск элементов до элемента 'tel.' - это будут элементы адреса и добавление их в список для внесения элементов адреса
        if splitted_address_element != 'tel.':
            addresses_list.append(splitted_address_element)
        else:
            break
    # внесение итоговых отформатированных адресов в соответствующий список
    final_addresses_list.append(' '.join(addresses_list))

# пустой список для внесения итогового отформатированного телефона аптек
final_phones = []
# итерирование по всем строкам с адресами и телефонами
for phone in alladdresses:
    # поиск индекса 'tel.' и выборка по элементам после него
    index = phone.text.split(' ').index('tel.')
    full_phones = phone.text.split(' ')[index+1:]
    # если указан один телефон - итоговое форматирование и внесение в соответствующий список
    if len(full_phones) == 8:
        two_last_numbers = full_phones[3][:2]
        full_phones = full_phones[:3]
        full_phones.append(two_last_numbers)
        final_phones.append([' '.join(full_phones)])
    # если указано несколько телефонов - создание списка телефонов, итоговое форматирование и внесение в соответствующий список
    else:
        phones_list = []
        three_last_numbers = full_phones[6][:3]
        numbers_without_semicolon = full_phones[3][:-1]
        full_phones[3] = numbers_without_semicolon
        full_phones[6] = three_last_numbers
        full_phones = full_phones[:-4]
        phone1 = ' '.join(full_phones[:4])
        phone2 = ' '.join(full_phones[4:])
        phones_list.append(phone1)
        phones_list.append(phone2)
        full_phones.append(phones_list)
        final_phones.append(phones_list)

# создание результирующего элемента
result = [{"address": final_addresses_list[i], "latlon": geocoder.arcgis(final_addresses_list[i]).latlng, "name": allnames[i].text,
    "phones": final_phones[i], "working_hours": working_time_list[i]} for i in range(0,len(final_addresses_list))]

# сохранение результирующего элемента в json-файл
with open ('ziko.json', 'w', encoding='utf-8') as file:
    json.dump(result, file, ensure_ascii=False)