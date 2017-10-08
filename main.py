from scrapers import Homepage_scraper
from scrapers import Movie_page_scraper
from mst_bot import Club_mst3k_info_bot


if __name__ == '__main__':
  cmib = Club_mst3k_info_bot(Homepage_scraper, Movie_page_scraper)
