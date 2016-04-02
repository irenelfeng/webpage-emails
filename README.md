#webpage-emails
A python program that will take an internet domain name (e.g. “jana.com”) and prints out a list of the email addresses that were found on that website. It finds email addresses on any discoverable page of the website.

## Sample Usage
`python find_email_addresses.py -domain geography.dartmouth.edu`
Sample output: 
```
Found these email addresses:
gail.m.patten@dartmouth.edu
elaine.p.livingston@dartmouth.edu
esteban.castano@dartmouth.edu
conferences.and.events@dartmouth.edu
Xun.Shi@Dartmouth.edu
laura.e.conkey@dartmouth.edu
rockefeller.center@dartmouth.edu
```
...


## Installation
Here are command line options to install certain libraries before the running `---.py`
```
$ git clone https://github.com/irenelfeng/webpage-emails.git
$ cd webpage-emails
$ pip install argparse
$ pip install beautifulsoup4
$ python find_email_addresses.py
```