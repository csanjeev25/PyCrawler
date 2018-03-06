import re
import urllib3

url = 'http://example.webscraping.com/view/UnitedKingdom-239'
def download(url):
    http=urllib3.PoolManager()
    response=http.request("GET",url)
    #print(response.data)
    return response.data.decode('utf-8')

print(re.findall('<td (.*?)>(.*?)</td>', download(url)))
