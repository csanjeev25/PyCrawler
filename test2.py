import re
import urllib3
import urllib
from datetime import datetime
import urllib.robotparser
import queue

urllib3.disable_warnings() #disable certificate related warnings


def link_crawler(seed_url,link_regrex=None,delay=5,max_depth=2,max_urls=2,headers=None,proxy=None,num_retries=1,user_agent='wswp'):
    #start crawling bitch
    print(seed_url)
    crawl_queue=queue.deque()
    crawl_queue.append(seed_url)
    seen={seed_url:0}   # the URL's that have been seen and at what depth
    num_urls=0
    rp=get_robots(seed_url)
    trottle=Trottle(delay)
    headers=headers or {}
    if user_agent:
        headers['User-agent']=user_agent
    while crawl_queue:
        url=crawl_queue.pop()
        #if rp.can_fetch(user_agent,url):
        if True:
            trottle.wait(url)
            html=download(url,headers,proxy=proxy,num_retries=num_retries)
            links=[]
            depth=seen[url]
            if depth!=max_depth:
                if link_regrex:   # filter for links matching our regular expression
                    links.extend(link for link in get_links(html.decode('utf-8')) if re.match(link_regrex,link))

                for link in links:
                    link = normalize(seed_url,link)
                    if link not in seen:
                        seen[link]=depth+1
                        if same_domain(seed_url,link):
                            crawl_queue.append(link)
            num_urls+=1
            if num_urls==max_urls:
                break
    else:
        print("Blocked in robots.txt:{}}",url)

def download(url,headers,proxy,num_retries,data=None):
    print("Downloading:{}".format(url))
    try:
        if proxy:
            html=proxy.request("GET",url,headers)
        else:
            http=urllib3.PoolManager()
            html=http.request("GET",url,headers)
            code=html.status
    except urllib.error.URLError as e:
        print("Download error:{}".format(e.__cause__))
        html=''
        if hasattr(e,'errno'):
            status=e.errno
            if num_retries>0 and 500 <= status < 600:
                return download(url, headers, proxy, num_retries-1, data)
        else:
            status=None
    return html.data

def normalize(seed_url,link):   #Normalize this URL by removing hash and adding domain eg:'HTTP://www.Python.org/doc/#' to http://www.Python.org/doc/  and here urllib.parse.urlparse returns Parse a URL into six components, returning a 6-tuple. This corresponds to the general structure of a URL: scheme://netloc/path;parameters?query#fragment.
    link,_ = urllib.parse.urldefrag(link)
    return urllib.parse.urljoin(seed_url,link)

def same_domain(url1,url2):
    return urllib.parse.urlparse(url1).netloc == urllib.parse.urlparse(url2).netloc   #netloc gives us the hostname only i.e if url is http://www.cricbuzz.com/live-score only gives hostname=www.cricbuzz.com

def get_links(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE) # a regular expression to extract all links from the webpage
    return webpage_regex.findall(html)

def get_robots(url):
    rp=urllib.robotparser.RobotFileParser()
    rp.set_url(urllib.parse.urljoin(url,'/robots.txt'))
    rp.read()
    return(rp)

class Trottle:
    def __init__(self,delay):
        self.delay=delay        # amount of delay between downloads for each domain
        self.domains={}         # timestamp(when) of when a domain was last accessed

    def wait(self,url):
        domain=urllib.parse.urlparse(url).netloc  #This returns main hostname eg.www.cricbuzz.com
        last_accessed=self.domains.get(domain)

        if self.delay>0 and last_accessed is not None:
            sleep_secs=self.delay-(datetime.now-last_accessed).seconds
            if sleep_secs>0:
                time.sleep(sleep_secs)
        self.domains[domain]=datetime.now()

if __name__ == '__main__':
    link_crawler('https://www.cricbuzz.com/', delay=0, num_retries=1)
    link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, max_depth=1,user_agent='GoodCrawler')
