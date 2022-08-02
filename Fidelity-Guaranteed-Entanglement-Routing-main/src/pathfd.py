class Cpathfd:
    def __init__(self):
        pass

    def calpathfd(self,path,freedlist):
        freed=0
        for i in range(len(path)-1):
            freed+=freedlist[i]

        freed-=len(path)-2
        return freed
    def caluti(self,freed,de,a=0,b=1):#计算路径的uti值
        sum=0
        for i in de:
            sum+=i
       
        return a*freed+b*sum
