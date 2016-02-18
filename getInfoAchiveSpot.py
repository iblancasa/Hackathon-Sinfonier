
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

import time
import basesinfonierspout
import json
import urllib2

class TestPySpout(basesinfonierspout.BaseSinfonierSpout):

    def __init__(self):
        basesinfonierspout.BaseSinfonierSpout().__init__()

    def useropen(self):
        self.results = self.getParam("results") #Get number of results
        self.keywords = self.getParam("keywords")

    def usernextTuple(self):
        url = "https://archive.org/advancedsearch.php?q="+self.keywords+"&fl%5B%5D=" \
        "avg_rating&fl%5B%5D=call_number&fl%5B%5D=collection&fl%5B%5D=" \
        "contributor&fl%5B%5D=coverage&fl%5B%5D=creator&fl%5B%5D=date&fl%5B%5D=" \
        "description&fl%5B%5D=downloads&fl%5B%5D=external-identifier&fl%5B%5D=" \
        "foldoutcount&fl%5B%5D=format&fl%5B%5D=headerImage&fl%5B%5D=identifier&" \
        "fl%5B%5D=imagecount&fl%5B%5D=language&fl%5B%5D=licenseurl&fl%5B%5D=" \
        "mediatype&fl%5B%5D=members&fl%5B%5D=month&fl%5B%5D=num_reviews&fl%5B%5D=" \
        "oai_updatedate&fl%5B%5D=publicdate&fl%5B%5D=publisher&fl%5B%5D=" \
        "related-external-id&fl%5B%5D=reviewdate&fl%5B%5D=rights&fl%5B%5D=" \
        "scanningcentre&fl%5B%5D=source&fl%5B%5D=subject&fl%5B%5D=title&fl%5B%5D=" \
        "type&fl%5B%5D=volume&fl%5B%5D=week&fl%5B%5D=year&sort%5B%5D=&sort%5B%5D=" \
        "&sort%5B%5D=&rows="+self.results+"&output=json"


        req = urllib2.Request(url) #Creating request
        response = urllib2.urlopen(req) #Opening URL
        web_data = response.read() #Reading response
        jsonData = json.loads(web_data)

        self.addField("result", jsonData["response"]["docs"])
        self.emit()


    def userclose(self):
        pass


TestPySpout().run()
