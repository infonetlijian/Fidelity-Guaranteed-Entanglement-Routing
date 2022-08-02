from vtopology import *
from costf	import *
import sys

class Espf:
	def __init__(self):
		self._passed=[]
		self._nopass=[]
		self._prev=[]  #记录从源点V0到终点Vi的当前最短路径上终点Vi的直接前驱顶点序号，若V0到Vi之间有边前驱为V0否则为-1 
		self._cost=[]  #记录源点到终点之间最短路径的代价，存在记V0到Vi的边的代价，否则记为MAX
		self._path=[]  #源点到目的点的路径
	
	def dijkstra(self,g,source,des):
		#初始化起点
		self._passed.append(source)
		self.g=g
		
		#初始化未经过的点
		for i in range(len(g)):
			if i!=source:
				self._nopass.append(i)
		#初始化前驱列表以及代价
		for i in range(len(g)):
			if g[source][i]._isconnected is True and i!=source:
				self._cost.append(Costf()._costF(g,[source,i]))
			elif i==source:
				self._cost.append(0)
			else:
				self._cost.append(sys.maxsize/2)
			
			if g[source][i]._isconnected is True and i!=source:
				self._prev.append(source)
			else:
				self._prev.append(-1)

		
		while len(self._nopass):
			idx=self._nopass[0]
			#选择最佳路径
			for i in self._nopass:
				if self._cost[i]<self._cost[idx]:
					idx=i
			self._nopass.remove(idx)
			self._passed.append(idx)

			#更新代价信息
			for i in self._nopass:
				if Costf()._costF(g,self.getpath(idx)+[i])<self._cost[i] and self.getpath(idx)[0]==source:
					self._cost[i]=Costf()._costF(g,self.getpath(idx)+[i])
					self._prev[i]=idx
		
		#总体路径确定
		return self.getpath(des)    #,self.getwide(self.getpath(des))
	
	def getpath(self,u):   #获取到当前点u的路径
		tmp=u
		li=[]
		while u!=-1:
			li.append(u)
			u=self._prev[u]

		li.reverse()
		return li

					 
	def getwide(self,path):
		w=50000
		for i in range(len(path)-1):
			if self.g[path[i]][path[i+1]]._c<w:
				w=self.g[path[i]][path[i+1]]._c
		return w
