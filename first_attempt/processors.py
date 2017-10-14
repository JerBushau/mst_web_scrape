"""
Class to process the data collected from the scraper.
"""


class Data_processor:

    def __init__(self):
        self.mst3k_info = {}
        for i in range(11):
            self.mst3k_info['season_{}'.format(i)] = {}

    def extract_ep_num_from_title(self, title):
        """Take title string and return title and episode number separately"""

        title = title.replace('-', '').strip().split()
        number = title[0]
        del title[0]
        return (' '.join(title), number)

    def determine_season(self, number):
        """Derive season from episode number"""

        if number[0] == '0' or number[0] == 'K':
            season = 0
        elif len(number) > 3:
            season = 10
        else:
            season = list(number)[0]
        return 'season_{}'.format(season)

    def process_homepage_data(self, data):
        """
        Processes scraped data and returns a set of tuples containing movie
        title, episode number and any associated shorts
        """
        for tr in data:
            if data.index(tr) > 4:
                # get text from a tag inside the tr
                for link in tr.select('a'):
                    title = link.string
                    title, number = self.extract_ep_num_from_title(title)
                # If there are any shorts associated add them
                if tr.select('.episode_short'):
                    for short in tr.select('.episode_short'):
                        shorts = []
                        for string in short.strings:
                            short_title = string.replace('+', '').strip()
                            shorts.append(short_title)
                        entry = { 'title': title, 'shorts': shorts }
                        self.mst3k_info[self.determine_season(number)][str(number)] = entry
                # Otherwise leave shorts blank and add
                else:
                    entry = { 'title': title, 'shorts': [] }
                    self.mst3k_info[self.determine_season(number)][str(number)] = entry
            #  Use set to remove any obvious duplicates from data
        print('Homepage data processed.')

    def process_quote_data(self, quotes):
        quotes = [p.string for p in quotes]
        quotes = self.clean_quotes(quotes)
        for episode in self.mst3k_info[ep_season]:
            if episode == str(ep_number):
                self.mst3k_info[ep_season][episode]['quotes'] = quotes
                print('Best riffs for {} episode {} have been added.'
                      .format(ep_season, episode))

    def clean_quotes(self, quotes):
        """Get rid of whitespace and empty quotes"""

        return [i.strip() for i in quotes if i != None]
