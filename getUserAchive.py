user = "bolexman"

import urllib2
from bs4 import BeautifulSoup


url = "https://archive.org/details/@"+user
req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' }) #Creating request
response = urllib2.urlopen(req) #Opening URL
web_data = response.read() #Reading response
soup = BeautifulSoup(web_data, 'html.parser') #HTML Parser

userData = {}
userData["name"] = user

img = soup.find("img",{"id":"file-dropper-img"})
userData["avatar"] = img["src"]

numbers = soup.findAll("h3", {"class":"co-top-row"})

userData["uploads"] = numbers[0].contents[0].replace(" ","").replace("\n","")
userData["collections"] = numbers[1].contents[0].replace(" ","").replace("\n","")

topicsLinks = soup.find("div", {"class": "facet-subject"}).findAll("a")

topics = []

for link in topicsLinks:
    topics.append(link.text)

userData["topics"] = topics

url+="#posts"
req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' }) #Creating request
response = urllib2.urlopen(req) #Opening URL
web_data = response.read() #Reading response
soup = BeautifulSoup(web_data, 'html.parser') #HTML Parser

rows = soup.findAll("tr",{"class": "forumRow"})

userPosts = []
for r in rows:
    post = {}
    post["url"] = r.findAll("td")[0].find("a")["href"]
    post["title"] = r.findAll("td")[0].find("a").text
    userPosts.append(post)

userData["latestPosts"] = userPosts
