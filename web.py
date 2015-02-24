from db_connectivity import DBAccessLayer
from flask import render_template
import sqlite3
from flask import Flask
import os
app = Flask(__name__)
DB_NAME = 'npr.db'

@app.route('/')
def articles():
    access = DBAccessLayer(os.path.dirname(os.path.realpath(__file__)) + "/" + DB_NAME)
    articles = access.get_all_articles()
    return render_template('index.html', articles=articles, access=access)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
