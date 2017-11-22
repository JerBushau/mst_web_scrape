"""
Scraper objects that gather specific data.
"""


import time
import requests
from bs4 import BeautifulSoup


class Scraper:
    """Generic Scraper"""

    def __init__(self, url='', target=''):
        self.url = url
        self.res = requests.get(self.url)
        self.soup = BeautifulSoup(self.res.content, 'html.parser')
        self.data = self.soup.select(target)


class Movie_page_scraper(Scraper):
    """Movie 'detail' page scraper (for quotes)"""

    def __init__(self, url):
        url = '{}{}'.format('http://www.club-mst3k.com', url)
        super().__init__(url, target='a')
        self.quotes = self.soup.select('#quotes .body p')
        print('{} quotes scraped.'.format(url.split('/')[-1]))


class Mst_info_scraper(Scraper):
    """Gathers details from homepage and quotes from each movie page"""

    def __init__(self, data_processor):
        super().__init__(url='http://www.club-mst3k.com', target='table tr')
        self.dp = data_processor
        self.mps = Movie_page_scraper
        self.episode_links = self.soup.find_all('a')[22:]
        print('Homepage data scraped.')
        self.dp.process_homepage_data(self.data)
        self.scrape_quotes()

    def scrape_quotes(self):
        for ep in self.episode_links:
            ep_title, ep_number = self.dp.extract_ep_num_and_title(ep.string)
            mps = self.mps(ep['href'])
            self.dp.process_quote_data(mps.quotes, ep_title, ep_number)
            time.sleep(1)
