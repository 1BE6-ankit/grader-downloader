import sys
import re

from scraper import GraderSite

grader_url = sys.argv[1] if len(sys.argv)==2 \
    else "https://grader.eecs.jacobs-university.de/courses/320201/2019_1/"

# c
    # else "https://grader.eecs.jacobs-university.de/courses/320112/2019_1gA/"

# c++
    #else "https://grader.eecs.jacobs-university.de/courses/320143/2019_1r2/"

# ads
    #else "https://grader.eecs.jacobs-university.de/courses/320201/2019_1/"

grader = GraderSite(grader_url)
grader.get_all_resources()
