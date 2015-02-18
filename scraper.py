class NPRScraper(object):
    """This is a simple web scraper that scrapes
    npr.org's main news site. It fetches the content of the main
    news article on the site, and also stores its content in the object.  
    """

    def __init__(self):
        # This object:
        self.authors = []
        self.article = Article(None, None, None, None, None)

    def scrape(self):
        self.scrape_front_page()
        self.scrape_inside_page()

    def request_and_parse(self, url):
        html_source = requests.get(url)
        return BeautifulSoup(html_source.text)

    def scrape_front_page(self):
        """ Fetch the main news page from npr.org.
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
        """ Fetch the actual article content for the news article
        referenced on the front page of NPR. The url to fetch is assumed
        to be stored in the instance variable url (which will be set
        when running scrape_front_page.
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


