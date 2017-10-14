"""
Class to process the data collected from the scrapers.
"""


class Data_processor:

    def __init__(self):
        self.mst3k_info = {}
        for i in range(11):
            self.mst3k_info['season_{}'.format(i)] = {}

    # not sure this is the appropriate place for these methods
    @staticmethod
    def extract_ep_num_from_title(title):
        """Take title string and return title and episode number separately"""

        title = title.replace('-', '').strip().split()
        number = title[0]
        del title[0]
        return (' '.join(title), number)

    @staticmethod
    def determine_season(number):
        """Derive season from episode number"""

        if number[0] == '0' or number[0] == 'K':
            season = 0
        elif len(number) > 3:
            season = 10
        else:
            season = list(number)[0]
        return 'season_{}'.format(season)

    @staticmethod
    def clean_quotes(quotes):
        """Get rid of whitespace and empty quotes"""

        return [i.strip() for i in quotes if i != None]

    def process_homepage_data(self, data):
        """
        Processes scraped homepage data and populates mst3k_info dict with movie
        title, episode number and any associated shorts
        """
        for tr in data:
            if data.index(tr) > 4:
                for link in tr.select('a'):
                    title = link.string
                    title, number = self.extract_ep_num_from_title(title)
                if tr.select('.episode_short'):
                    for short in tr.select('.episode_short'):
                        shorts = []
                        for string in short.strings:
                            short_title = string.replace('+', '').strip()
                            shorts.append(short_title)
                        entry = { 'title': title, 'shorts': shorts }
                        self.mst3k_info[self.determine_season(number)][str(number)] = entry
                else:
                    entry = { 'title': title, 'shorts': [] }
                    self.mst3k_info[self.determine_season(number)][str(number)] = entry
        print('Homepage data processed.')

    def process_quote_data(self, quotes, ep_title, ep_number):
        """
        Processes scraped quote data and adds each episodes quotes to mst3k_info dict
        in the appropriate place.
        """
        ep_season = self.determine_season(ep_number)
        quotes = [p.string for p in quotes]
        quotes = self.clean_quotes(quotes)
        for episode in sorted(self.mst3k_info[ep_season]):
            if episode == str(ep_number):
                self.mst3k_info[ep_season][episode]['quotes'] = quotes
                print('Quotes for episode {} have been processed.'
                      .format(episode))
