from utils import CollectorConfig, ContentLink
from fake_useragent import UserAgent

import logging
import requests
import lxml
import sys
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')


class LinkCollector:
    def __init__(self) -> None:
        self.config = CollectorConfig()
        self.url = ContentLink(self.config.primary_domain, self.config.content_type)
        self.__update_headers()

    def __update_headers(self):
        self.user_agent = UserAgent().random
        self.headers = {'user-agent': self.user_agent}

    def __parse_elements(self, html_obj, tag, content_class, method):
        soup = BeautifulSoup(html_obj.text, 'lxml')
        parsing_method = getattr(soup, method)
        parsed_data = parsing_method(tag, class_=content_class)

        return parsed_data

    def get_page_count(self):
        try:
            request = requests.get(f"{str(self.url)}/1", headers=self.headers)
            request.raise_for_status()
        except Exception as e:
            print(e)

        navigation_block = self.__parse_elements(request, 'div', 'b-navigation', 'find')

        if navigation_block is not None:
            anchor_tags = navigation_block.find_all(
                'a', href=True, string=lambda text: text and text.isdigit()
            )
            current_last_page = max(anchor_tags, key=lambda x: int(x.text))
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
            self.__update_headers()
            try:
                request = requests.get(f"{self.url}{count}/", headers=self.headers)
                request.raise_for_status()
                if request.status_code == 200:
                    content_items = self.__parse_elements(
                        request, 'div', 'b-content__inline_item', 'find_all')
                    filtered_links = [content_item.get('data-url') for content_item in content_items]
                    all_filtered_links.extend(filtered_links)
                    count += 1

            except Exception as e:
                self.config._update_pages_info(last_parsed_page=count)
                print(e)
            except KeyboardInterrupt:
                self.config._update_pages_info(last_parsed_page=count)
                sys.exit(0)

        return all_filtered_links


link_collector = LinkCollector()
print(link_collector.collect_pages())
