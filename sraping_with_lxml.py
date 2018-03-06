import lxml.html
import urllib3


http=urllib3.PoolManager()
response=http.request("GET",'http://www.cricbuzz.com/')

html=lxml.html.fromstring(response.data)
response=lxml.html.tostring(html,pretty_print=True).decode('utf-8')  #lxml.html.HtmlElement

div=html.cssselect('div[ng-if^=run_active]')       #list

for divtag in div:
    print(divtag.text_content())
    print("\n")

'''with open('text.html','w') as f:
    f.write(response.decode('utf-8').encode('cp850','replace').decode('cp850'))'''
