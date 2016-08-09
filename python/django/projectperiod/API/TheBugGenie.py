# Create your views here.
# -*- coding: utf-8 -*- needed for regular expressions with äöü-characters

import requests, json, logging


logger = logging.getLogger(__name__)

class TheBugGenie(object):

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.connected = True

        r = requests.get(url + "/list/issues/json/?format=json&tbg3_username=" + username + "&tbg3_password=" + password)
        if r.status_code != 200:
            logger.error('Can not get the issues from ' + self.url + ' with the username ' + self.username)
            self.connected = False

    def getIssues(self):
        r = requests.get(self.url + "/list/issues/json/assigned/me/?format=json&tbg3_username=" + self.username + "&tbg3_password=" + self.password)
        data = json.loads(r.content)

        if not isinstance(data, list):
            data2 = data
            data = []
            data.append(data2)

        #print(data[0]['issues'][u'13'])
        return data

    def getIssue(self, id):
        r = requests.get(self.url + "/issues/" + str(id) + "?format=json&tbg3_username=" + self.username + "&tbg3_password=" + self.password)
        data = []
        data.append(json.loads(r.content))
        #print(data)

        return data