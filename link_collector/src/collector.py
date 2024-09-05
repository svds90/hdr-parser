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
            request = requests.get(f"{str(self.url)}/1", headers=self.headers)
        except Exception as e:
            print(e)

        soup = BeautifulSoup(request.text, 'lxml')
        navigation_block = soup.find('div', class_='b-navigation')
        print(navigation_block)

        if navigation_block is not None:
            anchor_tags = navigation_block.find_all(
                'a', href=True, string=lambda text: text and text.isdigit()
            )
            current_last_page = max(anchor_tags, key=lambda x: int(x.text))
            print(current_last_page.text)
            if int(self.config.last_page) != int(current_last_page.text):
                self.config._update_pages_info(last_page=current_last_page.text)
            return current_last_page.text
        else:
            return None

    def collect_pages(self, start=None, stop=None):
        if self.config.last_parsed_page is None:
            count = 1
        else:
            count = self.config.last_parsed_page

        all_filtered_links = []

        for page in range(count, self.config.last_page):
            try:
                request = requests.get(f"{self.url}{count}/", headers=self.headers)
                if request.status_code == 200:
                    soup = BeautifulSoup(request.text, 'lxml')
                    content_items = soup.find_all('div', class_='b-content__inline_item')
                    filtered_links = [content_item.get('data-url') for content_item in content_items]
                    all_filtered_links.extend(filtered_links)

                    count += 1

            except Exception as e:
                print(e)
        return all_filtered_links


link_collector = LinkCollector()
print(link_collector.get_page_count())
