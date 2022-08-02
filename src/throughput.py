class Etp:  
    def __init__(self):
        pass

    def caletp(self,g,path,de):#计算期望吞吐量
        tetp=[]
        tmp=500
        for i in range(len(path)-1):

            t_ext=self.calp(g[path[i]][path[i+1]],de[i])  #提纯de[i]次的成功率
            tetp.append(t_ext)
            if t_ext<tmp:
                tmp=t_ext

        return tmp
    def calp(self,l,npur):#计算在提纯链路l  npur次时成功率
        if npur==0:
            return 1
        elif npur==1:
            return self.calpgn(l._f,l._f)
        else:
            return self.calp(l,npur-1)*self.calpgn(l.ftable[npur-1][0],l.ftable[0][0])

    def calpg(self,tmpf):#提纯操作成功率公式
        return (tmpf**2+2*tmpf*(1-tmpf)/3+5*(1-tmpf)**2/9)
    def calpgn(self,t1,t2):#不同保真度提纯操作成功率公式
        return t1*t2+(1-t2)*(1-t1)
        #return (t1*t2+t1*(1-t2)/3+t2*(1-t1)/3+5*(1-t1)*(1-t2)/9)

    def calfg(self,tmpf):#相同保真度提纯：提纯操作后保真度公式
        return (tmpf**2+((1-tmpf)**2)/9)/(tmpf**2+2*tmpf*(1-tmpf)/3+5*(1-tmpf)**2/9)
    def calfgn(self,t1,t2):#不同保真度提纯：提纯操作后保真度公式
        return t1*t2/(t1*t2+(1-t2)*(1-t1))
        #return (t1*t2+((1-t1)*(1-t2))/9)/(t1*t2+t1*(1-t2)/3+t2*(1-t1)/3+5*(1-t1)*(1-t2)/9)
    def calpathsumth(self,g,path,de):#计算路径上能产生多少份单位纠缠
        minn=50000
        for i in range(len(path)-1):
            if g[path[i]][path[i+1]]._c//(de[i]+1)<minn:
                minn=g[path[i]][path[i+1]]._c//(de[i]+1)

        return minn

    def calactcon(self,de,n):#计算在n份时消耗的实际基础纠缠数
        t=[]
        for i in de:
            t.append(n*(i+1))

        return t