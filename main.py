#!/usr/bin/python3

import telebot
import requests
import lxml
import time
import sys

from lxml import html
from datetime import datetime

TOKEN = '<token string>'
# tb = telebot.TeleBot(TOKEN)

url = 'https://www.playstation.com/en-us/ps-plus/this-month-on-ps-plus/'
# container = '//*[contains(@class, "text-block")]/text()'
container = "//div/h3/text()"

def main():
    start_time = time.time()

    results = scrapping()
    print (results["items"])

def scrapping():
    items = []

    # print("URL Scrapped: " + url)
    xpath = container
    html = requests.get(url)
    doc = lxml.html.fromstring(html.content)
    items = doc.xpath(xpath)
    # items = doc.xpath("//div/h3/text()")

    return { "items": items }


if __name__ == '__main__':
    main()
