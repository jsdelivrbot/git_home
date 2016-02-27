from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os

html = urlopen("http://www.163.com")

bsObj = BeautifulSoup(html)

images = bsObj.find_all("img", {"data-src": re.compile(".*\.jpg")})

for image in images:
    os.system("wget %s" %image["data-src"])
