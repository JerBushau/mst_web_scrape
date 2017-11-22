"""
Class to process the data collected from the scrapers.
"""


from collections import OrderedDict


class Data_processor:

    def __init__(self):
        self.mst3k_info = OrderedDict()
        for i in range(11):
            self.mst3k_info['season_{}'.format(i)] = OrderedDict()

    # using static methods here to keep things logically grouped together
    # static methods may be called on the class or on an instance
    @staticmethod
    def extract_ep_num_and_title(title):
        """
        Take title string and return title and episode number separately
        """

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
        Processes homepage data populating mst3k_info dict with
        movie title, episode number and any associated shorts
        """

        for tr in data:
            if data.index(tr) > 4:
                for link in tr.select('a'):
                    title = link.string
                    title, number = self.extract_ep_num_and_title(title)
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
        Processes quote data adding each episodes quotes to mst3k_info dict
        """

        ep_season = self.determine_season(ep_number)
        quotes = [p.string for p in quotes]
        quotes = self.clean_quotes(quotes)
        for episode in sorted(self.mst3k_info[ep_season]):
            if episode == str(ep_number):
                self.mst3k_info[ep_season][episode]['quotes'] = quotes
                print('Quotes for episode {} have been processed.'
                      .format(episode))
