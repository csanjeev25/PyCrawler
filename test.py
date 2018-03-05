import urllib3
import json
import re

urllib3.disable_warnings()

def download(url,num_retries=2,user_agent='wswp'):
    html=None
    http = urllib3.PoolManager()
    print("Downloading : {}",(url))
    try:
        headers={'User-agent':user_agent}
        html = http.request('GET',url,headers)
    except Exception as e:
        html=None
        if num_retries > 0:
            if hasattr(e,'code') and 500 <= e.code < 600:
                return(download(url,num_retries))
    if html is not None:
        return html.data

'''def sitemap_crawler(url):
    if url is not None:
        links = download(url).decode('utf-8')
        link = re.findall('<loc>(.*?)</loc>',links)
        for link in links:
            download(link)

sitemap_crawler("http://example.webscraping.com/sitemap.xml")'''


with open('text.html','a+') as data:
    data.write(download("http://httpstat.us/500").decode('utf-8'))
