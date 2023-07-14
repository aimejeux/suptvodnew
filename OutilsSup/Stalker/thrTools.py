from twisted.web import client
from twisted.internet import reactor
import os, requests, urllib2, re, shutil
from threading import Thread
from logTools import printD,printE
class thrTools():
    def __init__(self):
        pass
    def stopDataThread(self):
        self.dataThread.stop()
    def startDataThread(self,callFunction=None,iParams={}, callBack = None):
        try:
            self.dataThread = threadObj(callFunction=callFunction, iParams=iParams, callBack = callBack)
            self.dataThread.start()
        except:
            printE()
    def stopDataThread(self):
        self.dataThread.stop()
    #####image
    def startImageThread(self,callFunction=None,iParams={}, callBack = None):
        try:
            self.imageThread = threadObj(callFunction=callFunction, iParams=iParams, callBack = callBack)
            self.imageThread.start()
        except:
            printE()
    def stopDataThread(self):
        self.imageThread.stop()
    def startFileThread(self,callFunction=None,iParams={}, callBack = None):
        try:
            self.fileThread = threadObj(callFunction=json_request, iParams=iParams, callBack = callBack)
            self.fileThread.start()
        except:
            printE()
    def stopFileThread(self):
        self.fileThread.stop()
class threadObj(Thread):#url,headers,params,method
    def __init__(self, callFunction=None, iParams={}, callBack = None,dataIndex=0):
        Thread.__init__(self)
        self.daemon = True
        self.callFunction = callFunction
        self.iParams = iParams
        self.callBack = callBack
        printD('thread-callBack',self.callBack)
        self.dataIndex=dataIndex
        self.threadExit = False
    def run(self):
        outData = ''
        ret=True
        msg=''
        try:
            ret,data=self.callFunction(self.iParams)
            printD('thread-run-ret',ret)
            printD('thread-run-data',data)
            if ret==False:
                msg=data
        except Exception as error:
            print "thread error",error
            printE()
            data=''
            msg="Data error-check log"
            ret=False
        if self.threadExit:
            data=''
            msg=""
            ret=False
        return reactor.callFromThread(self.callBack,ret,msg,data)
        printD('thread-callBackcallBackcallBackcallBackcallBackcallBackcallBackcallBack',str(reactor.getThreadGroup()))
    def stop(self):
        self.threadExit = True
import requests,json
def json_request(iParams={}):##iParams={}
    T = ''
    url= iParams.get("url","")
    headers= iParams.get("headers","")
    params= iParams.get("params","")
    method= iParams.get("method","")
    printD('thread-json_request-url-coucou',url)
    printD('thread-json_request-headers-coucou',headers)
    printD('thread-json_request-params-coucou',params)
    printD('thread-json_request-method-coucou',method)
    try:
        url = str(url)
        session = requests.Session()
        r = session.get(url, headers=headers,verify=False)
        if r.status_code == 200:
            printD('thread-json_request-r',r)
            return (True,r.json())
        return (False,"download error-check log")
    except:
        printE()
        return (False,"download error-check log")
def getData(params={},_format=''):
    url=params.get("url","")
    try:
        url = str(url)
        printD("url",url)
        import requests
        session = requests.Session()
        r = session.get(url, timeout=10, verify=False)
        if r.status_code == 200:
            if _format=='json':
                return (True,r.json())
            return (True,r.content)
        return (False,"download error-check log")
    except:
        printE()
        return (False,"download error-check log")
def getFile(iParams={}):
    source = iParams.get("url",'')
    dest = iParams.get("target",'')
    replace=iParams.get('replace',True)
    if source is None or source.strip() == '' or dest is None or dest.strip()== '' :
        return False,'invalid paramters'
    else:
        if  source.startswith('http'):
            try:
                import requests
                if os.path.exists(dest) and replace==False:
                    return dest
                session = requests.session()
                r = session.get(source, timeout=5, verify=False)
                printD("r.status_code",r.status_code)
                if r.status_code == 200:
                    with open(dest, 'wb') as f:
                        f.write(r.content)
                    f.close()
                    return True,dest
            except Exception as error:
                printE()
                return False,str(error)
        else:
            if source.startswith("/"):
               return True,dest
            else:
               return False,"invalid source"
getImage=getFile
json_request=json_request