import urllib.request
from urllib.parse import urlparse
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

        # self.html_content = response.read().decode("utf-8");

        print(self.html_content)

class GraderSite(Site):
    def __init__(self, url):
        Site.__init__(self, url)

    def get_all_resources(self):
        Site.get_html_content(self)
        self.get_lecture_notes()

    def get_lecture_notes(self):
        # define regex for lecture notes
        lectur_re = "<tr><td class=\"menutext\">Course Materials:</td>(.*?)</tr>"

        # capture
        lecture_links = re.search(lectur_re, self.html_content).group(1)

    def get_assignments():
        # TODO: add logic
        print()