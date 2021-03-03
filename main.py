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
month = '//*[contains(@class, "txt--6")]//span/text()'
container = "//div/h3/text()"
link = '//*[contains(@class, "buttonblock")]//a/@href'
monthCompare = 'PlayStation Plus: February 2021'
bad_chars = [';', '__', '*']


def main():
    
    bot_token = sys.argv[1]
    recipients = json.loads(sys.argv[2])

    results = []
    games = []
    start_time = time.time()

    results = scrapping()

    games = results["items"][0:3]
    for char in bad_chars :
        games = (s.strip(char) for s in games)

    links = results["links"][0:3]
    currentMonth = results["currentMonth"][0]

    if currentMonth == monthCompare:
        print("Iguales")
        if results["items"]:
            message = "🎮 📆 These are the free games of " + currentMonth + ":\n\n👾 " + "\n👾 ".join(games) + "\n\n🔗 " + '\n🔗 '.join(links) + "\n\n"

        print(message)

        telegram_bot_sendtext(message, bot_token, recipients)
    else:
        if results["items"]:
            message = "🎮 📆 These are the free games of " + currentMonth + ":\n\n👾 " + "\n👾 ".join(games) + "\n\n🔗 " + '\n🔗 '.join(links) + "\n\n"

        print(message)

        telegram_bot_sendtext(message, bot_token, recipients)

def scrapping():
    items = []

    print("URL Scrapped: " + url)
    xpathItems = container
    xpathLinks = link
    xpathMonth = month
    html = requests.get(url)
    doc = lxml.html.fromstring(html.content)
    items = doc.xpath(xpathItems)
    links = doc.xpath(xpathLinks)
    monthTitle = doc.xpath(xpathMonth)
    print(monthTitle)

    return { "items": items, "links": links, "currentMonth": monthTitle }

def telegram_bot_sendtext(bot_message, bot_token, recipients):
    for bot_chatID in recipients:
        print(bot_chatID)
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        print(response.json())

if __name__ == '__main__':
    main()
