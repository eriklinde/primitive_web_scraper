### Instructions for building a primitive, bare-bones web scraper in Python

# On your local machine

## Clone this repository

    git clone https://github.com/eriklinde/primitive_web_scraper.git
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

(this may not be a complete list)

## Test the code in this repository to make sure everything is running properly, by executing the Python script:

    python scrape.py

It should scrape the `npr.org` website, create a database named `npr.db` in the current directory, and insert information into it. You may inspect that database by opening it up in SQLite:

    sqlite3 npr.db

Make sure the database has some content by querying its tables:

    SELECT * FROM articles;
    SELECT * FROM authors;
    SELECT * FROM works;

Its content should reflect the top story on npr.org.

# Build your own scraper

Once you have confirmed that the above is running properly, please review its code carefully.

Then build your own web scraper! Use this code as an example (only), rather than as a **strict** requirement as for how to build / structure your app. You are welcome to use a different name than `primitive_web_scraper`, which I have used throughout the remaining instructions. If you change names, make sure you are consistent---i.e., change names in all locations.

## Some advice / requirements:

* Make heavy use of the Python **interpreter** when building your web scraper. You may find that you like [IPython](http://ipython.org/) better than the standard Python interpreter.

* Make heavy use of Git. As discussed in previous classes, whenever you make sweeping changes to your code (or any changes, for that matter), make sure you use a separate branch from your master branch.

    Also, create a new repository on your Github profile so you can share your code with the instructor and other students. Be sure to regularly push your code to that repository.

* When you program, one strategy is to build / test out small snippets of code in your interpreter, and then copy / paste them into a file as you go. For example, you may start out by just trying to figure out how to make requests using the `requests` library, and the figure out how to parse the request into a tree using Beautifulsoup. Once you master that, you can move on to the next thing, such as figuring out how to zone in on a specific element of the website you are scraping, and actually get its information. Once you are done with this, you may have `10` or so lines of code, not more. Paste that code into a file! Run your file by typing `python file_name.py`, and make sure your code does what you intend it to do.

* Make heavy use of `print()` statements in your code. Print variables and other informational text as you go along. Once you get more advanced, feel free to start using the Python debugger. You may find that you prefer to use IPython's [debugger](https://pypi.python.org/pypi/ipdb) rather than the standard one.

* When your file starts to get too busy (too many variables, functions, etc.), start to think about structure, with structuring your variables / functions as **classes** being one example. For example, in the code, we created 3 classes, that each contained information relevant to our program. Separating our code into classes made our code easier to read. As you get more advanced, you will probably start to think about structure earlier on, but at this stage, please don't worry too much about it until your code simply becomes too difficult to manage without structure.

* If this is the first time you program, or if you are unfamiliar with web scraping in general, it is a **very bad** idea to take the existing code base included in this repo, and simply try to modify it so that it works for you. Rather, it is better to experiment on your own, and simply use the example code for inspiration or occasional guidance. In other words, please code your app from scratch.

# Server side / deployment

Once your code is working **perfectly fine** on your local machine, it's time to deploy it to your server, a.k.a. putting it into production.

## Issue the following commands on your server (replace `erik` with your username)

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

Save and exit out of the editor, and add `execute` permissions to the `post-receive` file as follows:

    chmod +x post-receive

Then go ahead and create a new directory in your home directory of your server:

    cd ~
    mkdir primitive_web_scraper

On your local machine (replace `erik` with your own information and the `xxx` with your server's IP address):

    git remote add server ssh://erik@xxx.xxx.xxx.xx/var/repos/primitive_web_scraper.git

Then **push** your local code to your server:

    git push server master

Once again on your server; inspect your scraper directory to make sure the files are there:

    cd ~
    cd primitive_web_scraper

This should match with what you have locally. Now go ahead and create a virtual environment on your server in the same way you did on your local machine (you will or may have to install the packages below before doing so):

    sudo apt-get install sqlite3
    sudo apt-get install python-pip
    sudo pip install virtualenv



Finally, activate your virtual environment, and run your program on your server to make sure it works, by running your main Python file through the Python interpreter. For example, if your main file's name is `scrape.py`, then type:

    python scrape.py

## Set up your script to run every hour using CRON

Cron is a tool available by default in nearly all UNIX / Linux distributions. It lets the user run a task, a.k.a. a background job at set intervals. For example, if you wanted your scraper to run automatically every our, Cron would be excellent at the job. 

To make Cron perform a task for you, you will need to add the task as a Cronjob. Let's open up the "Cron job editor" to see how we might do that (this assumes that you are currently on your server):

    crontab -e

The first time you issue this command, Cron will ask you to specify your default editor for when editing Cron jobs. Pick an editor that you feel comfortable with, for example Nano. Let's start out by editing your crontab to say the following:

    * * * * * python scrape.py

This command won't actually work the way it is currently written, but we will tweak it in the lines to follow so that it does. Let's first review the two parts that a Cron command consists of:

1) Schedule ( the `* * * * *`), and
2) The actual command to run (`python scrape.py`)

The schedule of a Cron command currently consists of 5 consecutive `*`'s. Translated into Cron syntax, this is equivalent to saying that we want our command to run **every minute**. Here is what each of the asterisks symbolize (in order):

