# -*- coding: utf-8 -*-

import re
from zipfile import ZipFile

class SAZ_Process(object):
    metadata_regexp = re.compile("raw/(?P<id>[0-9]+)_c\.txt")
    request_pattern = "raw/{}_c.txt"

    def __init__(self):
        pass

    ''' 将saz文件中的每个request转换为一个list，最终将所有request以二维list的形式返回 '''
    def GetRequestList(self, saz_name):
        RequestList = []
        with ZipFile(saz_name, 'r') as saz_file:
            for saz_element in saz_file.namelist():
                self.metadata_match = self.metadata_regexp.match(saz_element)
                if self.metadata_match is not None:
                    id = self.metadata_match.group("id")
                    request_name = self.request_pattern.format(id)
                    request_file = saz_file.open(request_name)
                    request_raw = request_file.readlines()
                    request_content = []
                    for i in range(len(request_raw)): # 去除每行末尾的'\r\n'
                        request_content.append(re.sub(r'\r\n', '', request_raw[i]))
                    RequestList.append(request_content)
        return RequestList

    ''' 解析单个request list，以dict的形式返回 '''
    def ParseRequest(self, request):
        requestDict = {}
        # request[0] = 'GET http://52test.org HTTP/1.1'
        [requestDict['requestMethod'], requestDict['requestURL'], requestDict['httpVersion']] = request[0].split(" ")
        elementNum = len(request)
        for i in range(elementNum):
            reqItem = request[i].split(": ")
            if len(reqItem) == 2:   #reqItem的格式为“XX: YY”，排除第一行和空行
                requestDict[reqItem[0]] = reqItem[1]    #reqItem=[XX,YY]
            if len(reqItem) is 1 and request[-1] is not '':   #适用于POST类请求
                requestDict['PostContent'] = reqItem[0]
        return requestDict

    ''' 将RequestList中的每个request转换为dict，最终将所有request以二维dict的形式返回'''
    def ParseRequestList(self, requestList):
        requestDictList = []
        for i in range(len(requestList)):
            requestDictList.append(self.ParseRequest(requestList[i]))
        return requestDictList

if __name__ == '__main__':
    sazProcess = SAZ_Process()
    sazFile = r"SAZ_Files\test.saz"
    requestList = sazProcess.GetRequestList(sazFile)
    print requestList
    request = requestList[0]
    print request
    requestDict = sazProcess.ParseRequest(request)
    print requestDict
    requestDictList = sazProcess.ParseRequestList(requestList)
    print requestDictList
