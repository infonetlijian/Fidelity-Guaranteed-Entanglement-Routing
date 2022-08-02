from spfsearch import *
from vtopology import *
from pathf import *
from throughput import *
from pud import  *
from updatetopo import *
from network import *
from patharrange import *
import sys,time

class Qleap:
    def __init__(self):
        self.path=[] #储存找到的路径
        self.fi=[] #储存该路径的期望保真度
        self.d=[] #储存纠缠次数
        self.con=[]#储存纠缠消耗数
        self.th=[]#各路径期望吞吐量
        self.sumt=0 #总吞吐量

    def alg2(self,network,source,des,fth,request):
        self.source=source
        self.des=des
        self.fth=fth
        self.request=request
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
            li=Spfsearch().heapdijkstra(ng,self.source,self.des)
            times+=time.time()-time_0
            if len(li)<=1:  #判断是否找到一条路
                break
            #self.path.append(li)
            #计算fave
            fave=Pud().calfthave(self.fth,len(li)-1)
            #提纯决定
            if Pathf()._pathf(g,li)<self.fth:
                d_li=Pud().calpud(g,li,fave)
                #self.d.append(d_li)  #提纯决定
            else:
                d_li=[0]*(len(li)-1)
                #self.d.append(d_li)  #不需要提纯
            #判断路径上是否有足够资源
            #n=1
            if Udtp().preudtppath(g,li,d_li):
                self.d.append(d_li)
                self.path.append(li)
                #计算在该路径上消耗单份提纯资源的期望吞吐量
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
                Udtp().udtppath(g,li,Etp().calactcon(d_li,n),self.fth)
                
            """else:
                t_li=0
                self.fi.append(0)"""
            #更新路径容量
            #Udtp().udtppath(g,li,Etp().calactcon(d_li,n),self.fth)

        #actualpath,pathfi,pathd,pathth,countnz=Patharr().patharr(self.path,self.fi,self.d,self.th)
        return self.path,self.d,self.fi,self.con,self.th,self.sumt,times
        """print('path=',self.path)
        print('through=',self.sumt)
        print('expect fi=',self.fi)
        print('pur decision=',self.d)"""


