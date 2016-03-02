# Note - this code must run in Python 2.x and you must download
# http://www.pythonlearn.com/code/BeautifulSoup.py
# Into the same folder as this program

from urllib.request import urlopen
from bs4 import BeautifulSoup

url = input('Enter - ')
if len(url) <1:
    url = "http://python-data.dr-chuck.net/known_by_Fikret.html"

pos = input("Position(default=3): ")
if len(pos) <1:
    pos = 2
else:
    pos = int(pos) - 1

iter = input("Iterations(default=3): ")
if len(iter) <1:
    iter = 3
else:
    iter = int(iter)

for i in range(0, iter+1):
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find_all("li")
    url = str(tags[pos].find("a")["href"])
    i += 1
    if i == iter:
        print(tags[pos].find("a").contents[0])
        break
