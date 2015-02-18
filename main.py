# Web scraping libraries
from bs4 import BeautifulSoup
import requests

# Databases
import sqlite3

# Our own classes
from data_structure import Author
from data_structure import Article
from db_connectivity import DBAccessLayer 

DB_PATH = 'npr.db'

# Instantiate an NPRScraper object and perform the scraping of NPR
# the information scraped gets stored in the scraper object
scraper = NPRScraper()
scraper.scrape()

# Insert the information from the Scraper object into the database
access = DBAccessLayer(DB_PATH)
access.create_tables()
access.insert_authors_and_article(scraper.authors, scraper.article)
access.close_connection()


