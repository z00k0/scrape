import requests
from bs4 import BeautifulSoup
import logging
import os
# import cProfile


class Ufavodokanal:
    url = 'https://www.ufavodokanal.ru/personal/'
    logging.basicConfig(
        level=logging.DEBUG,
        filename='vdknl.log',
        format='%(asctime)s %(levelname)s:%(message)s'
    )

    def __init__(self, login, password) -> None:
        self.login = login
        self.password = password
        self.parser_count = 0

    def get_responce(self):
        self.session = requests.Session()

        resp = self.session.get(self.url)
        logging.debug('Start connection')
        soup = BeautifulSoup(resp.content, 'lxml')
        self.hidden1 = soup.find('input', {'name': 'AUTH_FORM'})['value']
        self.hidden2 = soup.find('input', {'name': 'TYPE'})['value']
        self.hidden3 = soup.find('input', {'name': 'backurl'})['value']

        data = {
            'USER_LOGIN': self.login,
            'USER_PASSWORD': self.password,
            'AUTH_FORM': self.hidden1,
            'TYPE': self.hidden2,
            'backurl': self.hidden3,
        }

        # with open('vodokanal.html', 'w') as file:
        #     file.write(resp.text)
        return data

    def auth(self):
        data = self.get_responce()
        resp = self.session.post(self.url, data)
        logging.debug('AUTH connection')
        soup = BeautifulSoup(resp.content, 'lxml')

        with open('lk_vodokanal.html', 'w') as file:
            file.write(resp.text)

        return soup

    def parsing(self):
        soup = self.auth()

        lk_row = soup.find_all('div', 'us_cont')

        self.lk_number = lk_row[0].text
        self.adress = lk_row[1].text

        balance_row = soup.table.tbody.tr
        self.balance = float(balance_row.find_all('td')[-1].text)

        return self.lk_number, self.adress, self.balance


if __name__ == '__main__':

    login = os.getenv('VDKNL_LOGIN')
    password = os.getenv('VDKNL_PASSWORD')
    vdknl = Ufavodokanal(login, password)
    vdknl.parsing()
    print(f'Номер счета: {vdknl.lk_number}')
    print(f'Адрес: {vdknl.adress}')
    print(f'Задолженность: {vdknl.balance:,.2f} руб.')
