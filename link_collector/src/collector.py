from utils import CollectorConfig, ContentLink
from fake_useragent import UserAgent

import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')


class CollectorInit:
    def __init__(self) -> None:
        self.config = CollectorConfig()
        self.link = ContentLink(self.config.primary_domain, self.config.content_type)
        self.user_agent = UserAgent().random
        self.headers = {'user-agent': self.user_agent}


collector = CollectorInit()

print(collector.headers)

#
# if soup:
#     block: Optional[Tag] = soup.find('div', class_='b-content__inline_items')
#     if block:
#         links: Optional[Tag] = block.find('div', class_='b-content__inline_item')
#
