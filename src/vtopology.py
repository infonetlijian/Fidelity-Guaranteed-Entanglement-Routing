from vlink import *
import math
import random
import sys
from scipy.special import comb, perm
class Vtopo:
	def __init__(self):
		pass

	####################生成随机拓扑，返回nodes[],edges[],positions[]##################
	##a = alpha, b = beta
	def create_random_topology(nodes_num=78, a=0.6, b=1):  ##a = alpha, b = beta
		nodes = []
		edges = []
		positions = []
		edges_cost = []
		topology = [[0 for i in range(110)] for j in range(110)]
		distance = [[0 for i in range(nodes_num)] for j in range(nodes_num)]
		for n in range(0, nodes_num):
			x = random.randint(0, 100)
			y = random.randint(0, 100)
			while topology[x][y] == 1:
				x = random.randint(0, 100)
				y = random.randint(0, 100)
			topology[x][y] = 1
			nodes.append(f"N{n}")
			positions.append([x, y])
		i = 0
		max_length = -1
		while i < nodes_num:
			j = i + 1
			while j < nodes_num:
				distance[i][j] = (abs(positions[i][0] - positions[j][0]) ** 2 + abs(
					positions[i][1] - positions[j][1])) ** 0.5
				max_length = max(max_length, distance[i][j])
				j += 1
			i += 1
		i = 0
		while i < nodes_num:
			j = i + 1
			while j < nodes_num:
				p = b * math.exp(-distance[i][j] / (max_length * a))  ##a = alpha, b = beta
				if random.random() < p:
					edges_cost.append(round(distance[i][j], 1))
					edges.append((nodes[i], nodes[j]))
					edges.append((nodes[j], nodes[i]))
				j += 1
			i += 1
		return nodes, edges, positions
		
	def _set(self,i,j,c=0,p=1,f=1):
		self._topo[i][j]._c=c
		self._topo[i][j]._p=p
		self._topo[i][j]._f=f
		self._topo[i][j]._isconnected=True

	def creatvtopo(self,network):#返回邻接矩阵
		self._node=network[0]
		self._edge=network[1]
		
		self._topo=[]
		for i in range(len(self._node)):
			t=[]
			for j in range(len(self._node)):
				t.append(Link())
			self._topo.append(t)
		
		i=0
		dictnode={}
		for node in self._node:
			dictnode[node]=i
			i+=1
		for edge in self._edge:
			#self._set(dictnode.get(edge[0]),dictnode.get(edge[1]))
			self._topo[dictnode.get(edge.fr)][dictnode.get(edge.to)]=edge
		
		return self._topo

	def creatbasicvtopo(self,network,c=1000,mode=0,file_name='graph_fidelity_data.txt'):#转换格式，返回值为节点集边集
		self._node=network[0]
		self._edge=network[1]
		if mode == 0:
		#生成随机正态分布随机数
			num=[]
			while len(num)<len(self._edge):
				t=random.normalvariate(0.9,0.1)
				if t<1 and t >0.8:
					num.append(t)

			graph_fidelity_save_name = file_name
			graph_fidelity_file = open(graph_fidelity_save_name, 'w')
			for index in range(len(num)):
				graph_fidelity_file.write(str(num[index])+'\n')

		if mode == 1:
			# 读取已有的随机链路保真度的值，以确保仿真的一致性
			graph_fidelity_save_name = file_name
			graph_fidelity_file = open(graph_fidelity_save_name, 'r')
			num = []
			for index in range(len(open(graph_fidelity_save_name, 'rU').readlines())):
				num.append(float(graph_fidelity_file.readline()))

		#生成节点的边
		newedge=[]
		self._topo=[]
		for i in range(len(self._node)):
			t=[]
			for j in range(len(self._node)):
				t.append(Link())
			self._topo.append(t)
		i=0
		dictnode={}
		for node in self._node:
			dictnode[node]=i
			i+=1
		for i in range(len(self._edge)):
			newedge.append(Link(self._edge[i][0],self._edge[i][1],c,num[i],1,True))
			newedge.append(Link(self._edge[i][1],self._edge[i][0],c,num[i],1,True))

		return [self._node,newedge]

	def calg(self,topo): #计算节点自由度
		#topo=self.creatvtopo(network)
		self.freedegree=[]
		for i in range(len(topo)):
			t=0
			for j in topo[i]:
				if j._isconnected is True:
					t+=1
			self.freedegree.append(t)
		return self.freedegree
	def changec(self,g,c):
		for i in range(len(g)):
			for j in range(len(g)):
				if g[i][j]._isconnected is True:
					g[i][j]._c=c
		return g




