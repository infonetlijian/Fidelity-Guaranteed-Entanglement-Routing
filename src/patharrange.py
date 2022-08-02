class Patharr:
	def __init__(self):
		pass

	def patharr(self,path,fi,d,th): #将path集中重复的路径去除
		newpath=[]
		newfi=[]
		newd=[]
		tmp=[]
		countnz=[]
		pathth=[]
		f=[]
		tmpth=0
		
		for i in range(len(path)):
			if path[i]!=tmp:
				if th[i]>0:
					newpath.append(path[i])
					newfi.append(fi[i])
					newd.append(d[i])
					tmp=path[i]
					f.append(i)
		f.append(len(path))
		#处理吞吐量
		countnonzero=0
		for i in range(len(f)-1):
			for j in range(f[i],f[i+1]):
				tmpth+=th[j]
				if th[j]!=0:
					countnonzero+=1


			countnz.append(countnonzero)
			countnonzero=0
			pathth.append(tmpth)
			tmpth=0
		newcountnz=[]  #记录消耗多少纠缠才能达到这种吞吐量
		for i in range(len(newpath)):
			tmpncz=[]
			for j in range(len(newpath[i])-1):
				tmpncz.append(2**newd[i][j]*countnz[i])
			newcountnz.append(tmpncz)





		return newpath,newfi,newd,pathth,newcountnz