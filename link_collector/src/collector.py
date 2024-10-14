from utils import CollectorConfig, ContentLink, LinkFileHandler, TempFileHandler
from log_service import CommonLogger
from fake_useragent import UserAgent

import requests
import lxml
import sys
from bs4 import BeautifulSoup


class LinkCollector:
    def __init__(self) -> None:
        self.config = CollectorConfig()
        self.url = ContentLink(self.config.primary_domain, self.config.content_type)
        self.file_handler = LinkFileHandler('links.txt', self.config.page_buffer_size)
        self.main_logger = CommonLogger(self.config.logging_settings)

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

    def collect_links(self):
        current_page = 1 if self.config.last_parsed_page is None else self.config.last_parsed_page

        for page in range(current_page, self.config.last_page + 1):
            self.__update_headers()
            try:
                request = requests.get(f"{self.url}{current_page}/", headers=self.headers)
                request.raise_for_status()
                if request.status_code == 200:
                    content_items = self.__parse_elements(
                        request, 'div', 'b-content__inline_item', 'find_all')
                    filtered_links = [content_item.get('data-url') for content_item in content_items]
                    self.file_handler.append_links(filtered_links, current_page)

                    self.main_logger.logger.info("Page %s, added %s links.",
                                                 current_page, len(filtered_links))

                    current_page += 1

            except Exception as e:
                self.file_handler.close()
                self.config._update_pages_info(last_parsed_page=current_page)
                self.main_logger.logger.error("%s", e, exc_info=True)
                break
            except KeyboardInterrupt:
                self.file_handler.close()
                self.config._update_pages_info(last_parsed_page=current_page)
                self.main_logger.logger.error("Execution interrupted and closed by user.")
                sys.exit(0)

        self.config._update_pages_info(last_parsed_page=current_page if current_page <
                                       self.config.last_page else self.config.last_page)

        self.main_logger.logger.info("Parsing finished. Last parsed page: %s.", current_page)
        self.file_handler.close()

    def update_links(self):
        temp_file_handler = TempFileHandler(self.config.temp_file_prefix, self.config.temp_file_suffix)
        first_page = self.config.first_page
        last_parsed_link = self.file_handler.get_last_parsed_link()

        self.main_logger.logger.info("Previous parsed link - %s", last_parsed_link.strip().split('/')[-1])

        while True:
            self.__update_headers()
            request = requests.get(f"{self.url}{first_page}/", headers=self.headers)
            request.raise_for_status()
            if request.status_code == 200:
                content_items = self.__parse_elements(request, 'div', 'b-content__inline_item', 'find_all')
                filtered_links = [content_item.get('data-url') for content_item in content_items]
                updated_links = []

                for link in filtered_links:
                    if link == last_parsed_link.strip():
                        temp_file_handler.write_to_file(updated_links)
                        if updated_links:
                            self.main_logger.logger.info(
                                "Page %s: added %s links to the temporary file.", first_page, len(updated_links))
                            self.main_logger.logger.info("Last parsed link - %s",
                                                         updated_links[-1].strip().split('/')[-1])
                        else:
                            self.main_logger.logger.info("Nothing to parse.")
                            temp_file_handler.close()
                            return
                        break
                    updated_links.append(link)
                else:
                    self.main_logger.logger.info(
                        "Page %s: added %s links to the temporary file.", first_page, len(updated_links))
                    first_page += 1
                    temp_file_handler.write_to_file(updated_links)
                    continue

                self.main_logger.logger.info("First parsed link - %s",
                                             temp_file_handler.get_first_link().split('/')[-1])
                self.file_handler.merge_files(temp_file_handler)
                self.main_logger.logger.info("Temporary file has been merged into the main file.")
                break


if __name__ == "__main__":
    link_collector = LinkCollector()
    link_collector.update_links()