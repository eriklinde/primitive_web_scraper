### Instructions for building a primitive, bare-bones web scraper in Python

# On your local machine

## Clone this repository

    git clone https://github.com/eriklinde/primitive_web_scraper.git
    mkdir primitive_web_scraper
    cd primitive_web_scraper

## Install Python Virtual Environment

    pip install virtualenv

## Then create a new virtual environment `venv` 

    virtualenv venv

If you don't know what `virtualenv` is, please refer to its [documentation](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

## Activate your virtual environment

    source venv/bin/activate

## Install any packages you may need

    pip install requests
    pip install beautifulsoup4

If any packages are missing from your code, you will have to install them. This may not be a complete list. 

## Test the code in this repository to make sure everything is running properly, by executing the Python script:

    python scraper.py

It should scrape the `npr.org` website, create a database named `npr.db` in the current directory, and insert information into it. You may inspect that database by opening it up in SQLite:

    sqlite3 npr.db

Make sure the database has some content by querying its tables:

    SELECT * FROM articles;
    SELECT * FROM authors;
    SELECT * FROM works;

Its content should reflect the top story on npr.org.

# Build your own scraper

Once you have confirmed that the above is running properly, please review its code carefully. 

Then build your own web scraper! Use this code as an example (only), rather than as a **strict** requirement as for how to build / structure your app.

Some advice / requirements: 

* Make heavy use of the Python **interpreter** when building your web scraper. You may find that you like [IPython](http://ipython.org/) better than the standard Python interpreter. 

* Make heavy use of Git. As discussed in previous classes, whenever you make sweeping changes to your code (or any changes, for that matter), make sure you use a separate branch from your master branch.

* When you program, one strategy is to build / test out small snippets of code in your interpreter, and then copy / paste them into a file as you go. For example, you may start out by just trying to figure out how to make requests using the `requests` library, and the figure out how to parse the request into a tree using Beautifulsoup. Once you master that, you can move on to the next thing, such as figuring out how to zone in on a specific element of the website you are scraping, and actually get its information. Once you are done with this, you may have `10` or so lines of code, not more. Paste that code into a file! Run your file by typing `python file_name.py`, and make sure your code does what you intend it to do.

* Make heavy use of `print()` statements in your code. Print variables and other informational text as you go along. Once you get more advanced, feel free to start using the Python debugger. You may find that you prefer to use IPython's [debugger](https://pypi.python.org/pypi/ipdb) rather than the standard one.  

* When your file starts to get too busy^[Too many variables, functions, etc.], start to think about structure^[Structuring your variables / functions as **classes** being one example.]. For example, in the code, we created 3 classes, that each contained information relevant to our program. 

* If this is the first time you program, or if you are unfamiliar with web scraping in general, it is a **very bad** idea to take the existing code base included in this repo, and simply try to modify it so that it works for you. Rather, it is better to experiment on your own, and simply use the example code for inspiration or occasional guidance.

# Server side / deployment

Once your code is working **perfectly fine** on your local machine, it's time to deploy it to your server^[A.k.a. putting it into production.]. 

## Issue the following commands on your server in (replace `erik` with your username)

These commands will let you **push** code to your server using `git push`.

    sudo mkdir -p /var/repos/primitive_web_scraper.git
    sudo chown erik:erik /var/repos/primitive_web_scraper.git
    cd /var/repos/primitive_web_scraper.git/
    git init --bare
    cd hooks
    nano post-receive

While editing the `post-receive` file, add the following to the file (once again, replace `erik` with your own username):

	#!/bin/sh
	git --work-tree=/home/erik/primitive_web_scraper --git-dir=/var/repos/primitive_web_scraper.git checkout -f
    chmod +x post-receive

Save and exit out of the editor, and go ahead and create a new directory in your home directory of your server:
    
    mkdir primitive_web_scraper

On local machine (replace `erik` and the IP address with your own information):

    git remote add server ssh://erik@104.236.225.34/var/repos/primitive_web_scraper.git

Then **push** your local code to your server:

    git push server master

Finally, run your program on your server to make sure it works, by running your main Python file through the Python interpreter. For example:

    python my_scraper.py

## Set up your script to run every our using CRON

Instructions to come.
