from db_connectivity import DBAccessLayer
from flask import render_template
import sqlite3
from flask import Flask
app = Flask(__name__)

@app.route('/')
def articles():
    access = DBAccessLayer('npr.db')
    articles = access.get_all_articles()
    return render_template('index.html', articles=articles, access=access)

if __name__ == '__main__':
    app.run(debug=True)
