"""
Scraper objects that gather specific data.
"""


import requests
from bs4 import BeautifulSoup
import helpers as h

class Scraper:
    """Generic Scraper"""

    def __init__(self, url='', target=''):
        self.url = url
        self.res = res = requests.get(self.url)
        self.soup = BeautifulSoup(res.content, 'html.parser')
        self.data = self.soup.select(target)


class Homepage_scraper(Scraper):
    """Club-mst3k homepage table scraper"""

    def __init__(self):
        super().__init__(url='http://www.club-mst3k.com', target='table tr')

    def process_data(self):
        """
        Processes scraped data and returns a set of tuples containing movie
        title, episode number and any associated shorts
        """
        result = []
        for tr in self.data:
            # Look through data starting at index 5
            if self.data.index(tr) > 4:
                # get text from a tag inside the tr
                for link in tr.select('a'):
                    title = link.string

                    title, number = h.extract_title_and_episode_number(title)

                # If there are any shorts associated and add them
                if tr.select('.episode_short'):
                    for short in tr.select('.episode_short'):
                        for string in short.strings:
                            short_title = string.replace('+', '').strip()

                        info = (number, title, short_title)
                        result.append(info)

                # Otherwise leave shorts blank and add
                else:
                    info = (number, title, '')
                    result.append(info)

        #  Use set to remove any duplicates from data
        self.processed_data = sorted(set(result))
        print('Homepage data scraped and processed.')


class Movie_page_scraper(Scraper):
    """Movie 'detail' page scraper (for quotes)"""

    def __init__(self, url):
        url = '{}{}'.format('http://www.club-mst3k.com', url)
        super().__init__(url, target='a')
