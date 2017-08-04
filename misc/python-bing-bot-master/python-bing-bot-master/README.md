python-bing-bot
===============

A bot for earning Bing Rewards on multiple accounts, written in Python.
Supports earning mobile search points, and can automatically claim the 
"Free Daily Point".

This bot is based on work done on a Ruby project by TillerMiller.
https://github.com/TillerMiller/BingBot

The bot takes a YAML file as a configuration input, logs in to Facebook or Outlook, 
attempts to detect the number of searches needed for daily points, and then carries
out those searches systematically by either using faked input from the Faker class,
or hitting the iHeartQuotes API for a random quote.

What you need:

- Google Chrome
- The Google Chrome Driver Server * : http://chromedriver.storage.googleapis.com/index.html
- Selenium Webdriver (Python) : http://docs.seleniumhq.org/download/
- PyYAML : http://pyyaml.org
- Faker : https://pypi.python.org/pypi/Faker/0.0.4

The Chrome Driver Server is a separate piece of the Selenium Webdriver puzzle. This current
bot build is running successfully on today's latest Chrome Driver version (2.10). Right now
this can be found at http://chromedriver.storage.googleapis.com/index.html?path=2.10/

For OSX please download the Linux 64 bit zip. The resulting file is called `chromedriver`. Please
move this file to `/usr/bin`. On OSX you can use the keyboard shortcut `cmd+shift+g` to navigate
to this directory (it is hidden by default). Moving the file here will require admin privileges.

You could also do it from the command line:

    cd /path/to/chromedriver
    sudo mv chromedriver /usr/bin
    
You must also uncomment a line in the `config.yaml` file beneath the `CHROMEDRIVER_PATH:` line.
On Linux or OSX take out the `#` in front of /usr/bin and on Windows the C:\chromedriver. You can 
optionally set the absolute path if you prefer to store the chromedriver somewhere else.
    
For some reason the chromedriver binary is difficult to get working. If you are having trouble please
open an issue on this repository so we can crowdsource the solutions. I had trouble getting chromedriver
to work initially. The error messages that selenium throws about problems point to a generic wiki, 
https://code.google.com/p/selenium/wiki/ChromeDriver
    

Unpack all the other archives and install them according to the directions given on each website.
On OSX this usually entails

    cd /path/to/files
    sudo python setup.py install

Config Setup:
Add email addresses to the config.yaml file as follows

    FACEBOOK_EMAIL:
    - emailAddress
    FACEBOOK_PASSWORD:
     - password
    OUTLOOK_EMAIL:
     - emailAddress
    OUTLOOK_PASSWORD:
     - password

Be mindful of the SPACE, DASH, SPACE before any config inputs.

List as many emails as necessary (Bing has a 5 account per IP/household limit, caveat emptor)


Usage
Mac, Linux : 

    cd /path/to/PythonBingBot
    python PBB.py
