#!/usr/bin/python3

import telebot
import requests
import json
import lxml
import time
import sys

from lxml import html
from datetime import datetime

url = 'https://www.playstation.com/en-us/ps-plus/this-month-on-ps-plus/'
container = "//div/h3/text()"
link = '//*[contains(@class, "buttonblock")]//a/@href'

def main():
    
    bot_token = sys.argv[1]
    recipients = sys.argv[2]
    print(recipients)

    results = []
    games = []
    start_time = time.time()

    results = scrapping()

    games = results["items"][0:3]
    links = results["links"][0:3]

    if results["items"]:
        message = "🎮 📆 These are the free games of the month on PS Plus:\n\n👾 " + "\n👾 ".join(games) + "\n\n🔗 " + '\n🔗 '.join(links)

    print(message)

    telegram_bot_sendtext(message, bot_token, recipients)

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

def telegram_bot_sendtext(bot_message, bot_token, recipients):
    # for bot_chatID in recipients:
        bot_chatID = recipients
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        print(response.json())

if __name__ == '__main__':
    main()
