import re
import requests
import os
from bs4 import BeautifulSoup

session = requests.Session()

url = 'https://lkpe.bashrts.bgkrb.ru/Account/Login?ReturnUrl=%2F'
url_lk = 'https://lkpe.bashrts.bgkrb.ru/'
r = session.get(url)

soup = BeautifulSoup(r.text, 'lxml')
token = soup.find('input', {'name': '__RequestVerificationToken'})['value']
login = os.getenv('BASHRTS_LOGIN')
password = os.getenv('BASHRTS_PASSWORD')
data = {
    'Login': login,
    'Password': password,
    '__RequestVerificationToken': token
}

auth = session.post(url, data)
res = session.get(url_lk)
soup_lk = BeautifulSoup(res.text, 'lxml')

with open('lk.html', 'w') as f1:
    f1.write(res.text)

name = soup_lk.find('div', "user-name").text.split()

number = soup_lk.find('div', 'counter-num').text
m = re.search('\d+', number)
num = m.group(0)

adress = soup_lk.find('div', "counter-adress").div.text

bal = soup_lk.find('div', "balans-sum").span.text.strip()
m = re.match('(\d*)\s(\d+)\,(\d+)', bal)
balance = int(''.join(m.groups('0'))) / 100

device_info = soup_lk.find(id="ChangeMeterDevice").option.text.strip()
desc = soup_lk.find('div', 'device-info_desc').text.strip()
m = re.search('(\d+)\,(\d+)', desc)
device_desc = int(''.join(m.groups())) / 1000

print(f'Имя: {name[0]} {name[1]}')
print(f'Номер счета: {num}')
print(f'Адрес: {adress}')
print(f'Сумма к оплате: {balance:,.2f} руб.')
print(f'Счетчик:  {device_info}')
print(f'Показания: {device_desc:.3f} куб.м')
