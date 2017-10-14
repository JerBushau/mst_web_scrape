"""

Script to collect information about the first 10 seasons of MST3K from the web and save it as JSON.

Authored by: Jeremiah Bushau

"""

import json
import requests
from bs4 import BeautifulSoup


# not the best naming >.<
class Catalog(dict):
    """dict type class where the data will be stored"""

    def __init__(self, data):
        super().__init__()
        self.data = data

        for i in range(11):
            self['season_{}'.format(i)] = {}

    def create_entry_from_data(self, info):
        # get rid of edge case inconsistencies / duplicates from scrape first
        # this should probably be it's own seperate function or something
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
                      'shorts': info[2]}
            self[determine_season(info[0])][str(info[0])] = entry

    def populate_catalog(self):
        for i in self.data:
            self.create_entry_from_data(i)

        return self

    def get_quotes(self):
        data = soup.find_all('a')[20:]
        del data[1]
        for i in data:
            ep = i['href']
            ep_title, ep_number = format_title(i.string)

            if ep_number != 'Pilot':
                ep_season = determine_season(ep_number)
                ep_url = '{}{}'.format(url, ep)
                ep_res = requests.get(ep_url)
                ep_soup = BeautifulSoup(ep_res.content, 'html.parser')

                quotes = ep_soup.select('#quotes .body p')
                quotes = [i.string for i in quotes]
                quotes = clean_quotes(quotes)

                print(ep_season)
                print(ep_number)

                for episode in self[ep_season]:
                    if episode == str(ep_number):
                        self[ep_season][episode]['quotes'] = quotes
                        print(self[ep_season][episode])

    def write_catalog_as_json(self):
        with open('mst3k.json', 'w') as db:
            json.dump(self, db)
            print('Data successfully written to mst3k.json')


def process_data(data):
    result = []
    for i in data:
        if data.index(i) > 4:
            for link in i.select('a'):
                title = link.string
                title, episode_number = format_title(title)

            if i.select('.episode_short'):
                for short in i.select('.episode_short'):
                    for string in short.strings:
                        short_title = string.replace('+', '').strip()
                    info = (episode_number, title, short_title)

                    result.append(info)
            else:
                info = (episode_number, title, '')
                result.append(info)

    # return as a set to remove any duplicates from data.
    return sorted(set(result))


def format_title(title):
    """take title string and return title and episode number seperatly"""

    title = title.replace('-', '').strip().split()
    episode_number = title[0]
    del title[0]

    return (' '.join(title), episode_number)


def clean_quotes(quotes):
    result = []
    for i in quotes:
        if i != None:
            result.append(i.strip())
    return result


def determine_season(episode_number):
    """derive season from episode number"""

    if episode_number[0] == '0' or episode_number[0] == 'K':
        season = 0
    elif len(episode_number) > 3:
        season = 10
    else:
        season = list(episode_number)[0]

    return 'season_{}'.format(season)


if __name__ == '__main__':
    url = 'http://www.club-mst3k.com'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.select('table tr')

    mst3k_episode_directory = Catalog(process_data(data))
    mst3k_episode_directory.populate_catalog()
    mst3k_episode_directory.get_quotes()
    mst3k_episode_directory.write_catalog_as_json()
