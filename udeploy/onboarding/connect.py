import json
import requests
import base64
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable insecure SSL Warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class udeploy(object):

    def __init__(self, url, user, token):
        self.url=url
        self.user=user
        self.token=token

    def uget(self, uri):
        furl = self.url + uri
        res=requests.get(furl, auth=(self.user, self.token), verify=False)
        if res.status_code != 200:
            print ("Error, Status code not 200")
        else:
            return res

    def upost(self, uri, pl, hd):
        payload = pl
        payld = json.dumps(payload)
        furl = self.url + uri
        res=requests.post(furl,auth=(self.user,self.token),headers=hd,data=payld,verify=False)
        if res.status_code != 200:
            print ("Error, Status code not 200")
            print (res.status_code)
            print (res.text)
        else:
            return res

    def uput(self, uri, pl, hd):
        payload = pl
        payld = json.dumps(payload)
        furl = self.url + uri
        res=requests.put(furl,auth=(self.user,self.token),headers=hd,data=payld,verify=False)
        return res

    def uput_nopl(self, uri, hd):
        furl = self.url + uri
        res=requests.put(furl,auth=(self.user,self.token),headers=hd,verify=False)
        return res
