import urllib.request
from urllib.parse import urlparse

class Site:
    url = html_content = None
    
    def __init__(self, url):
        # first validate url
        validated_url = urlparse(url)
        if not (validated_url.scheme and validated_url.netloc):
            print("Invalid url")
            exit(1)

        self.url = url

    def getHtmlContent(self):
        # create a request
        request = urllib.request.Request(self.url)
        try:
            response = urllib.request.urlopen(request) 
        except:
            print("Cannot opne resource")
            exit(1)

        # get html content
        html_content = response.read().decode("utf8")
        print(html_content)

class GraderSite(Site):
    def __init__(self, url):
        Site.__init__(self, url)
