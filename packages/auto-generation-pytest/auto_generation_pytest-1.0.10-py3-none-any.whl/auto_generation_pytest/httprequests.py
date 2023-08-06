import os
import requests
import json
import importlib
import pytest
from dotenv import find_dotenv, load_dotenv

from auto_generation_pytest.utlis import get_extract,set_extract,replace_extract
load_dotenv(find_dotenv(), override=True)

report = {}

class HttpRequest(object):

    def __init__(self):
        self.session = requests.session()
        self.session.keep_alive = False
        self.header = {}
        self.timeout = 60
        self.url = os.environ.get('HOST')
        self.format = str(os.environ.get('HTTP_FROMAT'))

    def res_format(self, data):
        path = self.format.split('.')
        funciton = importlib.import_module('.'.join(path[:-1]))
        response = getattr(funciton, path[-1])(data)
        return response

    def get(self, api ,data):
        if data == {}:
            data = ''
        response = None
        try:
            response = self.session.get(api, params=data, headers=self.header, timeout=self.timeout)
            response.raise_for_status()
        except Exception as e:
            return ("HTTP请求异常，异常信息：%s " % str(e))
        if self.format == 'json':
            response = response.json()
        elif '.' in self.format:
            response = self.res_format(response)
        return response

    def post(self, api, data):
        response = None
        if data == {}:
            data = ''
        else:
            data = json.dumps(data)
        try:
            response = self.session.post(api, data=data, headers=self.header, timeout=self.timeout)
            response.raise_for_status()
        except Exception as e:
            return ("ERROR  HTTP请求异常，异常信息：%s " % str(e))
            #print("\tHTTP请求异常，异常信息：%s \n" % str(e))
        if self.format == 'json':
            try:
                response = response.json()  
            except Exception as e :
                return ("ERROR  返回结果格式化失败：%s " % str(response.text))
                #print("返回结果格式化失败：%s \n" % str(response.text))
        elif '.' in self.format:
            try:
                response = self.res_format(response)
            except Exception as e :
                return ("ERROR  返回结果格式化失败：%s " % str(response.text))
                #print("返回结果格式化失败：%s \n" % str(response.text))
        return response

    def send(self, api, method, data, header, url=None):
        if url:
            self.url = url
        self.header = header
        #data = replace_extract(data)
        method = str.lower(method)
        if not self.url:
            raise ValueError('未配置环境变量HOST')
        self.data = data
        r = getattr(self, method)(self.url + api, data)
        self.r = r
        return r

    def report(self):
        info = {
            'request':self.data,
            'respone':self.r
        }
        return info

