import requests
from bs4 import BeautifulSoup
import telebot
import urllib.parse
import bot_token


class TelegramBot:
    token_bot = bot_token.token
    id_chat = bot_token.id_chat
    bot = telebot.TeleBot(token_bot)

    def send_message(self, message):
        self.bot.send_message(self.id_chat, message)


class AvitoParser:
    url = 'https://www.avito.ru/sankt-peterburg'

    def get_page(self, page: int = None, find_string=''):
        params = {'cd': '1', 'q': find_string}
        if page and page > 1:
            params['p'] = page

        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) '
                                 'Chrome/95.0.4638.54 Safari/537.36', 'accept': '*/*'}

        r = requests.get(self.url, headers=headers, params=params)
        return r.text

    def pagination_limit(self, find_string):
        text = self.get_page(find_string=find_string)
        soup = BeautifulSoup(text, 'lxml')
        content = soup.select('a.pagination-page')
        last_page = content[-1]
        href = last_page.get('href')
        if not href:
            return 1
        parse_href = urllib.parse.urlparse(href)
        params = urllib.parse.parse_qs(parse_href.query)
        return int(params['p'][0])

    def get_block(self, cost_min, cost_max, page: int = None, find_string=''):
        text = self.get_page(page=page, find_string=find_string)
        soup = BeautifulSoup(text, 'lxml')
        content = soup.select_one('div.items-items-kAJAg')
        for item in content:
            block = self.parse_block(item=item, cost_min=cost_min, cost_max=cost_max)
            self.find_new_ads(block)

    def check_min_max_price(self, price, cost_min=0, cost_max=9999999999):
        if cost_min < int(price) < cost_max:
            return True
        else:
            return False

    def parse_block(self, item, cost_min, cost_max):
        url_block = item.select_one('a')

        if url_block is None:
            pass
        else:
            href = url_block.get('href')
            url = 'https://www.avito.ru/' + href

            title_block = item.select_one('h3')
            title = title_block.string.strip()

            price_block = item.select_one('span.price-price-BQkOZ').text
            price = str(''.join(i for i in price_block if i.isdigit()))
            if self.check_min_max_price(price, cost_min, cost_max) is True:
                return [title, price, url]

    def parse_all_pages(self, find_string, cost_min, cost_max):
        last_page = self.pagination_limit(find_string=find_string)
        for i in range(1, last_page + 1):
            self.get_block(page=i, find_string=find_string, cost_min=cost_min, cost_max=cost_max)

    def find_new_ads(self, ads):
        try:
            data = open('data.txt', 'r')
        except FileNotFoundError:
            data = open('data.txt', 'w').close()
            data = open('data.txt', 'r')
        session = data.read().split('\n')
        data.close()
        for ads_data in session:
            if ads is None:
                return False
            elif str(ads_data) == str(ads):
                return False
        data = open('data.txt', 'a')
        data.write(str(ads) + '\n')
        data.close()
        # TelegramBot().send_message(str(ads))
        print(ads)
