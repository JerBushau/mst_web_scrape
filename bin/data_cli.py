"""
Quick and simple CLI application to interact with the data collected by collect_mst3k_data.py
You must first run main.py to create you mst3k.json in order to use this CLI tool.
"""


import json
import random


def get_season():
    """Get season from user input"""
    while True:
        try:
            season = int(input('Enter a season. > '))
        except ValueError:
            print('Try again. Hint: Enter a number.')
            continue

        if season < 0:
            print('Please enter a positive number')
            continue
        elif season > 10:
            print('There is only data available for the original 10 seasons.')
            continue
        else:
            season_key = 'season_{}'.format(season)
            return season, season_key


def get_episode(season, season_key):
    """Get episode number"""
    while True:
        try:
            episode = int(input('Enter an episode number. > '))
        except ValueError:
            print('Try again. Hint: Enter a number.')
            continue

        if episode < 0:
            print('Please enter a positive number')
            continue
        else:
            eps_in_season = len(MST3K[season_key])
            if episode > eps_in_season:
                print('There are only {} episodes in season {}.'
                      .format(eps_in_season, season))
                continue

            episode_key = create_episode_key(season, episode)

            return episode, episode_key


def create_episode_key(season, episode):
    """Create the string that will serve as the episode key"""
    episode = str(episode)

    if season == 0 and len(episode) == 1:
        episode_key = '{}{}{}'.format('K', '0', episode)
        return episode_key
    elif season == 0 and len(episode) >= 2:
        episode_key = '{}{}'.format('K', episode)
        return episode_key

    elif len(episode) == 1:
        episode_key = '{}{}{}'.format(season, '0', episode)
        return  episode_key
    elif len(episode) >= 2:
        episode_key = '{}{}'.format(season, episode)
        return episode_key


def get_quote(season_key, episode_key):
    try:
        return random.choice(MST3K[season_key][episode_key]['quotes'])
    except KeyError:
        print('\nDOH!\n')


def get_info():
    season, season_key = get_season()
    episode, episode_key  = get_episode(season, season_key)
    quote = get_quote(season_key, episode_key)
    return season, season_key, episode, episode_key, quote


def print_results(info):
    try:
      print('\nMST3K Season: {} Episode: {} \n'
            'Title: {}\nShort: {}\nRandom Riff: "{}"'
            .format(info[0] if info[0] != 0 else 'KTMA',
                    info[2],
                    MST3K[info[1]][info[3]]['title'],
                    MST3K[info[1]][info[3]]['shorts']
                    if MST3K[info[1]][info[3]]['shorts'] else 'Short-less',
                    info[4]))
    except KeyError:
      print('something went wrong :( \n'
            'make sure you\'re using a valid episode season combination')


def main_loop():
    done = False
    while not done:
        print_results(get_info())
        again = input('\nAgain? > ').lower()
        if again not in ('',
                         'yes', 'y',
                         'sey','yse',
                         'eys', 'sye',
                         'hit me', ':)'):
            done = True


if __name__ == '__main__':
    with open('mst3k.json', 'r') as eps:
        MST3K = json.load(eps)

    main_loop()
