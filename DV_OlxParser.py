from bs4 import BeautifulSoup
import requests
import telebot
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

token = '6592114682:AAF1bVU9gTDgSKgQzYKt6k-Wv1Ip98RFpoU'
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])


def lastrealestate(message):
    current_last_realestate = []
    a = 0
    while True:
        # save URL of page in url variable
        url = 'https://www.olx.ua/uk/nedvizhimost/kvartiry/prodazha-kvartir/od/?currency=UAH&search%5Bprivate_business%5D=private&search%5Border%5D=created_at:desc&search%5Bfilter_enum_commission%5D%5B0%5D=1'

        # send GET-request and save result in variable page
        page = requests.get(url, verify=False)

        # BeautifulSoup on page variable
        data = BeautifulSoup(page.text, 'html.parser')

        # find all 'a' tags with specific class
        all = data.findAll('a', class_='css-rc5s2u')

        #while first loop add 5 last entries
        if len(current_last_realestate) == 0:
            for first_five in range(3,8):
                current_last_realestate.insert(0, 'https://www.olx.ua' + all[first_five].get('href'))
        
        #clean list of entries
        if len(current_last_realestate) > 10000:
            current_last_realestate = current_last_realestate[:9000]

        #try to check if last entries haven't posted already
        try:
            if 'https://www.olx.ua'+all[3].get('href') not in current_last_realestate:

                url_of_new = 'https://www.olx.ua'+all[3].get('href')

                #options for selenium
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-gpu")
                
                #scrapping count of entry visitors
                browser = webdriver.Chrome(options=chrome_options)
                browser.get(url_of_new)
                watches = browser.find_element(By.CLASS_NAME, 'css-42xwsi')
                counter_of_watches = []
                for i in watches.text:
                    if i.isdigit():
                        counter_of_watches.append(str(i))
                
                browser.quit()
                current_last_realestate.insert(0, 'https://www.olx.ua'+all[3].get('href'))
                if int(''.join(counter_of_watches)) < 100:
                    bot.send_message(message.chat.id, 'https://www.olx.ua'+all[3].get('href'))
                    bot.send_message(712499854, 'https://www.olx.ua'+all[3].get('href'))
                    if 'https://www.olx.ua'+all[4].get('href') not in current_last_realestate:
                        url_of_new = 'https://www.olx.ua'+all[4].get('href')

                        chrome_options = webdriver.ChromeOptions()
                        chrome_options.add_argument("--no-sandbox")
                        chrome_options.add_argument("--headless")
                        chrome_options.add_argument("--disable-gpu")
                        
                        browser = webdriver.Chrome(options=chrome_options)
                        browser.get(url_of_new)
                        watches = browser.find_element(By.CLASS_NAME, 'css-42xwsi')
                        counter_of_watches = []
                        for i in watches.text:
                            if i.isdigit():
                                counter_of_watches.append(str(i))             
                        browser.quit()
                        current_last_realestate.insert(0, 'https://www.olx.ua'+all[4].get('href'))
                        if int(''.join(counter_of_watches)) < 100:
                            bot.send_message(message.chat.id, 'https://www.olx.ua'+all[4].get('href'))
                            bot.send_message(712499854, 'https://www.olx.ua'+all[4].get('href'))
                            bot.send_message(712499854, len(current_last_realestate))
                            time.sleep(60)
                    else:
                        time.sleep(60)
                else:
                    time.sleep(60)   
            else:
                time.sleep(60)             
        except:
            time.sleep(60)
#Run bot
bot.polling(none_stop=True)