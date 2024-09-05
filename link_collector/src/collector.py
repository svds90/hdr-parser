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
        try:
            request = requests.get(str(self.url), headers=self.headers)
        except Exception as e:
            print(e)

        soup = BeautifulSoup(request.text, 'lxml')
        navigation_block = soup.find('div', class_='b-navigation')

        if navigation_block is not None:
            anchor_tags = navigation_block.find_all(
                'a', href=True, string=lambda text: text and text.isdigit()
            )
            last_page = max(anchor_tags, key=lambda x: int(x.text))
            return last_page.text
        else:
            return None

    def collect(self, first_page=1, last_page=11):

        count = first_page
        print(f"{self.url}{count}/")
        all_filtered_links = []
        for page in range(count, last_page):
            try:
                request = requests.get(str(f"{self.url}{count}/"), headers=self.headers)
                if request.status_code == 200:
                    soup = BeautifulSoup(request.text, 'lxml')
                    items = soup.find_all('div', class_='b-content__inline_item')
                    links = [item.get('data-url') for item in items]
                    all_filtered_links.extend(links)

            except Exception as e:
                print(e)

            count += 1
        return all_filtered_links


link_collector = LinkCollector()
print(link_collector.config.last_page)

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
