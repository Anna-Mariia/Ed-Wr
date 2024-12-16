import requests
url = "https://itc.ua"
response = requests.get(url)
if response.status_code == 200:
    html_content = response.text
    print("HTML дані ти вже маєш")
else:
    print(f"Анна-Марія,вчи що таке 404,403,500,503: {response.status_code}")

"""Beautiful Soup is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree

Що я читала
https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser)
"""

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_content,"html.parser")
all_text = soup.get_text()
print(all_text)

"""Бібліотека re

що я читала
https://docs.python.org/3/library/re.html

спитати у чата чи знає він більше патернів окрім стандартних
"""

import re
date_pattern = r"\b\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}\b|\b\w+\s\d{1,2},\s\d{4}\b"
dates = re.findall(date_pattern,all_text)
print(f"Знайдені дати: {dates}")

import json

with open("dates.json","w") as file:
    json.dump(dates,file,indent=4)

print("Маєш файл")

"""Трішки побавимось з даними"""

sorted_dates = sorted(dates)
print(f"Посортовані дати : {sorted_dates}")

unique_dates = list(set(sorted(dates)))
print(f"Дати без повторів: {unique_dates}")

email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
emails = re.findall(email_pattern,all_text)
print(f"Знайдені email-адреси: {emails}")

url_pattern = r"https?://[^\s]+"
urls = re.findall(url_pattern,all_text)
print(f"Знайдені URL-адреси: {urls}")

unique_urls = list(set(urls))
print(f"Urls без повторів: {unique_urls}")
