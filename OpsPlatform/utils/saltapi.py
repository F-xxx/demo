# -*- coding:utf-8 -*-

import json
import ssl
from urllib import request, parse

class SaltApi(object):
    __token_id = ''
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    def __init__(self, url, username, password):
        self.__url = url.rstrip('/')
        self.__user = username
        self.__password = password

    def token_id(self):
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        post_data_encode = parse.urlencode(params)  
        post_data_encode = post_data_encode.encode(encoding='utf-8')  
        content = self.postRequest(post_data_encode, prefix='/login')
        try:
            self.__token_id = content['return'][0]['token']
        except KeyError:
            raise KeyError
        #print(self.__token_id)

    def postRequest(self, obj, prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token': self.__token_id}
        req = request.Request(url, obj, headers=headers)
        response = request.urlopen(req)
        content = json.loads(response.read().decode('utf-8'))
        return content

    def list_all_key(self):
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        post_data_encode = parse.urlencode(params)  
        post_data_encode = post_data_encode.encode(encoding='utf-8')  
        self.token_id()
        content = self.postRequest(post_data_encode)
        minions = content['return'][0]['data']['return']['minions']
        print(minions)
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        return minions, minions_pre



def main():
    #sapi = SaltApi(url='',username='',password='')
  

if __name__ == '__main__':
    main()









