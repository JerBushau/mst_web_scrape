"""
pointless app that scrapes www.club-mst3k.com for random quote,
random movie and the watch it together movie.

written by Jeremiah Bushau in 2017
"""

import os
import requests
from bs4 import BeautifulSoup
from pyfiglet import Figlet


def get_info():
    """
    Use Requests and Beautiful Soup modules to scrape club-mst3k for quote,
    watch it together and random movie from the links thereon

    returns a tuple containing strings
    """

    url = 'http://www.club-mst3k.com/'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    quote = soup.select('div.rectangle-speech-border a'
                        )[0].string or 'How about a little fire, Scarecrow?!'
    w_i_t_movie = soup.select('tr#todays-featured-episode a')[0].attrs['href']
    random_movie = soup.table.a.attrs['href']

    return (quote, w_i_t_movie, random_movie)


def t_case(string):
    """
    Title case (w/o articles and such)
    words[0] will always be the episode number
    words[1] will always be capitalized
    """

    no_cap = ['a', 'an', 'the', 'and', 'in', 'but', 'or', 'for', 'of', 'is']
    words = string.split(' ')
    result = [words[0], words[1].capitalize()]

    for word in words[2:]:
        result.append(word) if word in no_cap else result.append(
            word.capitalize())

    return ' '.join(result)


def format_title(title):
    """ Get title ready for printing """

    title = title.replace('/episodes/', '').replace('-', ' ')
    formatted_title = t_case(title)

    return 'Episode {}'.format(formatted_title)


def clear():
    """ Clear screen """

    os.system('clear' if os.name != 'nt' else 'cls')


def add_borders(border, string):
    """ Create borders """

    border = border * len(string)

    return '\n{}\n{}\n{}'.format(border, string, border)


def print_welcome(quote):
    """ Print the welcome message and quote """

    f = Figlet(font='future_7')
    print('')
    print(f.renderText('CLUB MST3K'))
    print('''
    '{}'



                                  MM
                                  MM
                                   MM
                                   .MM
                =M            MM.   MMM
                MMM          MMMMM  .MMM         MM. M
                .M.          MMMMM  .MMM        .MM.MD
                 MM           MMMM  IMMM       .MMMMM
                MMMM          MMMMMMMMMM      MMMM.
                MMMMM.       MMMMMMMMMMN       ..M.
  .MMMMMM,    NMMMMMMMM.  MMMMMMMMMMMMO    .+MMMMMM:     ,MMMMMM.
 MMMMMMMMMM   MMMMMMMMMMM$MMMMMMMMMMMMM  MMMMMMMMMMMM   MMMMMMMMMM
MMMMMMMMMMMM.MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM.MMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM

'''.format(quote.strip()))


def print_info(info, border):
    """ Print the main display for the app """

    clear()
    print_welcome(info[0])
    watch_it_title = format_title(info[1])
    random_title = format_title(info[2])

    print('\nThe watch it together movie is {}'
          .format(add_borders(border, watch_it_title)))
    print('\nYour random pick is {}\n\n{}Enjoy{}\n'
          .format(add_borders(border, random_title), '!' * 32, '!' * 32))


if __name__ == '__main__':2
    print_info(get_info(), '~')
