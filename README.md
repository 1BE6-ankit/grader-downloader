# grader-downloader
Download all lecture notes and assignments from a grader course site.

### Setup and Running
Run the following commands from grader-downloader root directory:
```bash
docker build -t grader-downloader .
docker run --rm --mount type=bind,src=$(pwd),target=/home/grader/downloader -w /home/grader/downloader/src -it grader-downloader /bin/bash
```

After the shell is prompted:
```bash
python3 index.py <grader url>
```

example:
```bash
python3 index.py https://grader.eecs.jacobs-university.de/courses/320143/2019_1r2/
```

The files will be download under downloads/course*/

---


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)