"""
Helper function for formatting scraped data.
"""


def extract_title_and_episode_number(title):
    """Take title string and return title and episode number separately"""

    title = title.replace('-', '').strip().split()
    number = title[0]
    del title[0]

    return (' '.join(title), number)


def determine_season(number):
    """Derive season from episode number"""

    if number[0] == '0' or number[0] == 'K':
        season = 0
    elif len(number) > 3:
        season = 10
    else:
        season = list(number)[0]

    return 'season_{}'.format(season)
