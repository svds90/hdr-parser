from pathlib import Path
import logging
import json
import tempfile


class CollectorConfig:

    """load and parse config file"""

    def __init__(self, config_file='config.json') -> None:
        self.filename = config_file
        self.cfg_path = Path(__file__).resolve().parent.parent / self.filename
        self.__collector_config = self._load_config()
        self.content_type = self._get_content_type()
        self.enabled_domains, self.primary_domain, self.secondary_domains = self._get_domains()
        self.first_page, self.last_page, self.last_parsed_page = self._get_pages_info()
        self.page_buffer_size = self._get_page_buffer_size()
        self.temp_file_prefix, self.temp_file_suffix = self._get_tmp_filename()

    def _load_config(self, **kwargs):
        try:
            with self.cfg_path.open('r') as f:
                config = json.load(f)
            return config
        except Exception as e:
            logging.error(f"Error loading configuration from {self.cfg_path}: {e.__class__.__name__} - {e}")
            return {}

    def _get_domains(self):

        primary_domain, enabled_domains, secondary_domains = "", [], []

        for domain_config in self.__collector_config['domains']:
            if domain_config.get('enabled', False):
                enabled_domains.append(domain_config['url'])
                if domain_config.get('primary', False):
                    primary_domain = domain_config['url']
                else:
                    secondary_domains.append(domain_config['url'])
        return enabled_domains, primary_domain, secondary_domains

    def _get_tmp_filename(self):
        return self.__collector_config['temp_file']['prefix'], self.__collector_config['temp_file']['suffix']

    def _get_content_type(self):
        return self.__collector_config['content_type']

    def _get_page_buffer_size(self):
        return self.__collector_config['page_buffer_size']

    def _get_pages_info(self):

        first_page, last_page, last_parsed_page = self.__collector_config['page_range'].values()
        return first_page, last_page, last_parsed_page

    def _update_pages_info(self, *args, **kwargs) -> None:
        if 'first_page' in kwargs:

            self.__collector_config['page_range']['first_page'] = kwargs['first_page']
            self.first_page = kwargs['first_page']

        if 'last_page' in kwargs:

            self.__collector_config['page_range']['last_page'] = int(kwargs['last_page'])
            self.last_page = int(kwargs['last_page'])

        if 'last_parsed_page' in kwargs:
            self.__collector_config['page_range']['last_parsed_page'] = kwargs['last_parsed_page']
            self.last_parsed_page = kwargs['last_parsed_page']

        with self.cfg_path.open('w') as f:
            json.dump(self.__collector_config, f, indent=4)


class ContentLink:

    """create content link from config file"""

    def __init__(self, base_url, content_type) -> None:
        self.base_url = base_url
        self.content_type = content_type
        self.__content_link = self._generate()

    def _generate(self):
        return f"https://{self.base_url}/{self.content_type}/page/"

    def __str__(self):
        return self.__content_link


class LinkFileHandler:
    def __init__(self, filename, page_buffer_size):
        self.filename = filename
        self.buffered_links = []
        self.buffered_pages = 0
        self.file = open(self.filename, "a")
        self.page_buffer_size = page_buffer_size
        self.last_parsed_link = None

    def get_last_parsed_link(self):
        with open('links.txt', 'rb') as f:
            f.seek(-2, 2)
            while f.read(1) != b'\n':
                f.seek(-2, 1)
            last_line = f.readline().decode()
            return last_line

    def append_links(self, links, current_page=None):
        self.buffered_links.extend(links)
        self.buffered_pages += 1
        if self.buffered_pages == self.page_buffer_size:
            self._write_to_file()

    def _write_to_file(self):
        self.file.write("\n".join(self.buffered_links) + "\n")
        self.buffered_pages = 0
        self.buffered_links = []

    def merge_files(self, temp_file_handler):
        temp_file_handler.temp_file.seek(0)
        new_links = temp_file_handler.temp_file.readlines()

        if new_links:
            self.file.writelines(reversed(new_links))

        temp_file_handler.close()
        self.close()

    def flush(self):
        if self.buffered_links:
            self._write_to_file()

    def close(self):
        self.flush()
        self.file.close()


class TempFileHandler:
    def __init__(self, prefix: str, suffix: str) -> None:
        try:
            self.temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                mode='w+t',
                prefix=prefix,
                suffix=suffix
            )
        except Exception as e:
            pass
        else:
            self.tempfile_directory = tempfile.gettempdir()

    def write_to_file(self, links: list):
        if not links:
            return

        self.temp_file.write('\n'.join(links) + '\n')
        self.temp_file.flush()

    def close(self):
        self.temp_file.flush()
        self.temp_file.close()
