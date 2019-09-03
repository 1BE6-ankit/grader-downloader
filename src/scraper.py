from urllib.parse import urlparse

import urllib.request
import htmlmin
import re
import requests
import os

class Site:
    def __init__(self, url):
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

        # extract links 
        # lecture = self.res_scraper("Course Materials")
        lecture = self.res_scraper("Schedule")
        assignments = self.res_scraper("Assignments")

        download_path = "../resources/"

        if not os.path.isdir(download_path):
            os.mkdir(download_path)
            os.mkdir(download_path+""+"lecture/")
            os.mkdir(download_path+""+"assignments/")

        self.download_links(download_path+"lecture/", lecture)
        self.download_links(download_path+"assignments/", assignments)

    def download_links(self, download_path, links):
        for link in links:
            content = urllib.request.urlopen(self.url+link[0])            
            data = content.read()
            with open(download_path+link[1], 'w+b') as f:
                f.write(data)

    def res_scraper(self, indentifier):
        # extract the table holding the links 
        base_string = "<tr><td class=menutext> {}: <\/td><td class=text>(.*?)</td></tr>".format(indentifier)
        content_html = re.search(base_string, self.html_content).group(1)

        print(content_html)

        # extracts the link content between <li> </li>
        content_lists = re.findall("<li>(.*?)</li>", content_html)

        content_res = []
        for each_list in content_lists:
            content_links = re.findall("href=(.*?)>(.*?)<\/a>", each_list)
            content_res.append(content_links[0])

        return content_res
