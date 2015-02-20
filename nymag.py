##########################################
# Jason Kong's code to scrape nymag.com
##########################################
# Note: this code is a lightweight way to accomplish two things
# 1) Scrape a website for data
# 2) Insert it into a database
# It is not meant to replace the larger codebase in this repository...
# it is simply meant as a lightweight alternative to the larger structure
# proposed in this repository.

# Import the necessary libraries: a library that can make http requests, 
# a library to connect with your database, and a library that can
# parse HTML source code into a searchable tree (referenced in the order
# they appeared)
import requests
import sqlite3
from bs4 import BeautifulSoup

# Make an HTTP request to www.nymag.com
# I.e., fetch the HTML source. html_source will now equal
# the same thing you would see had you gone to the website in your
# browser and clicked "View Source" 
html_source = requests.get("http://www.nymag.com")

# Parse the raw HTML source (which is just a string) into something that 
# is searchable
parsed_html=BeautifulSoup(html_source.text)

# Print it so we can see that it actually matches the HTML source we would
# see if we went there with our web browser and clicked "View Source". The
# prettify() method helps us indent it properly so we can easily see its 
# structure.
print(parsed_html.prettify())

# Let's find our first element. This will find a <div> with ID='wrap', and
# within that, it will find a <section> of class='latestNews', and within that, 
# it will find an <a>.
latest_story = parsed_html.select("div#wrap section.latestNews a")[0]

# Within the latest_story element, find the first <h3> element, 
# and store its text in the variable headline. 
headline = latest_story.find('h3').text

# Fetch the href attribute of latest story. This attribute is what contains
# the URL the link is pointing to. 
url = latest_story['href']

# Print the results (for debugging / to make sure you are on the right track)
print(headline)
print(url)

# Initiate a new database connection to your database named nymag.db
# If the database already exists, a connection will simply be established
# to it; if the database doesn't already exist, a it will be created, and then
# a connection will be established to it. The .connect() method returns the
# database connection object, so we store that in a new object called con.
con = sqlite3.connect("nymag.db")

# Create your table. If this is the first time you run this, the table will
# be created, as expected. If this is NOT the first time you run this code, 
# this request will simply be ignored. 
con.execute("CREATE TABLE IF NOT EXISTS articles(id INTEGER PRIMARY KEY NOT NULL, title TEXT NOT NULL, url TEXT NOT NULL UNIQUE)")

# Insert the values of the two variables we stored above (headline and url)
# into the articles table, in columns title and url. Rather than concatenating
# the strings, like we have done in class:

# "insert or ignore into articles(title, url) values(" + headline + "," + url + ")"

# We do it in the way below instead (using ?'s)---this is common in databases
# as it sanitizes---i.e cleans up---the input. If we don't sanitize whatever we input into
# our database, we risk bad things happen. For example, someone could try
# to run commands such as "DROP TABLE articles" in our database.  
# By writing it in the way we do below, we make sure that no "bad" commands
# can get run on our database.
con.execute("INSERT OR IGNORE INTO articles(title, url) VALUES(?,?)",(headline, url))

# Lastly, we commit the changes we have made to the database and close the
# connection. 
con.commit()
con.close()
