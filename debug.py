from datetime import datetime


class debug:
    def __init__(self,script,file=None):
        ### Constructor of the debug class. file will be optional. If defined, debug will be writen to a file
        ### In case it is not defined, it will be just printed
        self.script=script
        self.file=file

    def msg(self,action,objecttype,object,*details):
        ### message to file or printed
        detalles=""
        for ar in details:
            detalles=detalles+"["+ar+"]"
        if detalles=='':
            detalles='[NA]'
        print("["+str(datetime.now())+"]"+
            "[" + self.script + "]"+
            "[" + action + "]" +
            "[" + objecttype + "]" +
            "[" + object + "]" +
            detalles)