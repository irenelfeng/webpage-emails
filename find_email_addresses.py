import sys 
import argparse
import requests
import re
from BeautifulSoup import BeautifulSoup
from collections import deque
from urlparse import urlparse

def get_page(page):
    """if page can be found and retrieved, return the page"""
    try: 
        response = requests.get(page)
        content = BeautifulSoup(response.text.encode("utf-8",'ignore'))
    except: #RequestErrors, UnicodeErrors
        return None
    return content

def get_all_urls(page, domain_name):
    """
    given a url and domain name, return: urls in that page with that domain name.
    """
    page_list = []

    for link in page.findAll('a', href=True): 
        # if a relative link
        if not (link['href'].startswith("http://") or link['href'].startswith("https://")):
            
            if link['href'].startswith("/"):
                page_list.append("http://"+domain_name+link['href'])
            else: page_list.append("http://"+domain_name+'/'+link['href'])

        # if a absolute link, check if hostname is domain name
        elif urlparse(link['href']).hostname == domain_name:
            page_list.append(link['href'])

    return page_list

def get_emails(page):
    """given page, get list of emails in the page"""
    return set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(page), re.I))

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-domain', type=str, help='domain name of which will return all email addresses found on any page of the domain', required=True)
    args = parser.parse_args()

    domain = args.domain
    # add http:// to domain
    if not domain.startswith("http://"):
        domain_url = "http://"+domain
    page = get_page(domain_url)
    if page == None:
        print "We could not find " + str(domain) + " on the internet. Try another domain."
        sys.exit()

    crawling = deque([domain_url])
    #list of urls we have already crawled
    url_list = set([domain_url])
    #list of emails we have gotten
    emails = set()

    while len(crawling) > 0:
        # move next url from the queue to the set of processed urls
        url = crawling.popleft()
        # get page
        page = get_page(url)
        if page != None:
            # add any emails from the page
            emails.update(get_emails(page))

            # add new_page to deque if not in the set of urls already crawled
            for new_url in get_all_urls(page, domain):

                if new_url not in url_list:
                    crawling.append(new_url)
                    url_list.add(new_url)

    if len(emails) > 0:
        print "Found these email addresses:"
        for email in emails:
            print email

    else:
        print "No emails listed in this domain."



