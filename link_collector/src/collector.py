from utils import CollectorConfig

import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')


cfg = CollectorConfig()

print(cfg.collector_config)
print(cfg.enabled_domains)
print(cfg.primary_domains)

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
