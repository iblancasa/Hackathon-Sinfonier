import urllib2
from bs4 import BeautifulSoup

url = "https://es.linkedin.com/jobs/search?keywords=Informatica&location=Granada"



req = urllib2.Request(url) #Creating request
response = urllib2.urlopen(req) #Opening URL
web_data = response.read() #Reading response
soup = BeautifulSoup(web_data, 'html.parser') #HTML Parser


print("*********************")
a = soup.findAll("span", { "class" : "job-title-text" })
for j in a:
    print(j.text)