* Minute
* Hour
* Day of the month
* Month
* Day of the week

The most often we can run a cron command is once a minute (`* * * * * `). Think of the `*` to read as the word *every*, so that `* * * * * ` becomes:

    Run on every minute of every hour of every day of every month of every day of the week. 

If we change that to (`5 * * * *`), our schedule will instead read:

    Run on minute #5 of every hour of every day of every month of every day of the week.

In other words, whenever we have a number instead of an asterisk, replace it with syntax similar as to how it was done above. 

How might we then run something every Wednesday at 4.30pm? 

    30 16 * * 3

(note here that 16 is the 24h version of 4pm, and 3 represents Wednesdays). We can read the above as:

    Run on minute #30 of hour #16 of every day of every month of day #3 of the week

For our purposes, it may be suitable to run our scraper every time we suspect the headlines might update, which might be twice an hour. This means that we would, for example, like our scraper to run on minute 0, and minute 30. In that case, we need to separate those two values by a comma (`,`), like so: 

    0,30 * * * * 

The next thing in our command is what to actually **run**. The way our command currently reads is as follows:

     0,30 * * * * python scrape.py

This means that on minute #0 and minute #30 Cron will invoke the command `python scrape.py`. There are two problems with that:

1. Cron won't be using the Virtual Environment we set up previously (and therefore won't have access to our python interpreter, our libraries / packages, etc.)
2. Cron will be looking for a file named `scrape.py` in the directory from which it was launched, which will **not** be the directory in which your `scrape.py` exists.

To overcome the two problems above, let's modify the Cron script as follows: 

     0,30 * * * * /home/erik/primitive_web_scraper/venv/bin/python /home/erik/primitive_web_scraper/scrape.py

Exit out of the Cron editor, and sit back and wait---Cron will now run your program every half hour. Note that we are instructing Cron to run our program using the Python interpreter located in our Virtual Environment directory (i.e. `venv/bin/python`).

# Setting up a Flask web server

Note: this will be an extremely brief tutorial to Flask, a lightweight web framework. 

# Deploying your app on your server

## Upgrade to Python 3.4.1

(I couldn't get uWSGI to work with Python 3.4.0)

On your server:

    sudo apt-get install libssl-dev openssl
    sudo apt-get install build-essential
    sudo apt-get install python3-dev
    sudo apt-get install libsqlite3-dev

    wget https://www.python.org/ftp/python/3.4.1/Python-3.4.1.tgz
    tar -xvf Python-3.4.1.tgz
    cd Python-3.4.1/
    ./configure
    make
    sudo make install

Delete any existing virtual environments (we will create a new one using the Python 3.4.1 installation):

    cd ~/primitive_web_scraper
    rm -rf venv/

Make sure that your python3.4 binary has been updated to 3.4.1 by running it and noting the version number:

    python3.4

(make sure that it indeed says 3.4.1 as you run your interpreter, then exit out of the interpreter by typing `exit()`!)

Create a new virtual environment: 

    virtualenv venv
    source venv/bin/activate

    pip install flask
    pip install uwsgi
    pip install requests
    pip install beautifulsoup4

    which uwsgi

(your `uwsgi` binary should point to the uWSGI in your venv directory)

Test your web application / web server by running it as follows:

    python web.py

This should start up a new server that listens on the address / port indicated below: 

    Running on http://0.0.0.0:5000/ (Press CTRL+C to quit) 

Make sure your `app.run()` command inside of `web.py` looks like this:

    app.run(debug=True, host='0.0.0.0')

From your laptop's browser, visit your server's IP address followed by the port `5000` as follows (remember to replace the IP address with your own information):

    http://104.236.225.34:5000/

If you see the expected output, that means that your web server is correctly connecting to the database and displaying the right information. It's then time to set set up **uWSGI** and **NGINX**, and let them take over, as the built-in web server we have been using for development so far is not suitable for any meaningful amounts of traffic.

Start up your uWSGI server by issuing the following command, which will take your file name as an input, as well as your `app` object. 

    venv/bin/uwsgi --socket 127.0.0.1:3031 --wsgi-file web.py --callable app

We are starting our uWSGI server on address `127.0.0.1` (also known as *localhost*, which is the address your computer accesses itself) and on port `3031`---you could have selected any port above `1024`. An important difference between running a server on address `0.0.0.0` and `127.0.0.1` is that the latter doesn't allow outside access, whereas the former does. This is the reason why we were able to access our website from our development machines on `http://104.236.225.34:5000` as we were running it on `0.0.0.0`.

At this point, uWSGI is ready to receive traffic from NGINX. Let's update our `nginx.conf` file to read as follows: 

    events {}
    http {
        server {
            location / {
                uwsgi_pass 127.0.0.1:3031;
                include uwsgi_params;
            }
        }
    }

We are here simply telling NGINX to pass on all incoming traffic to `127.0.0.1:3031`, which is where our uWSGI server (which serves as the interface between our Flask app and NGINX) is listening. 

Test your NGINX setup using 

    sudo nginx -t

, and provided it is working, reload your settings using

    sudo service nginx reload

Your server should now be working!
