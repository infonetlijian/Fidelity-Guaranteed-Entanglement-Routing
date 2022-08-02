from queue import PriorityQueue
from network import *
from spfmincost import *
from pathf import *
from updatetopo import *
from throughput import *
from pud import  *
import sys
import copy,time
#基于最短路径的单sd路由算法
class Hspf:
    def __init__(self):
        self.path=[] #储存找到的路径
        self.fi=[] #储存该路径的期望保真度
        self.d=[] #储存纠缠次数
        self.con=[]#储存纠缠消耗数
        self.th=[]#各路径期望吞吐量
        self.sumt=0 #总吞吐量

    def hspf(self,network,source,des,fth,request):
        self.source=source
        self.des=des
        self.fth=fth
        self.request=request
        g=network

        times=0
        #计算ftable
        Pud().calftable(g)
        #删边
        Udtp().udtp(g,self.fth)
        # SPF Searching
        while True:
            hopg=Udtp().topocost(g) #cost转为跳数
            #转为临接表
            ng=Udtp().topoljb(hopg)
            time_0=time.time()
            li=Spfmc().heapdijkstra(copy.deepcopy(ng),source,des)
            times+=time.time()-time_0
            if len(li)<=1:
                break
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
                Udtp().udtppath(g,li,Etp().calactcon(d_li,n),self.fth)
                
            """else:
                t_li=0
                self.fi.append(0)"""
            #更新路径容量
            #Udtp().udtppath(g,li,Etp().calactcon(d_li,n),self.fth)
            
        return self.path,self.d,self.fi,self.con,self.th,self.sumt,times
       

