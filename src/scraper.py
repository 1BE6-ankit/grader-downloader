from urllib.parse import urlparse

import urllib.request
import htmlmin
import re

class Site:
    def __init__(self, url):
        # first validate url
        # self.validate_url(url)
        self.url = url
    
    def validate_url(self, url):
        validated_url = urlparse(url)
        if not (validated_url.scheme) or not (validated_url.netloc):
            print("Invalid url")
            exit(1)

    def get_html_content(self):
        # create a request
        request = urllib.request.Request(self.url)
        try:
            response = urllib.request.urlopen(request) 
        except:
            print("Cannot open resource")
            exit(1)

        # get html content
        self.html_content = htmlmin.minify(response.read().decode("utf-8"), \
            remove_empty_space=True)

        # self.html_content = response.read().decode("utf-8")

class GraderSite(Site):
    def __init__(self, url):
        Site.__init__(self, url)

    def get_all_resources(self):
        Site.get_html_content(self)
        self.get_lecture_notes()

    def get_lecture_notes(self):
        # capture
        lecture_html = re.search("<tr><td class=menutext> Course Materials: </td>(.*?)</tr>", \
            self.html_content).group(1)
        
        lecture_lists = re.findall("<li>(.*?)</li>", lecture_html)

        # list to hold elements
        res_lecture = []

        for each_list in lecture_lists:
            lecture_links = re.findall("href=(.*?)>(.*?)<\/a>", each_list)
            res_lecture.append(lecture_links[0])

        self.res_lecture = res_lecture

    def get_assignments():
        # TODO: add logic
        print()