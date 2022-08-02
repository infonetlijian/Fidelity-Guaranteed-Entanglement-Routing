from costext	import *
import sys
class Spfa:
    def __init__(self):
        self.q=[]
        self._prev=[]  #记录从源点V0到终点Vi的当前最短路径上终点Vi的直接前驱顶点序号，若V0到Vi之间有边前驱为V0否则为-1 
        self._cost=[]  #记录源点到终点之间最短路径的代价，存在记V0到Vi的边的代价，否则记为MAX
        self._path=[]  #源点到目的点的路径

    def spfa(self,g,source,des):
        #初始化队列
        self.q.append(source)
        #初始化前驱列表以及代价
        for i in range(len(g)):
            if i!=source:
                self._cost.append(sys.maxsize/2)
            else:
                self._cost.append(0)
            
            if g[source][i]._isconnected is True and i!=source:
                self._prev.append(source)
            else:
                self._prev.append(-1)
        while len(self.q):
            p=self.q.pop(0)
            for i in range(len(g)):
                if g[p][i]._isconnected is True and Cost()._costEXT(g,self.getpath(p)+[i])<self._cost[i]:
                    self._cost[i]=Cost()._costEXT(g,self.getpath(p)+[i])
                    self._prev[i]=p
                    if self.q.count(i)==0:
                        self.q.append(i)
        return self.getpath(des)

    def getpath(self,u):   #获取到当前点u的路径
        tmp=u
        li=[]
        while u!=-1:
            li.append(u)
            u=self._prev[u]

        li.reverse()
        return li