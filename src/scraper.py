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

class GraderSite(Site):
    def __init__(self, url):
        Site.__init__(self, url)

    def get_all_resources(self):
        Site.get_html_content(self)

        # extract links 
        lecture_identifier = [" Course Materials: ", "Schedule:"]
        lecture = self.res_scraper(lecture_identifier)

        assignment_identifier = [" Assignments: ", " Homework: "]
        assignments = self.res_scraper(assignment_identifier)

        download_path = "../downloads/"
        subdir_name = self.create_downloaddirs(download_path)
        download_path += subdir_name

        self.download_links(download_path+"lecture/", lecture)
        self.download_links(download_path+"assignments/", assignments)

        print("Files successfully downloaded at: downloads/" + subdir_name)

    def create_downloaddirs(self, download_path):
        if not os.path.isdir(download_path):
            os.mkdir(download_path)

        subdir_counter = 1
        subdir_name = ""
        while not subdir_name:
            if os.path.isdir(download_path+"course"+str(subdir_counter)):
                subdir_counter += 1
            else:
                subdir_name = "course"+str(subdir_counter)+"/"

        download_path += subdir_name
        os.mkdir(download_path)
        os.mkdir(download_path+"lecture/")
        os.mkdir(download_path+"assignments/")

        return subdir_name

    def download_links(self, download_path, links):
        for link in links:
            # There are two scenarios for a download link. 
            # 1) One condition is that the link may be an absolute directory from the grader url:
            #    /courses/320143/2019_1r2/.......
            # 2) OR it is a relative url from the course url:
            #    assignments/......
            # Considering these two scenarios, we check if the link is absolute or not
            download_url = self.url+link[0] if not link[0].startswith('/') \
                else self.url[0:self.url.index("/courses")]+link[0]
            
            content = urllib.request.urlopen(download_url)            
            data = content.read()
            with open(download_path+link[1], 'w+b') as f:
                f.write(data)

    def res_scraper(self, identifier_list):

        for identifier in identifier_list:
            content_res = []

            # Normally, each section is defined with a <tr><td class=menutext> ..... </td></tr>
            # So, we extract this section defined by an additional 'identifier' to extract specific link
            # section - assignment or lecture
            base_string = "<tr><td class=menutext>{}<\/td><td class=text>(.*?)<\/td><\/tr><tr><td class=menutext>".format(identifier)

            try:
                # Scrape html based on current identifer. If it is not possible to get the
                # content using this identifier then, continue the loop with another identifier
                content_html = re.search(base_string, self.html_content).group(1)
            except:
                continue

            # get all the links. We leave '<' in closing </a> because this anchor tag contains a link 
            # and a name, such as: <a href=SOME_LINK>LINK_TEXT</a>. 
            # If the '<' in </a> is included, 'findall' function cannot extract the LINK_TEXT
            content_lists = re.findall("<a (.*?)\/a>", content_html)

            for each_list in content_lists:
                # get the link and the link text. The link text is the file name after the file pointed
                # by this link is extracted
                content_links = re.findall("href=(.*?)>(.*?)<", each_list)
                content_res.append(content_links[0])

            return content_res
