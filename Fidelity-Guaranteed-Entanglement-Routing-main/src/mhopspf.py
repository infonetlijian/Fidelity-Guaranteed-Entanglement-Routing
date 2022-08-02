from hopspf import *
from network import *
from patharrange import *
from pathfd import *
from queue import PriorityQueue
import sys
import copy

#基于最短路径的多SD Pair搜索算法
class Mhopspf:
    def __init__(self):
        
        self.path=[] #储存各sd对找到的路径
        self.fi=[] #储存各路径的期望保真度
        self.d=[] #储存路径纠缠提纯次数
        self.th=[]#各路径期望吞吐量
        self.sdth=[] #各sd对的吞吐量
        self.con=[]#储存纠缠消耗数
        self.sumt=0 #网络总吞吐量
        self.q=PriorityQueue()
    def alg5(self,network,sdset,fthset,reqset,alpha=0,beta=1):
        self.network=network
        """vnetwork=Vtopo().creatbasicvtopo(network)  #预处理拓扑，转换为合适的格式
        newnetwork=Vtopo().creatvtopo(vnetwork)"""
        #计算节点自由度
        freed=Vtopo().calg(network)
        dicsd={}
        #初始化路径集、提纯、吞吐量,建立字典，映射关系为sd对
        for i in range(len(sdset)):
            self.path.append([])
            self.fi.append([])
            self.d.append([])
            self.th.append([])
            self.con.append([])
            self.sdth.append(0)
            dicsd[tuple(sdset[i])]=i
        #建立字典，映射关系为sd对
        
        
        for i in range(len(sdset)):
            c=copy.deepcopy(network)
            pathset,dset,fiset,conset,thset,sumt,t=Hspf().hspf(c,sdset[i][0],sdset[i][1],fthset[i],reqset[i])
            pathfreed=[]#初始化路径自由度
            for path in pathset:
                pathfreed.append(Cpathfd().calpathfd(path,freed))
            #计算综合Utility
            uti=[]
            for j in range(len(pathfreed)):
                uti.append(Cpathfd().caluti(pathfreed[j],dset[j]))
            #放入优先队列
            for p in range(len(pathset)):
                self.q.put((uti[p],[[sdset[i][0],sdset[i][1],fthset[i],reqset[i]],pathset[p],conset[p],thset[p],dset[p],fiset[p]]))
        while not self.q.empty():
            cur=self.q.get()[1]
            #资源分配
            #判断当前路径资源是否充足
            if Udtp().preudtppathc(network,cur[1],cur[2]):
                #更新topo资源
                Udtp().udtppathc(network,cur[1],cur[2])
                self.path[dicsd[tuple([cur[0][0],cur[0][1]])]].append(cur[1])
                self.th[dicsd[tuple([cur[0][0],cur[0][1]])]].append(cur[3])
                self.d[dicsd[tuple([cur[0][0],cur[0][1]])]].append(cur[4])
                self.fi[dicsd[tuple([cur[0][0],cur[0][1]])]].append(cur[5])
                self.sdth[dicsd[tuple([cur[0][0],cur[0][1]])]]+=cur[3]
                self.con[dicsd[tuple([cur[0][0],cur[0][1]])]].append(cur[2])
                self.sumt+=cur[3]

            else:#查找新路
                gcopy2=copy.deepcopy(network)
                pathset,dset,fiset,conset,thset,sumt,t=Hspf().hspf(gcopy2,cur[0][0],cur[0][1],cur[0][2],cur[0][3]-self.sdth[dicsd[tuple([cur[0][0],cur[0][1]])]])
                pathfreed=[]#初始化路径自由度
                for i in pathset:
                    pathfreed.append(Cpathfd().calpathfd(i,freed))
                #计算综合Utility
                uti=[]
                for i in range(len(pathfreed)):
                    uti.append(Cpathfd().caluti(pathfreed[i],conset[i],alpha,beta))
                #放入优先队列
                for i in range(len(pathset)):
                    self.q.put((uti[i],[cur[0],pathset[i],conset[i],thset[i],dset[i],fiset[i]]))

        return self.path,self.th,self.fi,self.d,self.con,self.sumt