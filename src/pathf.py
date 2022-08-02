from throughput import *
from queue import PriorityQueue
import copy,math,sys
class Pathf:
	def __init__(self):
		self._link=[0]  #初始化路径

	

	def _pathf(self,g,path):#计算未提纯时路径保真度
		f=1
		for i in range(len(path)-1):
			f=f*g[path[i]][path[i+1]]._f

		return f

	def _epathf(self,g,path,d):
		f=1
		for i in range(len(path)-1):
			f=f*g[path[i]][path[i+1]].ftable[d[i]][0]
		return f

	def _pathcost(self,g,path): #计算cost表中的cost
		sum=0
		for i in range(len(path)-1):
			sum+=g[path[i]][path[i+1]]
		return sum

	def _pathmincost(self,g,path,fth):#计算该路径满足fth的cost，以及提纯决定
		de=[]#初始化提纯决定
		pathf=[]
		for i in range(len(path)-1):
			de.append(0)
			pathf.append(g[path[i]][path[i+1]]._f)
		while self.pathfs(pathf)<fth:#每次最小的f提纯
			#查找最小的路径
			minf=10000000
			index=0
			for i in range(len(pathf)):
				if pathf[i]<minf:
					minf=pathf[i]
					index=i
			#进行提纯,更新提纯决定以及保真度
			
			de[index]+=1
			if de[index]>=len(g[path[index]][path[index+1]].ftable):
				return 1000000,[]
			pathf[index]=Etp().calfg(pathf[index])
		#计算cost
		sumcost=0
		for i in de:
			sumcost+=2**i
		return sumcost,de
	def _pathmincost1(self,g,path,fth):#计算该路径满足fth的cost，以及提纯决定
		de=[]#初始化提纯决定
		flag=0.743
		pathf=[]
		for i in range(len(path)-1):
			de.append(0)
			pathf.append(g[path[i]][path[i+1]]._f)
		while self.pathfs(pathf)<fth:#每次距离0.77081最近的提纯
			#查找最小的路径
			minf=10000000
			index=0
			for i in range(len(pathf)):
				if abs(pathf[i]-flag)<minf:
					minf=abs(pathf[i]-flag)
					index=i
			#进行提纯,更新提纯决定以及保真度
			
			de[index]+=1
			if de[index]>=len(g[path[index]][path[index+1]].ftable):
				return -1,[]
			pathf[index]=Etp().calfg(pathf[index])
		#计算cost
		sumcost=0
		for i in de:
			sumcost+=2**i
		return sumcost,de
	def _bfpathmincost(self,g,path,fth):#暴力搜索计算该路径满足fth的最小cost，以及提纯决定
		#判断路径所有资源能不能满足
		if self.prejudge(g,path,fth) is False:
			return -1,[]
		de=[[]]#初始化提纯决定
		alterde=[]#初始化可选提纯决定选项
		
		for i in range(len(path)-1):
			alterde.append(len(g[path[i]][path[i+1]].ftable))
		for i in alterde:#计算所有提纯选项
			for j in range(len(de)):
				tmp=de.pop(0)
				for t in range(i):
					z=copy.deepcopy(tmp)
					z.append(t)
					de.append(z)
		mincost=sys.maxsize
		tmpf=0
		mincostde=[]
		for i in de:
			pathf=[]
			for j in range(len(i)):
				pathf.append(g[path[j]][path[j+1]].ftable[i[j]][0])
			if self.pathfs(pathf)>=fth and self.ccost(i)<=mincost :
				if self.ccost(i)<mincost:
					mincost=self.ccost(i)
					mincostde=i
					tmpf=self.pathfs(pathf)
				else:
					if self.pathfs(pathf)>tmpf and self.ccost(i)==mincost:
						mincost=self.ccost(i)
						mincostde=i
						tmpf=self.pathfs(pathf)



		
		return mincost,mincostde
	def _mostup(self,g,path,fth):#每次提纯带来最大提升的一跳
		#判断路径所有资源能不能满足
		if self.prejudge(g,path,fth) is False:
			return -1,[]
		de=[]#初始化提纯决定
		pathf=[]
		for i in range(len(path)-1):
			de.append(0)
			pathf.append(g[path[i]][path[i+1]]._f)
		
		while self.pathfs(pathf)<fth:#每次提纯带来最大提升的一跳
			#查找最大的提升
			tmpf=0
			index=0
			for i in range(len(pathf)):
				tmppathf=copy.deepcopy(pathf)
				tmppathf[i]=Etp().calfgn(tmppathf[i],g[path[i]][path[i+1]]._f)
				if self.pathfs(tmppathf)>tmpf:
					tmpf=self.pathfs(tmppathf)
					index=i
					tmp=tmppathf
			
			de[index]+=1

			#进行提纯,更新提纯决定以及保真度
			
			
			if de[index]>=len(g[path[index]][path[index+1]].ftable):
				return -1,[]
			pathf=tmp



		
		return self.ccost(de),de
	def _mostup1(self,g,path,fth): #根据每次提升大小决定提纯决策
		de=[0]*(len(path)-1)#初始化提纯决定
		#维护一个优先队列
		self.q=PriorityQueue()
		pathf=[]
		for i in range(len(path)-1):
			pathf.append(g[path[i]][path[i+1]]._f)
		#建立提纯提升索引表
		purup=[]
		#计算每一跳的提纯提升索引表
		for i in range(len(path)-1):
			tmp=[]
			for j in range(len(g[path[i]][path[i+1]].ftable)):
				ttmp=[]
				ttmp.append(i)
				if j<len(g[path[i]][path[i+1]].ftable)-1:
					ttmp.append(g[path[i]][path[i+1]].ftable[j+1][0]-g[path[i]][path[i+1]].ftable[j][0])
				else:
					ttmp.append(0)
				ttmp.append(j)
				if j==0:
					ttmp.append(1)
				else:
					ttmp.append(2**(j-1))
				tmp.append(ttmp)
			purup.append(tmp)
		#初始化队列
		for i in purup:
			self.q.put([1-i[0][1],i[0]])
		while self.pathfs(pathf)<fth:
			cur=self.q.get()
			curlist=cur[1]
			if curlist[3]<2:#当前的cost增加为1
				de[curlist[0]]+=1
				if de[curlist[0]]>=len(g[path[curlist[0]]][path[curlist[0]+1]].ftable):
					return 0,[]
				pathf[curlist[0]]=Etp().calfg(pathf[curlist[0]])
				curlist=purup[curlist[0]][curlist[2]] #重新放入队列
				self.q.put([1-curlist[1],curlist])
			else:#cost增加不为1，那么有多种提纯可能,找出这种提纯可能
				sumcost=curlist[3]
				tmpcost=0
				tmpde1=de
				tmpde2=de
				tmpde1[curlist[0]]+=1
				tmpcurl=[]
				tmpout=[]
				while sumcost>0 and not self.q.empty():
					cur=self.q.get()
					curl=cur[1]
					if curl[3]<=sumcost:
						sumcost-=curl[3]
						tmpcurl.append(curl)
						tmpde2[curl[0]]+=1
					else:
						tmpout.append(cur) #暂时弹出稍后回填
				for i in tmpout:
					self.q.put(i) #回填
					
				if self._calf(g,path,tmpde1)>self._calf(g,path,tmpde2):
					de=tmpde1
					for i in tmpcurl:
						self.q.put([1-i[1],i])
					pathf[curlist[0]]=Etp().calfg(pathf[curlist[0]])
					curlist=purup[curlist[0]][curlist[2]] #重新放入队列
					self.q.put([1-curlist[1],curlist])
				else:
					de=tmpde2
					self.q.put([1-curlist[1],curlist])
					for i in tmpcurl:
						pathf[i[0]]=Etp().calfg(pathf[i[0]])
						i=purup[i[0]][i[2]] #重新放入队列
						self.q.put([1-i[1],i])
				for i in range(len(de)):
					if de[i]>=len(g[path[i][i+1]].ftable):
						return 0,[]
		return self.ccost(de),de

	def _calf(self,g,path,de):#根据提纯决定计算路径保真度
		pathf=[]
		for j in range(len(path)-1):
				pathf.append(g[path[j]][path[j+1]].ftable[de[j]][0])
		return self.pathfs(pathf)

	def ccost(self,de):
		sum=0
		for i in de:
			sum+=i+1
		return sum
	def cround(self,de):
		sum=0
		for i in de:
			sum+=i
		return sum
	def pathfs(self,pathf):
		f=1
		for i in pathf:
			f*=i
		return f
	def prejudge(self,g,path,fth): #提前判断
		pathf=[]
		#判断是否依然联通
		for i in range(len(path)-1):
			if g[path[i]][path[i+1]]._isconnected==False:
				return False
		#判断最大保真度能否满足要求
		for i in range(len(path)-1):
			pathf.append(g[path[i]][path[i+1]].ftable[-1][0])
		if self.pathfs(pathf)<fth:
			return False
		return True

	def noring(self,path):#判断是否有环
		for i in range(len(path)):
			for j in range(i+1,len(path)):
				if path[i]==path[j]:
					return False
		return True

	def pathfljb(self,g,path):
		f=1
		for i in range(len(path)-1):
			#找出对应路径
			for j in g[path[i]]:
				if j[0]==path[i+1]:
					f*=j[1]

		return f




