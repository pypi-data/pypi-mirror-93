import pytest
import requests
import jsonpath
import json
import os
import sys
from auto_generation_pytest.get_case import CaseData
from py.io import TerminalWriter
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv(), override=True)

class MyPlugin(object):

    def __init__(self):
        self.f_mat = {}
        self.flag = {
            'matreport':False,
            'matdata':None,
            'matreplay':None
        }

    def pytest_addoption(self,parser):
        parser.addoption(
            "--matreport",
            action="store_true", 
            default=False,
            help="show test info"
        )
        parser.addoption(
            "--matdata",
            action="store", 
            default=None,
            help="load test case"
        )
        parser.addoption(
            "--matreplay",
            action="store", 
            default=None,
            help="load test case"
        )

    def pytest_configure(self,config):
        self.config = config
        self.flag['matreport'] = config.getoption("matreport")
        self.flag['matdata'] = config.getoption("matdata")
        self.flag['matreplay'] = config.getoption("matreplay")

    def pytest_generate_tests(self,metafunc):
        if self.flag['matdata'] is not None:
            argnames = metafunc.definition._fixtureinfo.argnames
            testdata_file_path = self.flag['matdata']
            if self.flag['matreplay']:
                name_list = metafunc.function.__name__.split('_')
                test_method_name = name_list[1]+'*'+name_list[2]+'_'+name_list[-1]
                testcases = CaseData('').get_data(testdata_file_path,test_method_name)
            else:
                test_method_name = metafunc.cls.__name__[4:] + '_' + metafunc.function.__name__.split('_')[-1]
                testcases = CaseData('').get_data(testdata_file_path,test_method_name)
            if 'params' in argnames:
                metafunc.parametrize('params', testcases)

    def report_write(self,w,title,info,color):
        w.write(' ---  '+title, **{color: True})
        w.write('\t' + str(info) + '\n')
        w.line()
    
    def pytest_runtest_logreport(self,report):
        pass
        # if self.flag['matreport']:
        #     w = TerminalWriter()
        #     item = self.f_mat[report.nodeid]
        #     if report.when == "call" and report.outcome != 'passed':
        #         nodeid = item.nodeid

        #         _num = item.name.replace(item.originalname,'').replace('params','').strip('[').strip(']')

        #         try:
        #             case = item.module.report[item.originalname][int(_num)]
        #         except IndexError:
        #             case = item.module.report[item.originalname]

        #         if not case:
        #             raise ValueError('调试信息保存失败')

        #         used_fixtures = sorted(getattr(item, "fixturenames", []))
                
        #         f = {}
        #         if used_fixtures:
        #             for i in used_fixtures:
        #                 f[i] = item.funcargs[i]
        #         w.line()
        #         w.line()
        #         color = 'red'
        #         w.sep('_',item.nodeid,**{color: True})
        #         w.line()

        #         self.report_write(w,'运行用例：',str(item.function.__doc__),'white')
        #         self.report_write(w,'fixtrue数据为：',str(f),'green')
        #         self.report_write(w,'接口请求数据为：',str(case['request']),'yellow')
        #         self.report_write(w,'接口返回数据为：',str(case['respone']),'blue')
        #         if 'assert' in report.longreprtext:
        #             if self.config.getoption("tbstyle") == 'no':
        #                 index = report.longreprtext.index('E')
        #             else:
        #                 index = report.longreprtext.index('assert')
                    
        #             self.report_write(w,'断言结果为：\n',str(report.longreprtext[index:]),'red')

    def pytest_runtest_makereport(self,item, call):
        if self.flag['matreport']:
            self.f_mat = {
                item.nodeid:item
            }
    
    
