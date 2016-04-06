import sys 
import argparse
import re
from BeautifulSoup import BeautifulSoup
from collections import deque
from urlparse import urlparse
from selenium import webdriver

def start_up_driver():
    driver = webdriver.PhantomJS()
    return driver

def close_driver():
    driver.quit()

def get_page(driver, page):
    """if page can be found and retrieved, return the page"""
    try: 
        driver.get(page)
        response = driver.page_source

        content = BeautifulSoup(response.encode("utf-8",'ignore'))
    #except requests.exceptions.ConnectionError: 
        # return None
    except UnicodeError:
        print "Unicode error on " + page + ". Skipping..."
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

# def angular_get_urls(page, domain_name):
#     page_list = []

#     angular_tag = "changeRoute"
#     for link in page.findAll(True, {"ng-click":True}):
#         if link['ng-click'].startswith(angular_tag):
#             url = link['ng-click'][len(angular_tag):]
#             # strip punctuation
#             url = re.sub(r'[^\w\s]','',url) 
#             page_list.append("http://"+domain_name+'/'+url)

#     return page


def get_emails(page):
    """given page, get list of emails in the page"""
    return set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(page), re.I))

def http_domain(domain):
    """adds http:// to domain """ 
    if not domain.startswith("http://"):
        domain_url = "http://"+domain
    return domain_url

def output(emails):
    """given a list of emails, print them out"""

    if len(emails) > 0:
        print "Found these email addresses:"
        for email in emails:
            print email

    else:
        print "No emails listed in this domain."

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-domain', type=str, help='domain name of which will return all email addresses found on any page of the domain', required=True)
    args = parser.parse_args()
    
    domain = args.domain
    domain_url = http_domain(domain)

    #initialize variables
    # list of urls need to crawl
    crawling = deque([domain_url])
    #list of urls we have already crawled
    url_list = set([domain_url])
    #list of emails we have gotten
    emails = set()
    #PhantomJS driver
    driver = start_up_driver()

    # crawls each webpage in the stack crawling
    while len(crawling) > 0:
        # move next url from the queue to the set of processed urls
        url = crawling.popleft()
        # get page
        page = get_page(driver, url)

        if page != None:
            # add any emails from the page
            emails.update(get_emails(page))

            # add new_page to deque if not in the set of urls already crawled
            for new_url in get_all_urls(page, domain):
                if new_url not in url_list:
                    crawling.append(new_url)
                    url_list.add(new_url)

    close_driver()
    output(emails)



