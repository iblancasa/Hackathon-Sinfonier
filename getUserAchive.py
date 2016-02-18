#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    The MIT License (MIT)

    Copyright (c) 2014 sinfonier-project

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""


import basesinfonierbolt
import datetime
import json
import urllib2
from bs4 import BeautifulSoup

class getDataFromArchiveUser(basesinfonierbolt.BaseSinfonierBolt):

    def __init__(self):

        basesinfonierbolt.BaseSinfonierBolt().__init__()

    def userprepare(self):

        self.user = self.getField("user")

    def userprocess(self):
        url = "https://archive.org/details/@"+self.user
        try:
            req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' }) #Creating request
            response = urllib2.urlopen(req) #Opening URL
            web_data = response.read() #Reading response
            soup = BeautifulSoup(web_data, 'html.parser') #HTML Parser
        except: #No data get from the user
            self.addField("userData", [])
            self.emit()
            return

        userData = {}
        userData["name"] = self.user

        #Get avatar URL
        try:
            img = soup.find("img",{"id":"file-dropper-img"})
            userData["avatar"] = img["src"]
        except:
            userData["avatar"]=""

        #Get number of uploads and collections
        try:
            numbers = soup.findAll("h3", {"class":"co-top-row"})
            userData["uploads"] = int(numbers[0].contents[0].replace(" ","").replace("\n",""))
            userData["collections"] = int(numbers[1].contents[0].replace(" ","").replace("\n",""))
        except:
            userData["uploads"] = 0
            userData["uploads"] = 0

        #Get topics and topic links
        try:
            topicsLinks = soup.find("div", {"class": "facet-subject"}).findAll("a")
            topics = []
            for link in topicsLinks:
                topics.append(link.text)
            userData["topics"] = topics
        except:
            userData["topics"]=[]

        #Get posts of user and links
        try:
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
        except:
            userData["latestPosts"] = []

        self.addField("userData", userData)
        self.emit()


    def userclose(self):
        pass

getDataFromArchiveUser().run()
