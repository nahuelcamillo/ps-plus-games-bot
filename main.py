#!/usr/bin/python3

import telebot
import telegram
import requests
import json
import lxml
import time
import sys

from lxml import html
from datetime import datetime

bot_token = sys.argv[1]
telegramURL = "https://api.telegram.org/bot" + bot_token + "/"
url = 'https://www.playstation.com/en-us/ps-plus/this-month-on-ps-plus/'
month = '//*[contains(@class, "txt--6")]//span/text()'
container = '//*[contains(@class, "text-block         ")]//h3/text()'
link = '//*[contains(@class, "box")]//*[contains(@class, "buttonblock")]//a/@href'
bad_chars = [';', '__', '*']


def main():
    
    recipients = json.loads(sys.argv[2])
    last_offset_id = 0
    results = []
    games = []
    results = scrapping()

    currentDate = current_date_format(datetime.now())
    monthCompare = 'PlayStation Plus: ' + currentDate

    games = results["items"]
    qtyGames = len(games)

    for char in bad_chars:
        games = (s.strip(char) for s in games)

    links = results["links"][0:qtyGames]
    currentMonth = results["currentMonth"][0]

    if currentMonth != monthCompare:
        if results["items"]:
                message = "🎮 📆 These are the free games of " + currentMonth + ":\n\n👾 " + "\n👾 ".join(games) + "\n\n🔗 " + '\n🔗 '.join(links) + "\n\n"
                telegram_bot_sendtext(message, recipients)

def scrapping():
    items = []

    xpathItems = container
    xpathLinks = link
    xpathMonth = month
    html = requests.get(url)
    doc = lxml.html.fromstring(html.content)
    items = doc.xpath(xpathItems)
    links = doc.xpath(xpathLinks)
    monthTitle = doc.xpath(xpathMonth)

    return { "items": items, "links": links, "currentMonth": monthTitle }

def telegram_bot_sendtext(bot_message, recipients):
    for bot_chatID in recipients:
        send_text = telegramURL + 'sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        print(response.json())

def current_date_format(date):
    months = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    month = months[date.month - 1]
    year = date.year
    actualDate = "{} {}".format(month, year)

    return actualDate

if __name__ == '__main__':
    main()
