from spfsearch import *
from vtopology import *
from pathf import *
from throughput import *
from pud import  *
from updatetopo import *
from network import *
from patharrange import *
import sys,time

class Alg2k:
    def __init__(self):
        self.path=[] #储存找到的路径
        self.fi=[] #储存该路径的期望保真度
        self.d=[] #储存纠缠次数
        self.con=[]#储存纠缠消耗数
        self.th=[]#各路径期望吞吐量
        self.sumt=0 #总吞吐量

    def alg2k(self,network,source,des,fth,request,k=2):
        self.source=source
        self.des=des
        self.fth=fth
        self.request=request
        self.k=k
        times=0
        """#network=Net().network  #存入拓扑
        network=Vtopo().creatbasicvtopo(network)  #预处理拓扑，转换为合适的格式
        Pud().calftable(network[1]) #计算ftable
        newedge=Udtp().udtp(network[1],fth)  #删边
        g=Vtopo().creatvtopo([network[0],newedge])  载入最终拓扑"""
        g=network
        #计算ftable
        Pud().calftable(g)
        #删边
        Udtp().udtp(g,self.fth)
        # SPF Searching
        while True:
            #拓扑转换为邻接表
            ng=Udtp().topoljbf(g)
            time_0=time.time()
            liset=Spfsearch().kmaxf(ng,self.source,self.des,self.k)
            times+=time.time()-time_0
            if len(liset)==0:#判断是否有可选路径
                break
            
            #找出最小cost的路径
            mincost=sys.maxsize
            for i in liset:
                tmpfave=Pud().calfthave(self.fth,len(i)-1)#计算fave
                if Pathf()._pathf(g,i)<self.fth:
                    td_li=Pud().calpud(g,i,tmpfave)
                #self.d.append(d_li)  #提纯决定
                else:
                    td_li=[0]*(len(i)-1)  #不需要提纯
                if Pathf().ccost(td_li)<mincost:
                    mincost=Pathf().ccost(td_li)
                    d_li=td_li
                    li=i
                
            
            
            
            #判断路径上是否有足够资源
            n=1
            if Udtp().preudtppath(g,li,d_li):
                self.d.append(d_li)
                self.path.append(li)
                #计算在该路径上消耗单位提纯次数的期望吞吐量
                t_li=Etp().caletp(g,li,d_li)
                #计算路径理论保真度
                self.fi.append(Pathf()._epathf(g,li,d_li))
                #计算该路径上所有资源的期望吞吐量
                n=Etp().calpathsumth(g,li,d_li)
                patht_li=n*t_li
                if self.sumt+patht_li>=self.request: #该路径资源足以满足请求
                    for i in range(1,n+1):
                        if self.sumt+i*t_li>=self.request:
                            self.th.append(i*t_li)
                            self.sumt=self.sumt+i*t_li
                            self.con.append(Etp().calactcon(d_li,i))
                            break
                    break
                            
                   
                else:  #该路径总资源不满足需求，删去该路径重新查找
                    self.th.append(patht_li)
                    self.sumt=self.sumt+patht_li
                    self.con.append(Etp().calactcon(d_li,n))
                
                
            """else:
                t_li=0
                self.fi.append(0)"""
            #更新路径容量
            Udtp().udtppath(g,li,Etp().calactcon(d_li,n),self.fth)

        #actualpath,pathfi,pathd,pathth,countnz=Patharr().patharr(self.path,self.fi,self.d,self.th)
        return self.path,self.d,self.fi,self.con,self.th,self.sumt,times
        """print('path=',self.path)
        print('through=',self.sumt)
        print('expect fi=',self.fi)
        print('pur decision=',self.d)"""


