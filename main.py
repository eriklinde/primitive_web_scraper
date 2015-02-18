# Web scraping libraries
from bs4 import BeautifulSoup
import requests

# Databases
import sqlite3

# Our own classes
from data_structure import Author
from data_structure import Article
from db_connectivity import DBAccessLayer 

# The name of the database file
DB_PATH = 'npr.db'

# Instantiate an NPRScraper object and perform the scraping of NPR
# the information scraped gets stored in the scraper object
scraper = NPRScraper()
scraper.scrape()

# Insert the information from the Scraper object into the database
# Start by creating a new instance of DBAccessLayer
access = DBAccessLayer(DB_PATH)

# This creates the tables. If the database already exists, nothing happens.
access.create_tables()

# This inserts the new information into the tables. Only "new" information
# will be inserted, as some of the columns have been defined with
# UNIQUE constraints. 
access.insert_authors_and_article(scraper.authors, scraper.article)

# Close the database connection when we are done!
access.close_connection()


