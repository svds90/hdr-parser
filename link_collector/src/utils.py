from pathlib import Path
import logging
import json


class CollectorConfig:

    """load and parse config file"""

    def __init__(self, config_file='config.json') -> None:
        self.filename = config_file
        self.__collector_config = self._load_config()
        self.content_type = self._get_content_type()
        self.enabled_domains, self.primary_domain, self.secondary_domains = self._get_domains()

    def _load_config(self):
        cfg_path = Path(__file__).resolve().parent.parent / self.filename
        try:
            with cfg_path.open('r') as f:
                config = json.load(f)
            return config
        except Exception as e:
            logging.error(f"Error loading configuration from {cfg_path}: {e.__class__.__name__} - {e}")
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
