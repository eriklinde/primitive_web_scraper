from flask import render_template
from flask import Flask
app = Flask(__name__)

@app.route('/')
def articles():
    return "Hello!"

if __name__ == '__main__':
    app.run(debug=True)
