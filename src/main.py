from webpage import webpage
from Extracter import Scraper

k=input("Enter product name : ")

scraper = Scraper()
scraper.set_query(k)
k=scraper.scrape()
webpage(k)
scraper.close()

