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

class getDataFromLinkedinJob(basesinfonierbolt.BaseSinfonierBolt):

    def __init__(self):

        basesinfonierbolt.BaseSinfonierBolt().__init__()

    def userprepare(self):

        self.job = self.getField("jobURL")

    def userprocess(self):
        try:
            req = urllib2.Request(self.job, headers={ 'User-Agent': 'Mozilla/5.0' }) #Creating request
            response = urllib2.urlopen(req) #Opening URL
            web_data = response.read() #Reading response
            soup = BeautifulSoup(web_data, 'html.parser') #HTML Parser
            json_comment = soup.find("code", {"id": "decoratedJobPostingModule"}).string.encode('utf-8','replace')
            jsonData = json.loads(json_comment,'utf-8')#To JSON

            #Getting data
            company = jsonData["decoratedJobPosting"]["jobPosting"]["companyName"]
            title = jsonData["decoratedJobPosting"]["jobPosting"]["title"]
            description = jsonData["decoratedJobPosting"]["jobPosting"]["description"]["rawText"]
            location = jsonData["decoratedJobPosting"]["formattedLocation"]

            job = {}
            job["title"] = title
            job["company"] = company
            job["location"] = location
            job["description"] = description

            self.addField("jobData", job)

        except:
            self.addField("jobData", [])

        self.emit()


    def userclose(self):
        pass

getDataFromLinkedinJob().run()
