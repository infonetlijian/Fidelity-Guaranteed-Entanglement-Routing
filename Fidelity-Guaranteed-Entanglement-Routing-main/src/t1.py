import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from qpath import *
from qleap import *
from alg2k import *
from hopspf import *
import copy,time
import networkx as nx

#fth作为自变量，单sd,数据保存于代码主文件夹下的txt文件中，运行次数count可以自定义。
#算法输入为拓扑，源，目的，保真度阈值，请求数量。
#算法返回值为：路径集，提纯决策集，保真度集，纠缠消耗集，吞吐量集，总吞吐量，寻路时间。

#算法变量设置
#总仿真次数
def SingleSdFth(count=10,x=np.arange(0.55,0.95,0.05),topology_fidelity_mode=0,nrof_requests=10000,alg1_mode=1,link_capacity=10,random_topology = 0,random_topology_mode=0,random_topology_nodes_num =5):
    """
    count=10
    #模式0代表重新生成，模式1代表读取之前保存的链路保真度数值
    topology_fidelity_modeS=0
    #单S-Dpair的请求connection数量
    nrof_requests=1
    #Alg1的运行模式，BFS搜索为0，k-shortest为1
    alg1_mode=1
    #链路容量设置
    link_capacity=10
    #保真度的范围
    x=np.arange(0.55,0.95,0.05)

    #x=np.arange(0.7,0.75,0.005)
    #本次仿真中启用的对比算法
    
    # 随机拓扑设置，1代表开启
    random_topology = 0
    #0代表每次生成随机的，1代表读取文件中的拓扑
    random_topology_mode=0
    random_topology_nodes_num =5
    """
    enable_Hspf=0#基于跳数的
    enable_alg1=1
    enable_alg2=1
    start_time=time.time()
    graph_topology_file_name1='random_topology_nodes_with_nrof_nodes_'+str(random_topology_nodes_num)+'.txt'
    graph_topology_file_name2='random_topology_edges_with_nrof_nodes_'+str(random_topology_nodes_num)+'.txt'
    filename='Single_SDPair_vs_Fidelity.txt'
    print('result saved in'+filename)
    fp = open(filename, 'w')
    #先写入数据标题
    utput_label = 'fth      '
    if enable_Hspf == 1:
        utput_label += 'throughput_hopCount      avgFidelity_hopCount      avepurround_hopCount      consumption_hopcount      time_hopCount      '
    if enable_alg1 == 1:
        utput_label += 'throughput_alg1      avgFidelity_alg1      avepurround_alg1      consumption_alg1      time_alg1      '
    if enable_alg2 == 1:
        utput_label += 'throughput_alg2      avgFidelity_alg2      avepurround_alg2      consumption_alg2      time_alg2'
    utput_label += '\n'
    # output_label = 'fth    tphopcount    tpalg1    tpalg2    tpalg2k    tpalg2k3    tpalg2k4    tpalg2k5    ' \
    #                    'avefhopcount    avefalg1    avefalg2    avefalg2k    avefalg2k3    avefalg2k4    avefalg2k5    ' \
    #                    'consuhopcount    consualg1    consualg2    consualg2k    consualg2k3    consualg2k4    consualg2k5    ' \
    #                    'timehop    timealg1    timealg2    timealg2k    timealg2k3    timealg2k4    timealg2k5\n'
    fp.write(utput_label)

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

    countf=[0]*len(x)
    countf1=[0]*len(x)
    countf2=[0]*len(x)

    purroundh=[0]*len(x)
    purround1=[0]*len(x)
    purround2=[0]*len(x)


    for i in range(count):
        print('running '+str(i)+' time:',str(time.time()-start_time)+'\n')
    
        #fp.write(str(i)+'    '+str(sou)+'    '+str(des)+'    ')
        if random_topology == 1:
            #采用随机生成拓扑，或者读取相同的拓扑
            if random_topology_mode == 0:
                # 生成随机拓扑
                nodes, edges, positions = create_random_topology(random_topology_nodes_num, 0.5, 1)

                graph_topology_save_name1 = graph_topology_file_name1
                graph_topology_file1 = open(graph_topology_save_name1, 'w')
                graph_topology_save_name2 = graph_topology_file_name2
                graph_topology_file2 = open(graph_topology_save_name2, 'w')
                for index in range(len(nodes)):
                    graph_topology_file1.write(str(nodes[index]) + '\n')
                for index in range(len(edges)):
                    graph_topology_file2.write(str(edges[index]) + '\n')

            if random_topology_mode == 1:
                nodes=[]
                edges0=[]
                # 读取已有的随机产生拓扑，以确保仿真的一致性
                graph_topology_save_name1 = graph_topology_file_name1
                graph_topology_save_name2 = graph_topology_file_name2
                graph_nodes_file = open(graph_topology_save_name1, 'r')
                graph_edges_file = open(graph_topology_save_name2, 'r')

                #分别读取节点和边
                for line in graph_nodes_file.readlines():
                    line=line.strip('\n')
                    #line = line.strip('\'')
                    nodes.append(line)
                for line in graph_edges_file.readlines():
                    line=line.strip('\n')
                    line.replace("''", "")
                    edges0.append(line)
                #nodes=graph_nodes_file.readlines()
                #edges=graph_edges_file.readlines
                edges=[]
                length=len(edges0)-1
                for index in range(length):
                    #edges.append((edges0[index]))
                    #edges.append((nodes[j], nodes[i]))
                    #print(index)
                    #print(edges0[index])
                    edges.append(eval(edges0[index]))
                #print(edges)
                #print(type(edges[1]))
            # 采用随机拓扑
            #nodes, edges, positions = create_random_topology(random_topology_nodes_num, 0.06, 1)
            network = Net().network
            network[0] = nodes
            network[1] = edges
            network = Vtopo().creatbasicvtopo(network, link_capacity, topology_fidelity_mode)
            g = Vtopo().creatvtopo(network)

        else:
            #采用骨干网拓扑
            network = Net().network
            #print("test")
            #print(len(network[0]))
            #print(len(network[1]))
            network = Vtopo().creatbasicvtopo(network, link_capacity, topology_fidelity_mode)
            g = Vtopo().creatvtopo(network)
        #x=np.arange(0.5,1,0.05)
        #随机产生sd点
        sou=random.randint(0,len(g)-1)
        des=random.randint(0,len(g)-1)
        while des==sou:
            des=random.randint(0,len(g)-1)
        print('source=',sou,'des=',des)
        tphspf=[]
        yalg1=[]
        yalg2=[]
    
        for j in range(len(x)):
            print("fidelity threshold: "+str(x[j]))
            time_0=time.time()

            if enable_Hspf == 1:
                #path,d,fi,con,th,sumt,times=Hspf().hspf(copy.deepcopy(g),sou,des,x[j],nrof_requests)
                path,d,fi,con,th,sumt,times=Hspf().hspf(copy.deepcopy(g),sou,des,x[j],nrof_requests)
                #print(path,d,fi,con,th,sumt)
                #if path !=[]:
                    #print(path,d)
            
                timeh[j]+=times
                tmpsf=0
                tmpsc=0
                tmpr=0
                for i in range(len(fi)):
                    tmpsf+=fi[i]
                
                    for c in con[i]:
                        tmpsc+=c
                    for r in d[i]:
                        tmpr+=r
                if len(fi)>0:
                    purroundh[j]+=tmpr
                    avefhopcount[j]+=(tmpsf/len(fi))
                    stphspf[j]+=sumt
                    consuhopcount[j]+=tmpsc
                    countf[j]+=1
        
            time_1=time.time()
            if enable_alg1 == 1:
                path1,d1,fi1,con1,th1,sumt1,times1=Qpath().alg1(copy.deepcopy(g),sou,des,x[j],nrof_requests,alg1_mode,3)
                #print(path1,d1,fi1,con1,th1,sumt1)
                 
                
                time1[j]+=times1
                tmpsf1=0
                tmpsc1=0
                tmpr1=0
                for i in range(len(fi1)):
                    tmpsf1+=fi1[i]
                    for c in con1[i]:
                        tmpsc1+=c
                    for r in d1[i]:
                        tmpr1+=r
                if len(fi1)>0:
                    purround1[j]+=tmpr1
                    avefalg1[j]+=(tmpsf1/len(fi1))
                    stpalg1[j]+=sumt1
                    consualg1[j]+=tmpsc1
                    countf1[j]+=1

            time_2=time.time()
            if enable_alg2 == 1:
                path2,d2,fi2,con2,th2,sumt2,times2=Qleap().alg2(copy.deepcopy(g),sou,des,x[j],nrof_requests)
                #print(path2,d2,fi2,con2,th2,sumt2)
                time2[j]+=times2
                tmpsf2=0
                tmpsc2=0
                tmpr2=0
                for i in range(len(fi2)):
                    tmpsf2+=fi2[i]
                    for c in con2[i]:
                        tmpsc2+=c
                    for r in d2[i]:
                        tmpr2+=r
                if len(fi2)>0:
                    purround2[j]+=tmpr2
                    avefalg2[j]+=(tmpsf2/len(fi2))
                    stpalg2[j]+=sumt2
                    consualg2[j]+=tmpsc2
                    countf2[j]+=1



    #print(stphspf)
    #print(stpalg1)
    #print(stpalg2)


    for i in range(len(x)):
    
    
    
    
        if countf[i] == 0:
            countf[i] =1
        stphspf[i]/=count
        avefhopcount[i]/=countf[i]
        if countf1[i] == 0:
            countf1[i] =1
        stpalg1[i]/=count
        avefalg1[i]/=countf1[i]
        if countf2[i] == 0:
            countf2[i] =1
        avefalg2[i]/=countf2[i]
        stpalg2[i]/=count
        consuhopcount[i]/=count
        consualg1[i]/=count
        consualg2[i]/=count
   
        timeh[i]/=count
        time1[i]/=count
        time2[i]/=count
    
        purroundh[i]/=countf[i]
        purround1[i]/=countf1[i]
        purround2[i]/=countf2[i]




        output_result = str(round(x[i], 2))
        if enable_Hspf == 1:
            output_result += '    '+str(stphspf[i])+'    '+str(avefhopcount[i])+'    '+str(purroundh[i])+'    '+str(consuhopcount[i])+'    '+str(timeh[i])+'    '
        if enable_alg1 == 1:
            output_result += '    '+str(stpalg1[i])+'    '+str(avefalg1[i])+'    '+str(purround1[i])+'    '+str(consualg1[i])+'    '+str(time1[i])+'    '
        if enable_alg2 == 1:
            output_result += '    '+str(stpalg2[i])+'    '+str(avefalg2[i])+'    '+str(purround2[i])+'    '+str(consualg2[i])+'    '+str(time2[i])+'    '
        output_result += '\n'
        print(output_result)
        #fp.write(str(x[i])+'    '+str(stphspf[i])+'    '+str(stpalg1[i])+'    '+str(stpalg2[i])+'    '+str(stpalg2k[i])+'    '+str(stpalg2k3[i])+'    '+str(stpalg2k4[i])+'    '+str(stpalg2k5[i])+'    '+str(avefhopcount[i])+'    '+str(avefalg1[i])+'    '+str(avefalg2[i])+'    '+str(avefalg2k[i])+'    '+str(avefalg2k3[i])+'    '+str(avefalg2k4[i])+'    '+str(avefalg2k5[i])+'    '+str(consuhopcount[i])+'    '+str(consualg1[i])+'    '+str(consualg2[i])+'    '+str(consualg2k[i])+'    '+str(consualg2k3[i])+'    '+str(consualg2k4[i])+'    '+str(consualg2k5[i])+'    '+str(timeh[i])+'    '+str(time1[i])+'    '+str(time2[i])+'    '+str(time2k[i])+'    '+str(time2k3[i])+'    '+str(time2k4[i])+'    '+str(time2k5[i])+'\n')
        fp.write(output_result)
    fp.close()
    #print(countf)
    fig = plt.figure()
    plt.plot(x,stphspf,color='red')
    plt.plot(x,stpalg1,color='green')
    plt.plot(x,stpalg2,color='black')
    plt.title("")
    plt.xlabel('fth')
    plt.ylabel('expect throughput')
    plt.show()

