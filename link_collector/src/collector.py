from os import link
from urllib import request
from utils import CollectorConfig, ContentLink
from fake_useragent import UserAgent

import logging
import requests
import lxml
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')


class LinkCollector:
    def __init__(self) -> None:
        self.config = CollectorConfig()
        self.url = ContentLink(self.config.primary_domain, self.config.content_type)
        self.user_agent = UserAgent().random
        self.headers = {'user-agent': self.user_agent}

    def get_page_count(self):
        request = requests.get(str(self.url), headers=self.headers)
        soup = BeautifulSoup(request.text, 'lxml')
        navigation_block = soup.find('div', class_='b-navigation')
        last_page = navigation_block.find_all('a', href=True,
                                              string=lambda text: text and text.isdigit())[-1]
        return last_page.text


link_collector = LinkCollector()
print(link_collector.get_page_count())

# soup = BeautifulSoup(html, 'lxml')
# nav_block = soup.find('div', class_='b-navigation')
# last_a = nav_block.find_all('a')[-1]
# print(last_a.text)  # Выведет "1390"

# request1 = requests.get(str(link_collector.url), headers=link_collector.headers)
# print(request1.text)

#
# if soup:
#     block: Optional[Tag] = soup.find('div', class_='b-content__inline_items')
#     if block:
#         links: Optional[Tag] = block.find('div', class_='b-content__inline_item')
#
