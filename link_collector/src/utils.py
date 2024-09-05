from pathlib import Path
import logging
import json


class CollectorConfig:

    """load and parse config file"""

    def __init__(self, config_file='config.json') -> None:
        self.filename = config_file
        self.cfg_path = Path(__file__).resolve().parent.parent / self.filename
        self.__collector_config = self._load_config()
        self.content_type = self._get_content_type()
        self.enabled_domains, self.primary_domain, self.secondary_domains = self._get_domains()
        self.first_page, self.last_page, self.last_parsed_page = self._get_pages_info()

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

    def _get_content_type(self):
        return self.__collector_config['content_type']

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
        return f"https://{self.base_url}/{self.content_type}/best/page/"

    def __str__(self):
        return self.__content_link
