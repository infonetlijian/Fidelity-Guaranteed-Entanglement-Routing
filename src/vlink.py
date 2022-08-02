from throughput import *
class Link:  #定义边结构
    def __init__(self,fr=None,to=None,c=0,f=0,p=0,isconnected=False):
        self.fr=fr
        self.to=to
        self._p=p   #纠缠交换成功率
        self._c=c   #链路容量：暂指纠缠的数量
        self._f=f   #纠缠的保真度
        self._isconnected=isconnected
        self.ftable=[]
       
    def dellink(self):#删除该边
        self._p=0   
        self._c=0   
        self._f=0   
        self._isconnected=False
        self.ftable=[]
        
    
    def calftable1(self): #以2**n为提纯代价
        self.ftable=[]
        tmpc=self._c
        tmpf=self._f
        if tmpc==0:
            return
        self.ftable.append([tmpf,tmpc,1])
        i=1
        while tmpc>1:

            tmpc=tmpc//2
            tmpf=Etp().calfg(tmpf)
            i=i+1
            self.ftable.append([tmpf,tmpc,i])
    def calftable(self): #以n为提纯代价
        self.ftable=[]
        tmpc=self._c
        tmpf=self._f
        if tmpc==0:
            return
        i=1
        self.ftable.append([tmpf,tmpc,1])
        while tmpc>1:
            tmpc=tmpc-1
            tmpf=Etp().calfgn(tmpf,self._f)
            i=i+1
            self.ftable.append([tmpf,tmpc,i])
      
