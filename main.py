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
link = '//*[contains(@class, "buttonblock")]//a/@href'

def main():
    start_time = time.time()

    results = scrapping()
    print (results["items"][0:3])
    print (results["links"][0:3])

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

if __name__ == '__main__':
    main()
