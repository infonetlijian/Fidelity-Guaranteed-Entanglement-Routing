from scipy.special import comb, perm
import sys
class Cost:
	def __init__(self):
		self._link=[0]  #初始化路径

	def _costEXT(self,g,path):
		global  q
		self.g=g
		#跳数
		self._hop=len(path)-1
		#纠缠交换成功率
		self._q=0.9
		#计算w
		w=self._calcuteW(path)
		if w==0:
			return sys.maxsize
		#计算EXT
		sumPih=0
		for num in range(1,w+1):
			sumPih+=num*self._calcutePih(num,self._hop,w)
		e=self._q**self._hop*sumPih
		if e==0:
			return sys.maxsize
		return 1/e

	#计算Pih
	def _calcutePih(self,i,k,w):
		if k==1:
			return self._calcuteQih(i,k,w)
		else:
			sumQlk=0
			for num in range(i,w+1):
				sumQlk+=self._calcuteQih(num,k,w)
			sumPlk_1=0
			for num in range(i+1,w+1):
				sumPlk_1+=self._calcutePih(num,k-1,w)

			return self._calcutePih(i,k-1,w)*sumQlk+self._calcuteQih(i,k,w)*sumPlk_1
	
	#计算Qih
	def _calcuteQih(self,i,k,w):
		Q=comb(w,i)*self._link[k]._p**i*(1-self._link[k]._p)**(w-i)
		return Q

	#w
	def _calcuteW(self,path):
		w=5000
		for i in range(len(path)-1):
			self._link.append(self.g[path[i]][path[i+1]])
			if self.g[path[i]][path[i+1]]._c<w:
				w=self.g[path[i]][path[i+1]]._c
		return w