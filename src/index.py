import sys
import re
import urllib.request
from urllib.parse import urlparse

from scraper import GraderSite

grader_url = sys.argv[1] if len(sys.argv)==2 \
    else "https://grader.eecs.jacobs-university.de/courses/320201/2019_1/"

validated_url = urlparse(grader_url)
if not (validated_url.scheme and validated_url.netloc):
    print("Invalid url")
    exit(1)

print("For url: ", grader_url)

# temp fix
grader_url = "http://acalc.eu5.net"

# create a request
request = urllib.request.Request(grader_url)
try:
    response = urllib.request.urlopen(request) 
except:
    print("Cannot opne resource")
    exit(1)

# get html content
html_content = response.read().decode("utf8")
print(html_content)
