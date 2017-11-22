import json
from processor import Data_processor
from scrapers import Mst_info_scraper


class Mst3k_bot:
    """Class to control data collection and processing"""

    def __init__(self):
        self.data = Data_processor()
        self.scraper = Mst_info_scraper(self.data)
        self.dump_json()

    def dump_json(self):
        """Write the info to file as JSON"""

        with open('mst3k.json', 'w+') as db:
            json.dump(self.data.mst3k_info, db)
            print('\nData successfully written to mst3k.json')
