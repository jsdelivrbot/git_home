# Note - this code must run in Python 2.x and you must download
# http://www.pythonlearn.com/code/BeautifulSoup.py
# Into the same folder as this program

from urllib.request import urlopen
from bs4 import BeautifulSoup # this is using python3.4

url = input('Enter - ') # raw_input is changed to input in python3
html = urlopen(url) # read() is not needed in python3

soup = BeautifulSoup(html)

sum = 0
num = 0
# Retrieve all of the anchor tags
tags = soup.find_all("span")
for tag in tags:
    # Look at the parts of a tag
    if len(tag) < 1: continue
    num = int(tag.contents[0])
    sum += num

print("The sum: %i.\n" % sum)
