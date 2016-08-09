# Create your views here.
# -*- coding: utf-8 -*- needed for regular expressions with äöü-characters
from requests import Request, Session
from suds.client import Client

import json, logging, re
from suds.sax.element import Element


logger = logging.getLogger(__name__)

class Polarion(object):

    def __init__(self, url, username, password, query):
        self.url = url
        self.username = username
        self.password = password
        self.query = query #project.id:ProjectPeriod AND type:defect
        self.connected = True

        self.session = Client(self.url + '/ws/services/SessionWebService?wsdl') #http://10.0.0.1/polarion
        try:
            self.session.service.logIn(self.username, self.password)
            header_regex = re.compile('<ns1:sessionID.+>(.*)</ns1:sessionID')
            m=header_regex.search(self.session.last_received().str())
            sessionId=m.group(1)
            session_ns=('ns1', 'http://ws.polarion.com/session')
            self.sessionId = Element('sessionID', ns=session_ns).setText(sessionId)
        except:
            logger.error('Can not get the issues from ' + self.url + ' with the username ' + self.username)
            self.connected = False

    def getIssues(self):
        tracker = Client(self.url + '/ws/services/TrackerWebService?wsdl')
        tracker.set_options(soapheaders=self.sessionId)
        return tracker.service.queryWorkItems(self.query,'id',['id','title'])