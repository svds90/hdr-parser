from pathlib import Path
import logging
import json


class CollectorConfig:
    def __init__(self, config_file='config.json') -> None:
        self.config_filename = config_file
        self.collector_config = self._load_config()
        self.enabled_domains, self.primary_domains, self.secondary_domains = self._get_domains()

    def _load_config(self):
        cfg_path = Path(__file__).resolve().parent.parent / self.config_filename
        try:
            with cfg_path.open('r') as f:
                config = json.load(f)
            return config
        except Exception as e:
            logging.error(f"Error loading configuration from {cfg_path}: {e.__class__.__name__} - {e}")
            return {}

    def _get_domains(self):

        enabled_domains = []
        primary_domains = []
        secondary_domains = []

        for domain_config in self.collector_config['domains']:
            if domain_config.get('enabled', False):
                enabled_domains.append(domain_config['url'])
                if domain_config.get('primary', False):
                    primary_domains.append(domain_config['url'])
                else:
                    secondary_domains.append(domain_config['url'])
        return enabled_domains, primary_domains, secondary_domains
