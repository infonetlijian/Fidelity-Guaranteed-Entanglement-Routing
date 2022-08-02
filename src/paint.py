import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from qpass import *
import copy

#绘制提纯轮数和成功概率
def calf(f,n):
    if n==1:
        return calfgn(f,f)
    else:
        return calfgn(calf(f,n-1),f)
def calfgn(t1,t2):#不同保真度提纯：提纯操作后保真度公式
    return t1*t2/(t1*t2+(1-t2)*(1-t1))
    #return (t1*t2+((1-t1)*(1-t2))/9)/(t1*t2+t1*(1-t2)/3+t2*(1-t1)/3+5*(1-t1)*(1-t2)/9)
def calp(f,n):
    if n==1:
        return calpgn(f,f)
    else:
        return calp(f,n-1)*calpgn(calf(f,n-1),f)
def calpgn(t1,t2):#不同保真度提纯操作成功率公式
    return t1*t2+(1-t2)*(1-t1)
    #return (t1*t2+t1*(1-t2)/3+t2*(1-t1)/3+5*(1-t1)*(1-t2)/9)
"""x=np.arange(0.5,1,0.001)
for i in range(1,10):
    filename='test'+str(i)+'.txt'
    fp=open(filename,'w')
    for j in x:
        fp.write(str(j)+' '+str(i)+' '+str(calf(j,i))+' '+str(calp(j,i))+'\n')
    fp.close()"""
filename='pur_f_p'+'.txt'
fp=open(filename,'w')
fp.write('fidelity'+' '+'round1f'+' '+'round1p'+' '+'round2f'+' '+'round2p'+' '+'round3f'+' '+'round3p'+' '+'round4f'+' '+'round4p'+' '+'round5f'+' '+'round5p'+'\n')
x=np.arange(0.5,1,0.001)
n=np.arange(1,100,1)

f1=[]
f2=[]
f3=[]
f4=[]
f5=[]
p1=[]
p2=[]
p3=[]
p4=[]
p5=[]
for i in x:
    f1.append(calf(i,1))
    f2.append(calf(i,2))
    f3.append(calf(i,3))
    f4.append(calf(i,4))
    f5.append(calf(i,5))
    p1.append(calp(i,1))
    p2.append(calp(i,2))
    p3.append(calp(i,3))
    p4.append(calp(i,4))
    p5.append(calp(i,5))
    fp.write(str(i)+' '+str(calf(i,1))+' '+str(calp(i,1))+' '+str(calf(i,2))+' '+str(calp(i,2))+' '+str(calf(i,3))
             +' '+str(calp(i,3))+' '+str(calf(i,4))+' '+str(calp(i,4))+' '+str(calf(i,5))+' '+str(calp(i,5))+'\n')

fp.close
fig = plt.figure()





plt.plot(x,f1,color='red')
plt.plot(x,p1,color='green')
plt.plot(x,p2,color='green')
plt.plot(x,p3,color='green')
plt.plot(x,p4,color='green')
plt.plot(x,p5,color='green')
plt.plot(x,f2,color='green')
plt.plot(x,f3,color='green')
plt.plot(x,f4,color='green')
plt.plot(x,f5,color='green')

plt.xlabel('n')
plt.ylabel('f or p')
plt.show()

