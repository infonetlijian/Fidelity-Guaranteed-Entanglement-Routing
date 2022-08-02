from queue import PriorityQueue
from network import *
from spfmincost import *
from pathf import *
from updatetopo import *
from throughput import *
from pud import  *
import sys
import copy,time
#searchchoice为1代表k最短，0代表暴力，puchoice0代表暴力3代表提纯增幅最大项。
class Qpath:
    def __init__(self):
        self.path=[] #储存找到的路径
        self.fi=[] #储存该路径的期望保真度
        self.d=[] #储存纠缠提纯次数
        self.con=[]#储存纠缠消耗数
        self.th=[]#各路径期望吞吐量
        self.sumt=0 #总吞吐量
        self.notfound=[]  #储存迭代的路径

    def alg1(self,network,source,des,fth,request,searchchoice=1,puchoice=1):#searchchoice为1代表k最短，0代表暴力，puchoice为1代表提纯最小项，0代表暴力。
        self.source=source
        self.des=des
        self.fth=fth
        self.request=request
        g=network
        a=[]
        b=[]
        count=0
        self.q=PriorityQueue()
        times=0
        times1=0
        #计算ftable
        Pud().calftable(g)
        #删边
        Udtp().udtp(g,self.fth)
        #cost转为跳数
        hopg=Udtp().topocost(g) 
        #转为临接表
        tng=Udtp().topoljb(hopg)
        #计算minhop
        minhop=len(Spfmc().heapdijkstra(copy.deepcopy(tng),source,des))-1
        
        #提前将cost小于minhop的路径遍历
        self.notfound=Spfmc().spfmc2(tng,source,des,minhop-1)
        for cost in range(minhop,sys.maxsize):#按cost搜索路径
            #print(cost)
            hopg=Udtp().topocost(g)
            ng=Udtp().topoljb(hopg)
            if len(Spfmc().heapdijkstra(copy.deepcopy(ng),source,des))==0:
                break
                        
            if cost<=len(g)-1:
                time_0=time.time()
                if searchchoice==0:
                    pathset,self.notfound=Spfmc().walk(copy.deepcopy(ng),self.notfound,source,des,cost)
                    pathset1,a,b=Spfmc().costsearch(tng,source,des,cost,a,b)
                else:
                    pathset,a,b=Spfmc().costsearch(copy.deepcopy(ng),source,des,cost,a,b)
                #pathset,a,b=Spfmc().costsearch(ng,source,des,cost,a,b)
                time_1=time.time()
                times+=time_1-time_0
                #计算路径提纯选项并加入优先队列
                for path in pathset:
                    if Udtp().ispathconnect(g,path):
                        if puchoice==0:
                            scost,tmpde=Pathf()._bfpathmincost(g,path,self.fth)
                        else:
                            scost,tmpde=Pathf()._mostup(g,path,self.fth)
                        if tmpde!=[]:
                            self.q.put((scost,[path,tmpde]))
                        #if scost==-1:
                            #return -1,self.d,self.fi,self.con,self.th,self.sumt,times
                        
                times1+=time.time()-time_1
            #吞吐量更新
            if cost>len(g) and self.q.empty():
                break
            if not self.q.empty():
                #print('吞吐量更新')
                while True and not self.q.empty():
                    cur=self.q.get()
                    if cur[0]<=cost+1:
                    #判断路径上是否有足够资源
                    #n=1
                    #print(cur)
                        if Udtp().preudtppath(g,cur[1][0],cur[1][1]):
                            self.path.append(cur[1][0])
                            #print(self.path)
                            self.d.append(cur[1][1])
                            #计算期望吞吐量
                            #计算在该路径上消耗单份提纯资源的期望吞吐量
                            t_li=Etp().caletp(g,cur[1][0],cur[1][1])
                            #计算路径理论保真度
                            self.fi.append(Pathf()._epathf(g,cur[1][0],cur[1][1]))
                            #计算该路径上所有资源的期望吞吐量
                            n=Etp().calpathsumth(g,cur[1][0],cur[1][1])
                            patht_li=n*t_li
                            if self.sumt+patht_li>=self.request: #该路径资源足以满足请求
                                for i in range(1,n+1):
                                    if self.sumt+i*t_li>=self.request:
                                        self.th.append(i*t_li)
                                        self.sumt=self.sumt+i*t_li
                                        self.con.append(Etp().calactcon(cur[1][1],i))
                                        break
                                return self.path,self.d,self.fi,self.con,self.th,self.sumt,times
                            else:  #该路径总资源不满足需求，删去该路径重新查找
                                self.th.append(patht_li)
                                self.sumt=self.sumt+patht_li
                                self.con.append(Etp().calactcon(cur[1][1],n))
                            Udtp().udtppath(g,cur[1][0],Etp().calactcon(cur[1][1],n),self.fth)
                    else:
                        self.q.put(cur)
                        break
       
        return self.path,self.d,self.fi,self.con,self.th,self.sumt,times
       

