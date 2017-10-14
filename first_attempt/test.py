import scrapers
import processors

hp = scrapers.Homepage_scraper()
p = processors.Data_processor()

p.process_homepage_data(hp.data)

print(hp.episode_links)
