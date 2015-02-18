"""Structures the information from NPR into classes, which will
match the way we store them in the database.
"""

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

