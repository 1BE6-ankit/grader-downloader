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
        lecture = self.res_scraper(" Course Materials: ")

        # The parameter "Schedule:" should have no spaces
        # lecture = self.res_scraper("Schedule:")

        assignments = self.res_scraper(" Assignments: ")
        # assignments = self.res_scraper(" Homework: ")


        download_path = "../resources/"

        if not os.path.isdir(download_path):
            os.mkdir(download_path)
            os.mkdir(download_path+""+"lecture/")
            os.mkdir(download_path+""+"assignments/")

        self.download_links(download_path+"lecture/", lecture)
        self.download_links(download_path+"assignments/", assignments)

    def download_links(self, download_path, links):
        for link in links:
            # There are two scenarios for a download link. 
            # One condition is that the link may be an absolute directory from the grader url,
            # OR it is a relative url from the course url. 
            # Considering these two scenarios, we check if the link is absolute or not
            download_url = self.url+link[0] if not link[0].startswith('/') \
                else self.url[0:self.url.index("/courses")]+link[0]
            
            content = urllib.request.urlopen(download_url)            
            data = content.read()
            with open(download_path+link[1], 'w+b') as f:
                f.write(data)

    def res_scraper(self, indentifier):
        # Normally, each section is defined with a <tr><td class=menutext> ..... </td></tr>
        # So, we extract this section defined by an additional 'identifier' to extract specific link
        # section - assignment or lecture
        base_string = "<tr><td class=menutext>{}<\/td><td class=text>(.*?)<\/td><\/tr><tr><td class=menutext>".format(indentifier)
        content_html = re.search(base_string, self.html_content).group(1)

        # get all the links. We leave '<' in closing </a> because this anchor tag contains a link 
        # and a name such as: <a href=SOME_LINK>LINK_TEXT</a>. 
        # If the '<' in </a> is included, findall cannot extract the LINK_TEXT
        content_lists = re.findall("<a (.*?)\/a>", content_html)

        content_res = []
        for each_list in content_lists:
            # get the link and the link text. The link text is the file name after the file pointed
            # by this link is extracted
            content_links = re.findall("href=(.*?)>(.*?)<", each_list)
            content_res.append(content_links[0])

        return content_res
