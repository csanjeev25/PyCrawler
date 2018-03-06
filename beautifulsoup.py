from bs4 import BeautifulSoup
import urllib3
import sys

http=urllib3.PoolManager()
response=http.request("GET",'http://www.cricbuzz.com/')
soup=BeautifulSoup(response.data,'html.parser')  #parse html
response=soup.prettify()
ul=soup.find('ul',attrs={'class':'cb-ftr-ul'})

#print(ul)
#print(ul.find('li'))
#print("\n\n\n\n\n")
#print(response)
#print(ul)
#print(type(ul))
#print(ul.find_all('li'))

cool = soup.find_all(attrs={'class':'cb-subnav-item cb-sub-lg-sec-item'})
coool=soup.find_all('a',attrs={'class':'cb-hm-mnu-itm','href':'/cricket-match/live-scores','title':"Live Cricket Score"})
print(coool)

with open('text.html','w') as f:
    f.write(response.encode('cp850','replace').decode('cp850'))
