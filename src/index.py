import sys
import re

from scraper import GraderSite

grader_url = sys.argv[1] if len(sys.argv)==2 \
    else "https://grader.eecs.jacobs-university.de/courses/320201/2019_1/"

grader = GraderSite(grader_url)
grader.get_all_resources()
