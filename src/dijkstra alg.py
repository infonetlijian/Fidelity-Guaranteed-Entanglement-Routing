import sys

class Sfp:
	def __init__(self):
		self._passed=[]
		self._nopass=[]
		self._prev=[]  #从源点V0到终点Vi的当前最短路径上终点Vi的直接前驱顶点序号，若V0到Vi之间有边前驱为V0否则为-1 
		self._dis=[]  #源点到终点之间最短路径的长度，存在记V0到Vi的边的权值，否则记为MAX
		self._path=[]  #最短路径
	def dijkstra(self,G,source,des):
		#初始化已经到达的点，起始点
		self._passed.append(source)
		
		
		#初始化未经过的点
		for i in range(len(G)):
			if i!=source:
				self._nopass.append(i)
		#初始化各节点距离以及路径
		for i in range(len(G)):
			self._dis.append(G[source][i])
			if G[source][i]<sys.maxsize and i!=source:
				self._prev.append(source)
			else:
				self._prev.append(-1)

		
		while len(self._nopass):
			idx=self._nopass[0]
			#找到为遍历中的距离最短的点
			for i in self._nopass:
				if self._dis[i]<self._dis[idx]:
					idx=i
			self._nopass.remove(idx)
			self._passed.append(idx)

			#更新距离列表
			for i in self._nopass:
				if self._dis[idx]+G[idx][i]<self._dis[i]:
					self._dis[i]=self._dis[idx]+G[idx][i]
					self._prev[i]=idx
		
		#确定路径
		tmp=des
		
		while tmp!=-1:
			self._path.append(tmp)
			tmp=self._prev[tmp]

		self._path.reverse()
		return self._path
