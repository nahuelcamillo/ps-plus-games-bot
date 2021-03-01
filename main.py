#!/usr/bin/python3

import telebot
import requests
import json
import lxml
import time
import sys

from lxml import html
from datetime import datetime

TOKEN = '1437994990:AAHTvf7dKhW3Zpw2MPs6zFB-ixdN9N_mUXY'
tb = telebot.TeleBot(TOKEN)
myIdBot = '235320816'

url = 'https://www.playstation.com/en-us/ps-plus/this-month-on-ps-plus/'
container = "//div/h3/text()"
link = '//*[contains(@class, "buttonblock")]//a/@href'

def main():
    
    bot_token = TOKEN

    results = []
    games = []
    start_time = time.time()

    results = scrapping()

    games = results["items"][0:3]
    links = results["links"][0:3]

    if results["items"]:
        message = "🎮 📆 These are the free games of the month on PS Plus:\n\n👾 " + "\n👾 ".join(games) + "\n\n🔗 " + '\n🔗 '.join(links)

    print(message)

    # telegram_bot_sendtext(message, bot_token, recipients)
    telegram_bot_sendtextOwn(message, bot_token)

def scrapping():
    items = []

    print("URL Scrapped: " + url)
    xpathItems = container
    xpathLinks = link
    html = requests.get(url)
    doc = lxml.html.fromstring(html.content)
    items = doc.xpath(xpathItems)
    links = doc.xpath(xpathLinks)

    return { "items": items, "links": links }

# def telegram_bot_sendtext(bot_message, bot_token, recipients):
#     for bot_chatID in recipients:
#         send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
#         response = requests.get(send_text)
#         print(response.json())

def telegram_bot_sendtextOwn(bot_message, bot_token):
    bot_chatID = '235320816'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    print(response.json())

if __name__ == '__main__':
    main()
