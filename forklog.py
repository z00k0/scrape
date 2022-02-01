import requests
import codecs
import json
import re
import logging

from bs4 import BeautifulSoup


logging.basicConfig(
    level=logging.DEBUG,
    filename='forklog.log',
    format='%(asctime)s %(levelname)s:%(message)s'
)

session = requests.Session()
url = "https://forklog.com/news/"
resp = session.get(url)
soup = BeautifulSoup(resp.content, 'lxml')

with codecs.open('news.html', 'w', 'utf-8') as file:  # save news.html for debugging
    file.write(resp.text)


news_dict = {}
counter = 0
for item in soup.findAll('div', 'post_item'):
    news_link = item.find('a')['href']
    news_date = item.find('span', 'post_date').text
    if 14 < int(news_date.split('.')[0]) < 27:
        news_dict[counter] = (news_date, news_link)
        counter += 1

with open('dict.json', 'w', encoding='utf-8') as file:  # save news links as json for debugging
    json.dump(news_dict, file, ensure_ascii=False, indent=4)

code_list = {}
for key, value in news_dict.items():
    news_resp = session.get(value[1])
    news_soup = BeautifulSoup(news_resp.content, 'lxml')
    news = news_soup.find('div', 'post_content')
    try:
        code = news.find('strong').text
        m = re.search('\[?(\d+)\s—\s(\w+)\]?', code)
        number = int(m.group(1))
        word = m.group(2)
        code_list[number] = word
    except Exception as ex:
        print(ex)
        number = 0

with open('words.json', 'r', encoding='utf-8') as file:
    words = json.load(file)

for key, value in code_list:
    if key not in words:
        words[key] = word

with open('words.json', 'w', encoding='utf-8') as file:
    json.dump(words, file, ensure_ascii=False, indent=4)
