###################################################
from datetime import datetime
log_file='/tmp/Tfarej.log'   
def delLog():#txt.center(100)
    import os
    Stoptime = datetime.now().strftime('%Y-%m-%d %H:%M')   
    if os.path.exists(log_file):
        f = open(log_file, 'w')
        f.write('SupTVoDNeW <--'+str(Stoptime).center(100)+'-->  SupTVoDNeW'+ '\n')
        f.close
        # os.remove(log_file)
    else:
        f = open(log_file, 'a')
        f.write('SupTVoDNeW <--'+str(Stoptime).center(100)+'-->  SupTVoDNeW'+ '\n')
        f.close
def printE(msg=''):
    import traceback,sys
    printD("===============================================")
    printD("                   EXCEPTION                   ")
    printD("===============================================")
    msg = msg + ': \n%s' % traceback.format_exc()
    traceback.print_exc(file=sys.stdout)
    printD("Error",msg)
    printD("===============================================")
def getcaller_name():
    try:
        import inspect
        import os
        frame = inspect.currentframe()
        frame = frame.f_back.f_back
        code = frame.f_code
        calling_module = os.path.basename(code.co_filename)
        return calling_module
    except:
        return ''
def printD(label='', Ddata='' ):
    Ddata=str(Ddata)
    label=str(label)
    import traceback
    try:
        Stoptime = datetime.now().strftime('%Y-%m-%d %H:%M')
        caller_name = getcaller_name() 
        f = open(log_file, 'a')
        f.write(str(Stoptime)+'-->'+caller_name+":"+label+'->'+Ddata + '\n')
        f.close
    except Exception:
        print("======================EXC printD======================")
        print("Log: %s" % traceback.format_exc())
        print("========================================================")
        try:
            msg = '%s' % traceback.format_exc()
            f = open(log_file, 'a')
            f.write(str(Stoptime)+'-->'+Ddata + '\n')
            f.close
        except Exception:
            print("======================EXC printD======================")
            print("logII: %s" % traceback.format_exc())
            print("========================================================")
########################################