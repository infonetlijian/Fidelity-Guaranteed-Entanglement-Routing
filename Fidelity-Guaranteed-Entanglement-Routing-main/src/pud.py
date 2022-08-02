from throughput import *
class Pud:
    def __init__(self):
        pass

    def calpud(self,g,path,fth):#计算提纯次数
        de=[]
        
        for i in range(len(path)-1):
            fl=0
            tmpf=g[path[i]][path[i+1]]._f
            while tmpf<fth:
                fl+=1
                tmpf=Etp().calfgn(tmpf,g[path[i]][path[i+1]]._f)
            de.append(fl)
        return de
    def calfthave(self,fth,n):
        return fth**(1/n)
    def calftable(self,network):
        for i in network:
            for j in i:
                if j._isconnected is True:
                    j.calftable()