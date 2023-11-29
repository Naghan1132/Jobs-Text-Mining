# https://scrapeops.io/python-web-scraping-playbook/python-indeed-scraper/
# https://www.scrapingdog.com/blog/scrape-indeed-using-python/



# What Is Error 403 in Python Scraping?

# Error 403 in Python Scraping refers to the HTTP status code Forbidden error that arises when a web server denies your request. 
# Encountering this error when scraping using Python is common due to unique Python libraries' signatures
# and fingerprints that make them easily flagged by anti-bot measures. For example, its default User Agent and incomplete headers identify themselves to the web server as bots.

import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

l=[]
o={}


target_url = "https://fr.indeed.com/jobs?q=Data&l=&from=searchOnHP"

hdr= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive",
}

hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

hdr_indeed = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0'}

#defining header
# hdr= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
#       'AppleWebKit/537.11 (KHTML, like Gecko) '
#       'Chrome/23.0.1271.64 Safari/537.11',
#       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#       'Accept-Encoding': 'none',
#       'Accept-Language': 'en-US,en;q=0.8',
#       'Connection': 'keep-alive'}

#### ####

resp = requests.get(target_url, headers=hdr_indeed)
print("STATUS : ",resp.status_code,"\n")

if resp.status_code == 200:
    print("OK")
elif resp.status_code == 403:
    print("ERROR 403")
    exit()

#### ####

soup = BeautifulSoup(resp.text, 'html.parser')
print(soup)
allData = soup.find("ul",{"class":"jobsearch-ResultsList css-0"})

alllitags = allData.find_all("div",{"class":"cardOutline"})
print(len(alllitags))
for i in range(0,len(alllitags)):
    try:
        o["name-of-the-job"]=alllitags[i].find("a",{"class":"jcs-JobTitle css-jspxzf eu4oa1w0"}).text
    except:
        o["name-of-the-job"]=None

    try:
        o["name-of-the-company"]=alllitags[i].find("div",{"class":"companyInfo"}).find("span",{"class":"companyName"}).text
    except:
        o["name-of-the-company"]=None


    try:
        o["rating"]=alllitags[i].find("div",{"class":"companyInfo"}).find("span",{"class":"ratingsDisplay"}).text
    except:
        o["rating"]=None

    try:
        o["salary"]=alllitags[i].find("div",{"class":"salary-snippet-container"}).text
    except:
        o["salary"]=None

    try:
        o["job-details"]=alllitags[i].find("div",{"class":"metadata taxoAttributes-container"}).find("ul").text
    except:
        o["job-details"]=None

    l.append(o)
    o={}


print(l)