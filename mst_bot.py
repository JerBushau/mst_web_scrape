import json
import helpers as h


class Club_mst3k_info_bot:
    """
        Class that controls scrapers data processing and writing to file
    """

    def __init__(self, hp, mp):
        self.hp_scraper = hp()
        self.mp_scraper = mp
        self.MST3K_info = {}

        for i in range(11):
            self.MST3K_info['season_{}'.format(i)] = {}

        self.populate_info()
        self.dump_json()

    def add_quotes_to_info(self):
        """
        Gathers all 'best riffs' from each movie page and adds to
        appropriate episode
        """

        # get the links to each episode from the homepage scrape
        data = self.hp_scraper.soup.find_all('a')[22:]
        for link in data:
            ep = link['href']
            ep_title, ep_number = h.extract_title_and_episode_number(link.string)

            if ep_number == 'Pilot':
                pass
            # scrape the 'best riffs' from movie page
            ms = self.mp_scraper(ep)
            ep_season = h.determine_season(ep_number)

            quotes = ms.soup.select('#quotes .body p')
            quotes = [p.string for p in quotes]
            quotes = self.clean_quotes(quotes)

            for episode in self.MST3K_info[ep_season]:
                if episode == str(ep_number):
                    self.MST3K_info[ep_season][episode]['quotes'] = quotes
                    print('Best riffs for {} episode {} have been added.'
                          .format(ep_season, episode))

    def clean_quotes(self, quotes):
        """Get rid of whitespace and empty quotes"""

        return [i.strip() for i in quotes if i != None]

    def add_entry_to_info(self, info):
        """Create dict entry for each tuple in data"""

        # get rid of edge case inconsistencies / duplicates from scrape first
        # this should probably be it's own separate function or something
        if  info[1] == 'to show episodes)':
            pass
        elif info[2] == '' and (info[1] ==
                                'Assignment: Venezuela (the lost short)'):
            pass
        elif info[2] == '' and (info[1] ==
                                'Manos: The Hands of Fate'):
            pass
        # then make entry
        else:
            entry = { 'title': info[1],
                      'shorts': info[2] }
            self.MST3K_info[h.determine_season(info[0])][str(info[0])] = entry

    def populate_info(self):
        """Populate the MST3K_info dict with entries"""

        self.hp_scraper.process_data()
        for i in self.hp_scraper.processed_data:
            self.add_entry_to_info(i)

        self.add_quotes_to_info()

    def dump_json(self):
        """Write the info to file as JSON"""

        with open('mst3k.json', 'w+') as db:
            json.dump(self.MST3K_info, db)
            print('\nData successfully written to mst3k.json')
