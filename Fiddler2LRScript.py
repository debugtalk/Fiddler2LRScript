# -*- coding: utf-8 -*-

from SAZ_Process import SAZ_Process

class SAZ2LRScript(object):
    def __init__(self, sazFile):
        self.sazProcess = SAZ_Process()
        self.requestList = self.sazProcess.GetRequestList(sazFile)
        self.requestDictList = self.sazProcess.ParseRequestList(self.requestList)

    def Convert_To_Custom_Function(self, requestMethod, requestDict):
        s = 'web_custom_request("' + str(requestMethod) +'_request' + '",' + '\n\t'
        s += '"URL=' + requestDict['requestURL'] + '",' + '\n\t'
        s += '"Method=' + requestDict['requestMethod'] + '",' + '\n\t'
        s += '"Resource=' + '0' + '",' + '\n\t'
        if requestDict.get('Content-Type'):
            s += '"EncType=' + requestDict['Content-Type'] + '",' + '\n\t'
        if requestDict.get('Content-Encoding'):
            s += '"EncType=' + requestDict['Content-Encoding'] + '",' + '\n\t'
        if requestDict.get('PostContent'):
            s += '"Body=' + requestDict['PostContent'] + '",' + '\n\t'
        s += 'LAST);\n\n'
        return s

    ''' 生成LoadRunner脚本'''
    def GenerateLRScript(self):
        sript = ''
        for i in range(len(self.requestDictList)):
            requestDict = self.requestDictList[i]
            requestMethod = requestDict['requestMethod']
            #将第i个requestDict转换成为web_custom_request函数
            sript += self.Convert_To_Custom_Function(requestMethod, requestDict) 
        return sript


if __name__ == '__main__':
    sazFile = r"Input_SAZ_Files\test.saz"
    LRScriptFile = r"Output_C_Files\Action.c"
    f = open(LRScriptFile, 'w')
    saz_converter = SAZ2LRScript(sazFile)
    sript = saz_converter.GenerateLRScript()
    f.write(sript)
    f.close()