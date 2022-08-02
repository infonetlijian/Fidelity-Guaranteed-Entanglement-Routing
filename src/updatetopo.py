import sys,heapq
class Udtp:#拓扑更新
    def __init__(self):
        pass
    def udtp(self,network,fth):  #去除小于Fth的边
        for i in network:
            for j in i:
                if j._isconnected is True:
                    if j._c==0 or j.ftable[-1][0]<fth:
                        j.dellink()
     
    def preudtppath(self,g,path,de):  #计算路径能否满足一份提纯要求，如果不能将小于一份的资源删去。
        for i in range(len(path)-1):
            if g[path[i]][path[i+1]]._c<de[i]+1:
                g[path[i]][path[i+1]].dellink()
                g[path[i+1]][path[i]].dellink()
                return False
        return True
    def ispathconnect(self,g,path): #判断路径是否联通
        for i in range(len(path)-1):
            if g[path[i]][path[i+1]]._isconnected is False and g[path[i+1]][path[i]]._isconnected is False:
                return False
        return True
    def preudtppathc(self,g,path,con): #计算路径能否满足消耗要求
        for i in range(len(path)-1):
            if g[path[i]][path[i+1]]._c<con[i]:
                return False
        return True
    def udtppathc(self,g,path,con): #去除topo上路径消耗的资源
        for i in range(len(path)-1):
            g[path[i]][path[i+1]]._c-=con[i]
            g[path[i+1]][path[i]]._c-=con[i]
            if g[path[i]][path[i+1]]._c==0:
                g[path[i]][path[i+1]].dellink()
                g[path[i]][path[i+1]].dellink()

    def udtppath(self,g,path,con,fth): #去除一条路径的资源
        
        for i in range(len(path)-1):
            g[path[i]][path[i+1]]._c-=con[i]
            g[path[i+1]][path[i]]._c-=con[i]
            if g[path[i]][path[i+1]]._c<=0:
                g[path[i+1]][path[i]].dellink()
                g[path[i]][path[i+1]].dellink()
                continue 
            g[path[i]][path[i+1]].calftable()
            g[path[i+1]][path[i]].calftable()
            #移除不满足f>Fth的边
            if g[path[i]][path[i+1]].ftable[-1][0]<fth:
                g[path[i]][path[i+1]].dellink()
                g[path[i+1]][path[i]].dellink()

    def delpath(self,g,path): #将path从拓扑删去
        for i in range(len(path)-1):
            g[path[i]][path[i+1]].dellink()

    def topocost(self,g): #将拓扑转换为跳数邻接矩阵
        a=[]
        for i in range(len(g)):
            tmp=[]
            for j in range(len(g)):
                if i==j:
                    tmp.append(0)
                elif g[i][j]._isconnected is True:
                    tmp.append(1)
                else:
                    tmp.append(sys.maxsize/2)
            a.append(tmp)
        return a
    def topoljb(self,g):#临接矩阵转换为邻接表
        a=[]
        for i in range(len(g)):
            tmp=[]
            for j in range(len(g)):
                if g[i][j]==1:
                    tmp.append([j,1])
            a.append(tmp)

        return a

    def topoljbf(self,g):#将拓扑转换为邻接表(保真度)
        a=[]
        for i in range(len(g)):
            tmp=[]
            for j in range(len(g)):
                if g[i][j]._isconnected is True:
                    tmp.append([j,g[i][j]._f])
                
            a.append(tmp)
        return a


        