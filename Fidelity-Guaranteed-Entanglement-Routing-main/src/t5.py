from mqpath import *
from mqleap import *
from mhopspf import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
import copy
import time
import numpy as np

#自变量为sd数量

#算法变量设置
#总仿真次数
def Sd(count=1,x=np.arange(19,20),topology_fidelity_mode=1,fth = 0.7,sumreq = 100,link_capacity=50,save_mode = 1,read_mode = 0,alpha=0,beta=1):
    """
    count=1
    #模式0代表重新生成，模式1代表读取之前保存的链路保真度数值
    topology_fidelity_mode=1
    #端到端保真度阈值
    fth = 0.7
    #总请求连接数量
    sumreq = 100
    #链路容量设置
    link_capacity=50
    #S-D pair的读写模式设置
    save_mode = 1 #保存此次随机生成的S-0 Pair
    read_mode = 0 #读取之前随机生成的S-D Pair
    SD_Pair_file_name = 'SD_Pair_save_data.txt' #保存的文件名
    #S-D pair 请求数量
    x=np.arange(19,20)
    """

    SD_Pair_file_name = 'SD_Pair_save_data.txt' #保存的文件名
    start_time=time.time()
    filename='Multiple_SDPairs_vs_nrof_SDPairs.txt'
    fp=open(filename,'w')
    fp.write('fth    tphopcount    tpalg1    tpalg2    avefhopcount    avefalg1    avefalg2    consuhopcount    consualg1    consualg2    timehop    timealg1    timealg2\n')

    stphspf=[0]*len(x)
    stpalg1=[0]*len(x)
    stpalg2=[0]*len(x)

    avefhopcount=[0]*len(x)
    avefalg1=[0]*len(x)
    avefalg2=[0]*len(x)

    consuhopcount=[0]*len(x)
    consualg1=[0]*len(x)
    consualg2=[0]*len(x)

    timeh=[0]*len(x)
    time1=[0]*len(x)
    time2=[0]*len(x)

    for i in range(count):
        print('running '+str(i)+' time:',str(time.time()-start_time)+'\n')
    
        network=Net().network
        network=Vtopo().creatbasicvtopo(network,link_capacity,topology_fidelity_mode)
        g=Vtopo().creatvtopo(network)

        for j in range(len(x)):
            print('sdnum=',x[j])
            tmpsdset=[]
            sdset=[]
            reqset=[]
            sdnum=x[j]
            fiset=[fth]*sdnum

            #保存生成的随机SD Pair 以便于性能对比
            if read_mode == 1:
                # 读取已有的随机S-D Pair的值，以确保仿真的一致性
                SD_Pair_save_name = SD_Pair_file_name
                SD_Pair_save_file = open(SD_Pair_save_name, 'w')
                for index in range(len(open(SD_Pair_save_name, 'w').readlines())):
                    tmpsdset.append(int(SD_Pair_save_file.readline()))
            #如果不读取，就直接随机生成S-D Pair
            else:
                while len(tmpsdset) < (sdnum * 2):
                    t = random.randint(0, 38)
                    if t not in tmpsdset:
                        tmpsdset.append(t)

            if save_mode == 1:
                SD_Pair_save_name = SD_Pair_file_name
                SD_Pair_save_file = open(SD_Pair_save_name, 'w')
                for index in range(len(tmpsdset)):
                    SD_Pair_save_file.write(str(tmpsdset[index]) + '\n')
                SD_Pair_save_file.close()
                print('save successfully! \n')

            for i in range(sdnum):
                sdset.append(tuple([tmpsdset[2*i],tmpsdset[2*i+1]]))
                reqset.append(sumreq//sdnum)
        
            time_0=time.time()
            """path,th,fi,d,con,sumt=Mhopspf().alg5(copy.deepcopy(g),sdset,fiset,reqset,alpha,beta)
            print('time of alg5 :',time.time()-time_0,'\n')
            timeh[j]+=time.time()-time_0
            tmpsf=0
            tmpsc=0
            tmp_count=0
            for a in range(len(con)):#计算总消耗纠缠数、计算总f
                for b in range(len(con[a])):
                    for c in con[a][b]:
                        tmpsc+=c
                    if fi[a][b]>0:
                        tmp_count+=1
                        tmpsf+=fi[a][b]
            #计算平均f
            if tmp_count>0:
                tmpsf=tmpsf/tmp_count
            if tmpsf>0:
                stphspf[j]+=sumt
                consuhopcount[j]+=tmpsc
                avefhopcount[j]+=tmpsf
            """
            time_1=time.time()
            path1,th1,fi1,d1,con1,sumt1=MQpath().alg4(copy.deepcopy(g),sdset,fiset,reqset,alpha,beta)
            print('time of alg4 :',time.time()-time_1,'\n')
            time1[j]+=time.time()-time_1
            tmpsf1=0
            tmpsc1=0
            tmp_count=0
            for a in range(len(con1)):#计算总消耗纠缠数、计算总f
                for b in range(len(con1[a])):
                    for c in con1[a][b]:
                        tmpsc1+=c
                    if fi1[a][b]>0:
                        tmp_count+=1
                        tmpsf1+=fi1[a][b]
            #计算平均f
            if tmp_count>0:
                tmpsf1=tmpsf1/tmp_count
            if tmpsf1>0:
                stpalg1[j]+=sumt1
                consualg1[j]+=tmpsc1
                avefalg1[j]+=tmpsf1
            time_2=time.time()
            path2,th2,fi2,d2,con2,sumt2=MQleap().alg3(copy.deepcopy(g),sdset,fiset,reqset,alpha,beta)
            print('time of alg3 :',time.time()-time_2,'\n')
            time2[j]+=time.time()-time_2
            tmpsf2=0
            tmpsc2=0
            tmp_count=0
            for a in range(len(con2)):#计算总消耗纠缠数、计算总fi
                for b in range(len(con2[a])):
                    for c in con2[a][b]:
                        tmpsc2+=c
                    if fi2[a][b]>0:
                        tmp_count+=1
                        tmpsf2+=fi2[a][b]
            #计算平均f
            if tmp_count>0:
                tmpsf2=tmpsf2/tmp_count
            if tmpsf2>0:
                stpalg2[j]+=sumt2
                consualg2[j]+=tmpsc2
                avefalg2[j]+=tmpsf2
    
    for i in range(len(x)):
        stphspf[i]/=count
        stpalg1[i]/=count
        stpalg2[i]/=count
        avefhopcount[i]/=count
        avefalg1[i]/=count
        avefalg2[i]/=count
        consuhopcount[i]/=count
        consualg1[i]/=count
        consualg2[i]/=count
        fp.write(str(x[i])+'    '+str(stphspf[i])+'    '+str(stpalg1[i])+'    '+str(stpalg2[i])+'    '+str(avefhopcount[i])+'    '+str(avefalg1[i])+'    '+str(avefalg2[i])+'    '+str(consuhopcount[i])+'    '+str(consualg1[i])+'    '+str(consualg2[i])+'    '+str(timeh[i])+'    '+str(time1[i])+'    '+str(time2[i])+'\n')

    fp.close()
    fig = plt.figure()
    plt.plot(x,stphspf,color='red')
    plt.plot(x,stpalg1,color='green')
    plt.plot(x,stpalg2,color='black')
    plt.title("")
    plt.xlabel('c')
    plt.ylabel('expect throughput')
    plt.show()