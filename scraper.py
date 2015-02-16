from bs4 import BeautifulSoup
import requests
import sqlite3

DB_PATH = 'npr.db'

class DBAccessLayer(object):
    def __init__(self, path):
        self.database_path = path
        self.open_connection()

    def open_connection(self):
        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row

    def close_connection(self):
        self.connection.close()

    def reset_database(self):
        self.connection.execute("DROP TABLE IF EXISTS authors")
        self.connection.execute("DROP TABLE IF EXISTS articles")
        self.connection.execute("DROP TABLE IF EXISTS works")

    def create_tables(self):
        self.connection.execute("CREATE TABLE IF NOT EXISTS authors(id INTEGER PRIMARY KEY NOT NULL, name TEXT NOT NULL UNIQUE)")
        self.connection.execute("CREATE TABLE IF NOT EXISTS articles(id INTEGER PRIMARY KEY NOT NULL, title TEXT NOT NULL, url TEXT NOT NULL UNIQUE, teaser TEXT NOT NULL, paragraphs TEXT NOT NULL)")
        self.connection.execute("CREATE TABLE IF NOT EXISTS works(id INTEGER PRIMARY KEY NOT NULL, author_id INTEGER NOT NULL, article_id INTEGER NOT NULL, FOREIGN KEY (author_id) REFERENCES authors(id), FOREIGN KEY (article_id) REFERENCES articles(id), UNIQUE (author_id, article_id))")

    def insert_authors_and_article(self, authors, article):
        try:
            cursor = self.connection.cursor()
            for index, value in enumerate(authors):
                cursor.execute("INSERT OR IGNORE INTO authors (name) VALUES (?)", (authors[index].name,))
                result_set = cursor.execute("SELECT id FROM authors WHERE name = ?", (authors[index].name,))
                authors[index].id = result_set.fetchone()['id']
            cursor.execute("INSERT OR IGNORE INTO articles (url, title, teaser, paragraphs) VALUES (?, ?, ?, ?)", (article.url, article.title, article.teaser, article.paragraphs,))
            # import ipdb; ipdb.set_trace()
            result_set = cursor.execute("SELECT id FROM articles WHERE url = ?", (article.url,))
            article.id = result_set.fetchone()['id']
            for index, value in enumerate(authors):
                cursor.execute("INSERT OR IGNORE INTO works (author_id, article_id) VALUES (?, ?)", (authors[index].id, article.id,))
            self.connection.commit()
            print("Inserted article / authors into database.")
        except Exception as e:
            print("***ERROR*** something went wrong:")
            print(e)


class Author(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name


class Article(object):

    def __init__(self, id, url, title, teaser, paragraphs):
        self.id = id
        self.title = title
        self.url = url
        self.teaser = teaser
        self.paragraphs = paragraphs

class NPRScraper(object):

    def __init__(self):
        self.authors = []
        self.article = Article(None, None, None, None, None)

    def scrape(self):
        self.scrape_front_page()
        self.scrape_inside_page()

    def request_and_parse(self, url):
        html_source = requests.get(url)
        return BeautifulSoup(html_source.text)

    def scrape_front_page(self):
        """ Fetch the main news page
        """
        parsed_html = self.request_and_parse('http://www.npr.org/sections/news/')
        featured_tag = parsed_html.select('#featured')[0]

        title_tag = featured_tag.find('h1').find('a')
        self.article.title = title_tag.text.strip()
        self.article.url = title_tag['href']
        teaser = featured_tag.find('p', class_='teaser').find('a')
        teaser_text = teaser.get_text()
        time_teaser_text = teaser.find('time').get_text()
        self.article.teaser = teaser_text.replace(time_teaser_text, '')

    def scrape_inside_page(self):
        """ Fetch details for a news item
        """
        parsed_html = self.request_and_parse(self.article.url)
        authors = parsed_html.select('#storybyline .nameInner')
        for index, value in enumerate(authors):
            authors[index] = Author(None, value.get_text().strip())

        paragraphs = parsed_html.select('#storytext > p')
        concatenated_paragraphs = ''
        for p in paragraphs:
            concatenated_paragraphs += str(p).strip()
        self.article.paragraphs = concatenated_paragraphs
        self.authors = authors


scraper = NPRScraper()
scraper.scrape()

access = DBAccessLayer(DB_PATH)
# access.open_connection()
# access.reset_database()
access.create_tables()
access.insert_authors_and_article(scraper.authors, scraper.article)
access.close_connection()


