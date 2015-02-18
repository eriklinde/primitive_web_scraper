class DBAccessLayer(object):
    """Contains specialized methods to deal with connections to an SQLite database, 
    as well as inserting elements into the database. Built to use with the
    web scraping project Pen and Paper Coding Level II.
    """

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


