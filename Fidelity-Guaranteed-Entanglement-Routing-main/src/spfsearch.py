from vtopology import *
from pathf import *
import sys,heapq

class Spfsearch:
	def __init__(self):
		self._passed=[]
		self._nopass=[]
		self._prev=[]  #记录从源点V0到终点Vi的当前最短路径上终点Vi的直接前驱顶点序号，若V0到Vi之间有边前驱为V0否则为-1 
		self._cost=[]  #记录源点到终点之间最短路径的保真度，存在记V0到Vi的边的保真度，否则记0
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
				self._cost.append(Pathf()._pathf(g,[source,i]))
			elif i==source:
				self._cost.append(sys.maxsize/2)
			else:
				self._cost.append(0)
			
			if g[source][i]._isconnected is True and i!=source:
				self._prev.append(source)
			else:
				self._prev.append(-1)

		
		while len(self._nopass):
			idx=self._nopass[0]
			#选择最佳路径
			for i in self._nopass:
				if self._cost[i]>self._cost[idx]:
					idx=i
			self._nopass.remove(idx)
			self._passed.append(idx)

			#更新代价信息
			for i in self._nopass:
				t=Pathf()._pathf(g,self.getpath(idx)+[i])
				if t>self._cost[i] and self.getpath(idx)[0]==source:
					self._cost[i]=t
					self._prev[i]=idx
		
		#总体路径确定
		path=self.getpath(des)
		if path[0]==source and len(path)>=2:
			return path
		else:
			return []
		
	def heapdijkstra(self,g,source,des):
		self._passed=[]
		self._nopass=[]
		self._prev=[]  #记录从源点V0到终点Vi的当前最短路径上终点Vi的直接前驱顶点序号，若V0到Vi之间有边前驱为V0否则为-1 
		self._cost=[]  #记录源点到终点之间最短路径的保真度，存在记V0到Vi的边的保真度，否则记0
		self._path=[]  #源点到目的点的路径
		#初始化起点
		self._passed.append(source)
		self.g=g
		self._visited=[0]*len(g)
		#初始化前驱列表以及代价
		for i in range(len(g)):
			if i==source:
				self._cost.append(1)
			else:
				self._cost.append(0)
			self._prev.append(-1)
		heap=[]
		for i in self.g[source]:
			self._prev[i[0]]=source
			self._cost[i[0]]=i[1]
			heapq.heappush(heap,(1-i[1],i[0]))  #要将高保真度的优先级提高，将key值转化为1-f
		while heap!=[]:
			#弹出最大保真度边
			tmpe=heapq.heappop(heap)
			tmp=list(tmpe)
			tmp[0]=1-tmp[0] #重新转化为保真度f
			tmpe=tuple(tmp)
			if self._visited[tmpe[1]]==1:#如果该点已到过，就进行下一次循环
				continue
			self._visited[tmpe[1]]=1
			for i in self.g[tmpe[1]]:
				if self._cost[tmpe[1]]*i[1]>self._cost[i[0]]:
					self._cost[i[0]]=self._cost[tmpe[1]]*i[1]
					self._prev[i[0]]=tmpe[1]
					heapq.heappush(heap,(1-self._cost[i[0]],i[0]))
		#总体路径确定
		path=self.getpath(des)
		if path[0]==source and len(path)>=2:
			return path
		else:
			return []
	def kmaxf(self,g,source,des,maxk):#查找k个最大保真度路径
		self.aset=[]
		self.bset=[]
		
		li=self.heapdijkstra(copy.deepcopy(g),source,des)
		if len(li):
			self.aset.append(li)
		else:
			return self.bset
		for k in range(1,maxk):
			for i in range(len(self.aset[-1])-1):
				tmpg=copy.deepcopy(g)
				curnode=self.aset[-1][i]
				curroot=self.aset[-1][i+1]
				pathahead=self.aset[-1][0:i]
				#将当前边保真度设为0
				for i in tmpg[curnode]:
					if i[0]==curroot:
						i[1]=0

				path=self.heapdijkstra(tmpg,curnode,des)
				if len(path):
					sumpath=pathahead+path
					if sumpath  not in self.bset and sumpath not in self.aset and Pathf().noring(sumpath):#无环路
						self.bset.append(sumpath)

			if len(self.bset):
				#找出bset中保真度最大的
				f=0
				maxf=0
				for i in range(len(self.bset)):
					if Pathf().pathfljb(g,self.bset[i])>maxf:
						maxf=Pathf().pathfljb(g,self.bset[i])
						f=i
				#将最大保真度的路径加入aset,并移出bset
				if self.bset[f]  not in self.aset:
					self.aset.append(self.bset[f])
				
				self.bset.remove(self.bset[f])
			else:
				break
		return self.aset

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
