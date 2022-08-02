from vtopology import *
from pathf import *
from updatetopo import *
import sys
import copy

class Spfmc:
    
	def __init__(self):
		self._passed=[]
		self._nopass=[]
		self._prev=[]  #记录从源点V0到终点Vi的当前最短路径上终点Vi的直接前驱顶点序号，若V0到Vi之间有边前驱为V0否则为-1 
		self._cost=[]  #记录源点到终点之间最短路径的保真度，存在记V0到Vi的边的保真度，否则记0
		self._path=[]  #源点到目的点的路径
		self.paths=[]
		self.apath=[]
		self.aset=[]
		self.bset=[]
		self.flag=0 #标志能不能找出更多的路
		self.pathnum=0 #记录前一次找到的路径总数

	def spfmc(self,g,source,des,maxk=20): #搜索路径
		ng=Udtp().topocost(g)

		self.aset=[]
		self.bset=[]

		li=self.dijistra(copy.deepcopy(ng),source,des)
		if len(li):
			self.aset.append(li)
		else:
			return self.bset
		for k in range(1,maxk):
			for i in range(len(self.aset[-1])-1):
				tmpg=copy.deepcopy(ng)
				curnode=self.aset[-1][i]
				curroot=self.aset[-1][i+1]
				pathahead=self.aset[-1][0:i]
				#将当前边cost设为无穷大
				tmpg[self.aset[-1][i]][self.aset[-1][i+1]]=sys.maxsize/2
				tmpg[self.aset[-1][i+1]][self.aset[-1][i]]=sys.maxsize/2

				path=self.dijistra(tmpg,curnode,des)
				if len(path):
					sumpath=pathahead+path
					if sumpath  not in self.bset and sumpath not in self.aset and Pathf().noring(sumpath):#无环路
						self.bset.append(sumpath)
				

			if len(self.bset):
				#找出bset中cost最小的
				f=0
				mincost=5000
				for i in range(len(self.bset)):
					if Pathf()._pathcost(ng,self.bset[i])<mincost:
						mincost=Pathf()._pathcost(ng,self.bset[i])
						f=i
				#将最小cost值的路径加入aset,并移出bset
				if self.bset[f]  not in self.aset:
					self.aset.append(self.bset[f])
				
				self.bset.remove(self.bset[f])
			else:
				break
		return self.aset


		

		
	def dijistra(self,g,source,des):#最短路径
		self._passed=[]
		self._nopass=[]
		self._prev=[]  #记录从源点V0到终点Vi的当前最短路径上终点Vi的直接前驱顶点序号，若V0到Vi之间有边前驱为V0否则为-1 
		self._cost=[]  #记录源点到终点之间最短路径的保真度，存在记V0到Vi的边的保真度，否则记0
		self._path=[]  #源点到目的点的路径
		#初始化起点
		self._passed.append(source)
		self.g=g
		#初始化未经过的点
		for i in range(len(g)):
			if i!=source:
				self._nopass.append(i)
		#初始化前驱列表以及代价
		for i in range(len(g)):
			self._cost.append(g[source][i])
			
			if g[source][i]==1:
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
				t=Pathf()._pathcost(g,self.getpath(idx)+[i])
				if t<self._cost[i] and self.getpath(idx)[0]==source:
					self._cost[i]=t
					self._prev[i]=idx
		#总体路径确定
		path=self.getpath(des)
		if path[0]==source and len(path)>=2:
			return path
		else:
			return []


	def heapdijkstra(self,g,source,des):#最短路径堆优化
		self._passed=[]
		self._nopass=[]
		self._prev=[]  #记录从源点V0到终点Vi的当前最短路径上终点Vi的直接前驱顶点序号，若V0到Vi之间有边前驱为V0否则为-1 
		self._cost=[]  #记录源点到终点之间最短路径的保真度，存在记V0到Vi的边的保真度，否则记0
		self._path=[]  #源点到目的点的路径
		#初始化起点
		self._visited=[0]*len(g)
		self._passed.append(source)
		self.g=g
		#初始化前驱列表以及代价
		for i in range(len(g)):
			if i==source:
				self._cost.append(0)
			else:
				self._cost.append(sys.maxsize/2)
			self._prev.append(-1)
		heap=[]
		for i in self.g[source]:
			self._prev[i[0]]=source
			self._cost[i[0]]=i[1]
			heapq.heappush(heap,(i[1],i[0]))
		while heap!=[]:
			#弹出最小权值边
			tmpe=heapq.heappop(heap)
			if self._visited[tmpe[1]]==1:#如果该点已到过，就进行下一次循环
				continue
			self._visited[tmpe[1]]=1
			for i in self.g[tmpe[1]]:
				if self._cost[tmpe[1]]+i[1]<self._cost[i[0]]:
					self._cost[i[0]]=self._cost[tmpe[1]]+i[1]
					self._prev[i[0]]=tmpe[1]
					heapq.heappush(heap,(self._cost[i[0]],i[0]))

		#总体路径确定
		path=self.getpath(des)
		if path[0]==source and len(path)>=2:
			return path
		else:
			return []
	def kshortpath(self,g,source,des,maxk):#搜索k最短路径
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
				#将当前边距离设为最大
				for i in tmpg[curnode]:
					if i[0]==curroot:
						i[1]=sys.maxsize/2

				path=self.heapdijkstra(tmpg,curnode,des)
				if len(path):
					sumpath=pathahead+path
					if sumpath  not in self.bset and sumpath not in self.aset and Pathf().noring(sumpath):#无环路
						self.bset.append(sumpath)

			if len(self.bset):
				#找出bset中最短的
				f=0
				shortespath=sys.maxsize
				for i in range(len(self.bset)):
					if len(self.bset[i])<shortespath:
						shortespath=len(self.bset[i])
						f=i
				#将最大保真度的路径加入aset,并移出bset
				if self.bset[f]  not in self.aset:
					self.aset.append(self.bset[f])
				
				self.bset.remove(self.bset[f])
			else:
				break
		return self.aset
	def skshortpath(self,g,source,des,maxk): #保存上一次k的状态加速搜索
		
		t=maxk-len(self.aset)
		if t<=0:
			return
		"""li=self.heapdijkstra(copy.deepcopy(g),source,des)
		if len(li):
			if li not in self.aset:
				self.aset.append(li)
			
		else:
			return self.bset"""
		for k in range(0,t):
			for i in range(len(self.aset[-1])-1):
				tmpg=copy.deepcopy(g)
				curnode=self.aset[-1][i]
				curroot=self.aset[-1][i+1]
				pathahead=self.aset[-1][0:i]
				#将当前边删去
				for i in tmpg[curnode]:
					if i[0]==curroot:
						tmpg[curnode].remove(i)
						break
				for i in tmpg[curroot]:
					if i[0]==curnode:
						tmpg[curroot].remove(i)
						break
				path=self.heapdijkstra(tmpg,curnode,des)
				if len(path):
					sumpath=pathahead+path
					if sumpath  not in self.bset and sumpath not in self.aset and Pathf().noring(sumpath):#无环路
						self.bset.append(sumpath)

			if len(self.bset):
				#找出bset中最短的
				f=0
				shortespath=sys.maxsize
				for i in range(len(self.bset)):
					if len(self.bset[i])<shortespath:
						shortespath=len(self.bset[i])
						f=i
				#将最短的路径加入aset,并移出bset
				if self.bset[f]  not in self.aset:
					self.aset.append(self.bset[f])
				
				self.bset.remove(self.bset[f])
			else:
				break
		#return self.aset,self.bset
	def costsearch(self,g,source,des,cost,a,b):#根据cost搜出所有路径
		
		#self.flag=0 #标志能不能找出更多的路
		if self.flag==1:
			return [],self.aset,self.bset
		tmp=[]
		#初始化aset，bset
		self.aset=a
		self.bset=b
		#计算初始路径
		lenc=self.heapdijkstra(g,source,des)
		if self.aset==[]:
			self.aset.append(lenc)
			self.pathnum=1 
		while len(self.aset[-1])-1<=cost and self.flag==0:#还未找到所有的满足cost的路径
			i=len(self.aset)+1
			self.skshortpath(g,source,des,i)
			if len(self.aset)==self.pathnum:#说明已经找出所有路径，不必再找
				self.flag=1
			else:
				self.pathnum=len(self.aset)
			#如果找到的路径长度大于lenc，说明找出全部长度为lenc的路径 
		for i in self.aset:
			if len(i)-1==cost:
				tmp.append(i)

		return tmp,self.aset,self.bset



	"""
		if self.aset==[]:
			self.aset.append(lenc)
			self.pathnum=1
		if len(self.aset[-1])-1!=cost:
			return [],self.aset,self.bset
		#找出切片的前面
		for i in range(len(self.aset)):
			if len(self.aset[i])-1==cost:
				f=i
				break
		
		for i in range(f+2,sys.maxsize):
			self.skshortpath(g,source,des,i)
			if len(self.aset)==self.pathnum:#说明已经找出所有路径，不必再找
				self.flag=1
			else:
				self.pathnum=len(self.aset)
			#如果找到的路径长度大于lenc，说明找出全部长度为lenc的路径
			
			
			for j in range(f,len(self.aset)):
				if len(self.aset[j])-1>cost:
					t=self.aset[f:j:]
					return t,self.aset,self.bset
	"""
	def spfmc1(self,g,source,des,length):  #搜索路径
		self.paths=[]
		self.xz=len
		path=[]
		self.visit(g,source,des,path,length)
		return self.paths
		
	def visit(self,g,source,des,path,length):
		if len(path)>length:
			return
		if source==des:
			self.paths.append(path+[source])
			return
		path.append(source)
		for node in g[source]:
			if node[0] not in path:
				self.visit(g,node[0],des,path,length)
		path.pop()
	
	def spfmc2(self,g,source,des,length):  #搜索路径
		self.apath=[]
		self.xz=length
		path=[]
		self.visit1(g,source,des,path,length)
		return self.apath
	def visit1(self,g,source,des,path,length):
		if len(path)==length:
			self.apath.append(path+[source])
			return
		
		path.append(source)
		for node in g[source]:
			if node[0] not in path:
				self.visit1(g,node[0],des,path,length)
		path.pop()

	def walk(self,g,pathset,sou,des,cost):#返回两个集合，分别为到达目的和未到达
		found=[]
		notfound=[]
		
		for i in pathset:
			if len(i)==cost:
				for j in g[i[-1]]:
					if j[0] not in i:
						if j[0]==des:
							found.append(i+[j[0]])
						else:
							notfound.append(i+[j[0]])
		return found,notfound

	def getpath(self,u):   #获取到当前点u的路径
		tmp=u
		li=[]
		while u!=-1:
			li.append(u)
			u=self._prev[u]

		li.reverse()
		return li