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
monthCompare = 'PlayStation Plus: March 2021'
bad_chars = [';', '__', '*']


def main():
    
    recipients = json.loads(sys.argv[2])
    last_offset_id = 0
    results = []
    games = []
    start_time = time.time()

    results = scrapping()

    games = results["items"]
    qtyGames = len(games)

    for char in bad_chars:
        games = (s.strip(char) for s in games)

    links = results["links"][0:qtyGames]
    currentMonth = results["currentMonth"][0]

    if results["items"]:
            message = "🎮 📆 These are the free games of " + currentMonth + ":\n\n👾 " + "\n👾 ".join(games) + "\n\n🔗 " + '\n🔗 '.join(links) + "\n\n"
            telegram_bot_sendtext(message, recipients)

    while(True):
        message_dictionary = update(last_offset_id)
        for i in message_dictionary["result"]:

            id_chat, user, text, id_update = read_message(i)
            if id_update > (last_offset_id-1):
                last_offset_id = id_update + 1

            if "Game" in text:
                answer_text = message
            else:
                answer_text = "You have written: \"" + text + "\"\nPlease write **Game** to receive information."

            send_message(id_chat, answer_text)

    message_dictionary = []

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

def update(offset):
    answer = requests.get(telegramURL + "getUpdates" + "?offset=" + str(offset))
    message_js = answer.content.decode("utf8") 
    message_dictionary = json.loads(message_js)

    return message_dictionary
 
 
def read_message(message):
 
    text = message["message"]["text"]
    user = message["message"]["from"]["first_name"]
    id_chat = message["message"]["chat"]["id"]
    id_update = message["update_id"]
 
    return id_chat, user, text, id_update
 
def send_message(id_chat, texto):
    requests.get(telegramURL + "sendMessage?parse_mode=Markdown&text=" + texto + "&chat_id=" + str(id_chat))

if __name__ == '__main__':
    main()
