from utils import CollectorConfig, ContentLink

import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')


cfg = CollectorConfig()
link = ContentLink(cfg.primary_domain, cfg.content_type)

print(cfg.collector_config)
print(cfg.enabled_domains)
print(cfg.primary_domain)

print(link)

# user = UserAgent().random
# headers = {'user-agent': user}
#
# response = requests.get(link, headers=headers).text
# soup: Optional[BeautifulSoup] = BeautifulSoup(response, 'lxml')
#
# if soup:
#     block: Optional[Tag] = soup.find('div', class_='b-content__inline_items')
#     if block:
#         links: Optional[Tag] = block.find('div', class_='b-content__inline_item')
#
