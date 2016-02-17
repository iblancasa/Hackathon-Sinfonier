
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    The MIT License (MIT)

    Copyright (c) 2015 sinfonier-project

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


from apscheduler.schedulers.background import BackgroundScheduler
from collections import deque
import time
import basesinfonierspout
import json

import urllib2
from bs4 import BeautifulSoup

class TestPySpout(basesinfonierspout.BaseSinfonierSpout):

    def __init__(self):
        basesinfonierspout.BaseSinfonierSpout().__init__()

    def useropen(self):

        self.city = self.getParam("city") #Get city
        self.keywords = str(self.getParam("keywords")).replace(" ", "+")#Get and format keywords

    def usernextTuple(self):
        #Formatting URL
        url="https://es.linkedin.com/jobs/search?keywords=" #URL of jobs
        url+=self.keywords
        url+="&location="
        url+=self.city

        req = urllib2.Request(url) #Creating request
        response = urllib2.urlopen(req) #Opening URL
        web_data = response.read() #Reading response
        soup = BeautifulSoup(web_data, 'html.parser') #HTML Parser
        jobs = soup.findAll("span", { "class" : "job-title-text" })

        job_names = []

        for one_job in jobs:
            if one_job.text=="" or one_job.text==None:
                job_names.append("No title")
            else:
                job_names.append(one_job.text)


        if job_names == []: #No results
            job_names=["No results"]



        self.addField("jobs", job_names)
        self.emit()


    def userclose(self):
        pass


TestPySpout().run()

