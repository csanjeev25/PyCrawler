import re
import urllib3
import lxml.html
import urllib
import csv
from bs4 import BeautifulSoup
import time
import sys
import traceback

FIELDS = ('area', 'population', 'iso', 'country', 'capital',
'continent', 'tld', 'currency_code', 'currency_name', 'phone',
'postal_code_format', 'postal_code_regex', 'languages',
'neighbours')

def re_scraper(html):
    results = {}
    for field in FIELDS:
        if re.search('<tr id="places_%s__row">.*?<td class="w2p_fw">(.*?)</td>' % field, html) is not None:
            results[field] = re.search('<tr id="places_%s__row">.*?<td class="w2p_fw">(.*?)</td>' % field, html).groups()[0]
    return results

def bs_scraper(html):
    results={}
    soup=BeautifulSoup(html,'html.parser')
    for field in FIELDS:
        results[field] = soup.find('table').find('tr',id='places_%s__row'%field).find('td',class_='w2p_fw').text
    return results

def lxml_scraper(html):
    results={}
    tree=lxml.html.fromstring(html)
    for field in FIELDS:
        results[field]=tree.cssselect('table > tr#places_%s__row > td.w2p_fw'%field)[0].text_content()
    return results

def download(url):
    http=urllib3.PoolManager()
    html=http.request("GET",url)
    return html.data

NUM_ITERATIONS = 1000 # number of times to test each scraper
html = download('http://example.webscraping.com/places/default/view/Afghanistan-1')
for name, scraper in [('Regular expressions', re_scraper),('BeautifulSoup', bs_scraper),('Lxml', lxml_scraper)]:
    start = time.time()
    for i in range(NUM_ITERATIONS):
        if scraper == re_scraper:
            re.purge()  #clear cache
            result = scraper(html.decode('utf-8'))
        elif scraper == bs_scraper:
            result=scraper(html)
        else:
            result == scraper(html.decode('utf-8'))
        if result is not None:
            try:
                assert(result['area'] == '244,820 square kilometres') # check scraped result is as expected
            except KeyError:
                pass
            except AssertionError:
                pass
    end = time.time()  # record end time of scrape and output the total
    dif=end-start
    print('%s: %.2f seconds'%(name, dif))
