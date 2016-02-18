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

class getOffersLinkedinCityKeywords(basesinfonierbolt.BaseSinfonierBolt):

    def __init__(self):

        basesinfonierbolt.BaseSinfonierBolt().__init__()

    def userprepare(self):
        self.city = self.getParam("city") #Get city
        self.keywords = str(self.getParam("keywords")).replace(" ", "+")#Get and format keywords


    def userprocess(self):
        #Formatting URL
        url="https://es.linkedin.com/jobs/search?keywords=" #URL of jobs
        url+=self.keywords
        url+="&location="
        url+=self.city

        try:
            req = urllib2.Request(url) #Creating request
            response = urllib2.urlopen(req) #Opening URL
            web_data = response.read() #Reading response
            soup = BeautifulSoup(web_data, 'html.parser') #HTML Parser
            totalJobs = soup.findAll("div", { "class" : "results-context" })

            #Get all results in one webpage
            total_results = totalJobs[0].findChildren()[0].text

        except:
            self.addField("jobData", {})
            self.emit()
            return

        if not totalJobs or len(totalJobs)==0:#No results
            self.addField("jobData", {})
            self.emit()
            return


        url+="&start=1&count="+total_results

        #Formatting new URL
        try:
            req = urllib2.Request(url) #Creating request
            response = urllib2.urlopen(req) #Opening URL
            web_data = response.read() #Reading response
            soup = BeautifulSoup(web_data, 'html.parser') #HTML Parser
            jobs = soup.findAll("a", { "class" : "job-title-link" })
        except:
            self.addField("jobData", {})
            self.emit()
            return

        for current_job in jobs:
            new = {}

            try:
                new["url"] = current_job['href']
                new["name"] = current_job.text
                self.addField("jobData", new)
            except:
                new["url"] = ""
                new["name"] = ""
            self.emit()


    def userclose(self):
        pass

getOffersLinkedinCityKeywords().run()
