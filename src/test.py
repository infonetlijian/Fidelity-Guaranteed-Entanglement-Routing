import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from alg1 import *
from alg2 import *
from hopspf import *
import copy,time

f=0.85
nrof_requests=5000
network=Net().network
network=Vtopo().creatbasicvtopo(network)
g=Vtopo().creatvtopo(network)
sou=random.randint(0,38)
des=random.randint(0,38)
while des==sou:
    des=random.randint(0,38)
print(sou,' ',des)
path,d,fi,con,th,sumt,times=Hspf().hspf(copy.deepcopy(g),sou,des,f,nrof_requests)
print(path,d,fi,con,th,sumt)
path1,d1,fi1,con1,th1,sumt1,times1=Alg1().alg1(copy.deepcopy(g),sou,des,f,nrof_requests,1,3)
print(path1,d1,fi1,con1,th1,sumt1,times1)
path2,d2,fi2,con2,th2,sumt2,times2=Alg2().alg2(copy.deepcopy(g),sou,des,f,nrof_requests)
print(path2,d2,fi2,con2,th2,sumt2,times2)