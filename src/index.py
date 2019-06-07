import sys
import re

from scraper import GraderSite

grader_url = sys.argv[1] if len(sys.argv)==2 \
    else "https://grader.eecs.jacobs-university.de/courses/320201/2019_1/"

# temp fix
grader_url = "http://acalc.eu5.net"

grader = GraderSite(grader_url)
grader.getHtmlContent()

