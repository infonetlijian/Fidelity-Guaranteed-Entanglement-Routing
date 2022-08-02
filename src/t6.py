from mqpath import *
from mqleap import *
from mhopspf import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
import copy
import time
import numpy as np
import networkx as nx


# 保真度阈值
#两个子集SD选择
# 算法变量设置
# 总仿真次数
def MultiSdSecFth(count=1,x = np.arange(0.55, 0.95, 0.05),sumreq = 400,link_capacity = 50,norfSD_Pair = 4,SDselection = 1,topology_fidelity_mode = 0,read_random_SDpair=0,random_topology = 0,random_topology_mode=0,random_topology_nodes_num = 10,alpha=0,beta=1):
    """
    count = 1
    #本次仿真中启用的对比算法

    # 总请求连接数量
    sumreq = 400
    # 链路容量设置
    link_capacity = 50
    # 端到端保真度阈值
    x = np.arange(0.55, 0.95, 0.05)
    # S-D pair 请求数量
    norfSD_Pair = 4
    # 模式0代表重新生成，模式1代表读取之前保存的链路保真度数值
    topology_fidelity_mode = 0
    #是否通过读取SDpair对，以保证仿真的一致性
    read_random_SDpair=0
    #随机生成的SDpair记录文件
    Multiple_SDpair_save_name=str(norfSD_Pair)+'SDpairs_record'+'.txt'
    # 随机拓扑设置
    random_topology = 1
    #0代表每次生成随机的，1代表读取文件中的拓扑
    random_topology_mode=0
    random_topology_nodes_num = 10
    """
    #随机生成的SDpair记录文件
    Multiple_SDpair_save_name=str(norfSD_Pair)+'SDpairs_record'+'.txt'
    
    enable_Hspf=0#基于跳数的
    enable_alg1=1
    enable_alg2=1
    start_time=time.time()
    graph_topology_file_name1='random_topology_nodes_with_nrof_nodes_'+str(random_topology_nodes_num)+'.txt'
    graph_topology_file_name2='random_topology_edges_with_nrof_nodes_'+str(random_topology_nodes_num)+'.txt'

    start_time = time.time()
    filename = 'Multiple_SDPairs_vs_Fidelity_Threshold.txt'
    fp = open(filename, 'w')
    fp.write(
        'fth    tphopcount    tpalg1    tpalg2    avefhopcount    avefalg1    avefalg2    consuhopcount    consualg1    consualg2    avepathlengthhopcount    avepathlengthalg1    avepathlengthalg2    aveperconhopcount    aveperconalg1    aveperconalg2    timehop    timealg1    timealg2\n')

    stphspf = [0] * len(x)
    stpalg1 = [0] * len(x)
    stpalg2 = [0] * len(x)

    avefhopcount = [0] * len(x)
    avefalg1 = [0] * len(x)
    avefalg2 = [0] * len(x)

    consuhopcount = [0] * len(x)
    consualg1 = [0] * len(x)
    consualg2 = [0] * len(x)
    #平均路径长度
    avepathlengthhopcount=[0] * len(x)
    avepathlengthalg1=[0] * len(x)
    avepathlengthalg2=[0] * len(x)
    #平均单个连接消耗
    aveperconhopcount=[0] * len(x)
    aveperconalg1=[0] * len(x)
    aveperconalg2=[0] * len(x)

    timeh = [0] * len(x)
    time1 = [0] * len(x)
    time2 = [0] * len(x)

    ####################生成随机拓扑，返回nodes[],edges[],positions[]##################
    ##a = alpha, b = beta
    def create_random_topology(nodes_num=50, a=0.06, b=1):##a = alpha, b = beta
        nodes = []
        edges = []
        positions = []
        edges_cost = []
        topology = [[0 for i in range(110)] for j in range(110)]
        distance = [[0 for i in range(nodes_num)] for j in range(nodes_num)]
        for n in range(0, nodes_num):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            while topology[x][y] == 1:
                x = random.randint(0, 100)
                y = random.randint(0, 100)
            topology[x][y] = 1
            nodes.append(f"N{n}")
            positions.append([x, y])
        i = 0
        max_length = -1
        while i < nodes_num:
            j = i + 1
            while j < nodes_num:
                distance[i][j] = (abs(positions[i][0] - positions[j][0]) ** 2 + abs(
                    positions[i][1] - positions[j][1])) ** 0.5
                max_length = max(max_length, distance[i][j])
                j += 1
            i += 1
        i = 0
        while i < nodes_num:
            j = i + 1
            while j < nodes_num:
                p = b * math.exp(-distance[i][j] / (max_length * a))  ##a = alpha, b = beta
                if random.random() < p:
                    edges_cost.append(round(distance[i][j], 1))
                    edges.append((nodes[i], nodes[j]))
                    edges.append((nodes[j], nodes[i]))
                j += 1
            i += 1
        g = nx.Graph()  # create graph
        g.add_nodes_from(nodes)  # add nodes
        g.add_edges_from(edges)  # add edges
        nodes_position = dict(zip(nodes, positions))  #
        node_labels = dict(zip(nodes, nodes))  # label of nodes
        edge_labels = dict(zip(edges, edges_cost))  # label of edges
        nx.draw_networkx_nodes(g, nodes_position, node_size=100, node_color="#6CB6FF")  # draw nodes
        nx.draw_networkx_edges(g, nodes_position, edges)  # draw edges
        nx.draw_networkx_labels(g, nodes_position, node_labels)  # draw label of nodes
        # nx.draw_networkx_edge_labels(g, nodes_position, edge_labels=edge_labels)  # draw label of edges
        #plt.show()
        return nodes, edges, positions

    if read_random_SDpair == 0:
        Multiple_SDpair_record = open(Multiple_SDpair_save_name, 'w')
        Multiple_SDpair_record.close()
    for i in range(count):
        print('running ' + str(i) + ' time:', str(time.time() - start_time) + '\n')

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
                print(edges0[0])
                edges=[]
                for index in range(len(edges0)-1):
                    #edges.append((edges0[index]))
                    #edges.append((nodes[j], nodes[i]))
                    edges.append(eval(edges0[index]))
                print(edges)
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
            network = Vtopo().creatbasicvtopo(network, link_capacity, topology_fidelity_mode)
            g = Vtopo().creatvtopo(network)

        for j in range(len(x)):
            print('fidelity threshold: ', x[j])
            tmpsset=[]
            tmpdset=[]
            tmpsdset = []
            sdset = []
            reqset = []
            sdnum = norfSD_Pair
            #设置保真度阈值为自变量
            fiset = [x[j]] * sdnum

            if random_topology == 1:
                total_nodes = random_topology_nodes_num
            else:
                total_nodes = 39

            ##生成需要的SD Pair
            # 选择随机生成or读取已有文件
            if read_random_SDpair == 0:
                # 随机生成SD对
                leftset=Net().leftset
                rightset=Net().rightset
                if SDselection==0:#不同源
                    while len(tmpsset) < (sdnum):
                        t = random.randint(0, len(leftset)-1)
                        if leftset[t] not in tmpsset:
                            tmpsset.append(leftset[t])
                    while len(tmpdset) < (sdnum):
                        t = random.randint(0, len(rightset)-1)
                        if rightset[t] not in tmpsset:
                            tmpdset.append(rightset[t])
                else:
                    t = random.randint(0, len(leftset)-1)
                    tmpsset.append(leftset[t])
                    tmpsset*=sdnum
                    while len(tmpdset) < (sdnum):
                        t = random.randint(0, len(rightset)-1)
                        if rightset[t] not in tmpsset:
                            tmpdset.append(rightset[t])
                for i in range(sdnum):
                    tmpsdset.append(tmpsset[i])
                    tmpsdset.append(tmpdset[i])

                Multiple_SDpair_record = open(Multiple_SDpair_save_name, 'a')  # 以a模式打开写入指针默认指向末尾
                Multiple_SDpair_record.write("record" + str(i) + '\n')
                for index in range(len(tmpsdset)):
                    Multiple_SDpair_record.write(str(tmpsdset[index]) + '\n')
                Multiple_SDpair_record.close()
            if read_random_SDpair == 1:
                Multiple_SDpair_record = open(Multiple_SDpair_save_name, 'r')
                label = 0
                read_count = 0
                for line in Multiple_SDpair_record.readlines():
                    if line.startswith("record" + str(i)):
                        label = 1
                        continue
                    if label == 1:
                        if read_count < sdnum * 2:
                            # print(tmpsdset)
                            tmpsdset.append(int(line))
                            read_count += 1

            for i in range(sdnum):
                # 进一步绑定生成S-D pair
                sdset.append(tuple([tmpsdset[2 * i], tmpsdset[2 * i + 1]]))
                reqset.append(sumreq // sdnum)

            time_0 = time.time()
            if enable_Hspf == 1:
                path, th, fi, d, con, sumt = Mhopspf().alg5(copy.deepcopy(g), sdset, fiset, reqset,alpha,beta)
                print('time of alg5 :', time.time() - time_0, '\n')
                timeh[j] += time.time() - time_0
                tmpsf = 0
                tmpsc = 0
                tmp_count = 0
                tmp_pathlen = 0
                tmp_percon = 0
                for a in range(len(con)):  # 计算总消耗纠缠数、计算总f
                    for b in range(len(con[a])):
                        for c in range(len(con[a][b])):
                            tmpsc += con[a][b][c]
                            tmp_percon += d[a][b][c]+1
                        if fi[a][b] > 0:
                            tmp_count += 1
                            tmpsf += fi[a][b]
                            tmp_pathlen += len(path[a][b])-1
                # 计算平均f,平均路径长度及路径消耗
                if tmp_count > 0:
                    tmpsf = tmpsf / tmp_count
                    avepathlengthhopcount[j] = tmp_pathlen / tmp_count
                    aveperconhopcount[j] = tmp_percon / tmp_count
                if tmpsf > 0:
                    stphspf[j] += sumt
                    consuhopcount[j] += tmpsc
                    avefhopcount[j] += tmpsf

            time_1 = time.time()
            if enable_alg1 == 1:
                path1, th1, fi1, d1, con1, sumt1 = MQpath().alg4(copy.deepcopy(g), sdset, fiset, reqset,alpha,beta)
                print('time of alg4 :', time.time() - time_1, '\n')
                time1[j] += time.time() - time_1
                tmpsf1 = 0
                tmpsc1 = 0
                tmp_count = 0
                tmp_pathlen = 0
                tmp_percon = 0
                for a in range(len(con1)):  # 计算总消耗纠缠数、计算总f
                    for b in range(len(con1[a])):
                        for c in range(len(con1[a][b])):
                            tmpsc1 += con1[a][b][c]
                            tmp_percon += d1[a][b][c]+1
                        if fi1[a][b] > 0:
                            tmp_count += 1
                            tmpsf1 += fi1[a][b]
                            tmp_pathlen += len(path1[a][b])-1
                # 计算平均f
                if tmp_count > 0:
                    tmpsf1 = tmpsf1 / tmp_count
                    avepathlengthalg1[j] += tmp_pathlen / tmp_count
                    aveperconalg1[j] += tmp_percon / tmp_count
                if tmpsf1 > 0:
                    stpalg1[j] += sumt1
                    consualg1[j] += tmpsc1
                    avefalg1[j] += tmpsf1

            time_2 = time.time()
            if enable_alg2 == 1:
                path2, th2, fi2, d2, con2, sumt2 = MQleap().alg3(copy.deepcopy(g), sdset, fiset, reqset,alpha,beta)
                print('time of alg3 :', time.time() - time_2, '\n')
                time2[j] += time.time() - time_2
                tmpsf2 = 0
                tmpsc2 = 0
                tmp_count = 0
                tmp_pathlen = 0
                tmp_percon = 0
                for a in range(len(con2)):  # 计算总消耗纠缠数、计算总fi
                    for b in range(len(con2[a])):
                        for c in range(len(con2[a][b])):
                            tmpsc2 += con2[a][b][c]
                            tmp_percon += d2[a][b][c]+1
                        if fi2[a][b] > 0:
                            tmp_count += 1
                            tmpsf2 += fi2[a][b]
                            tmp_pathlen += len(path2[a][b])-1
                # 计算平均f
                if tmp_count > 0:
                    tmpsf2 = tmpsf2 / tmp_count
                    avepathlengthalg2[j] += tmp_pathlen / tmp_count
                    aveperconalg2[j] += tmp_percon / tmp_count
                if tmpsf2 > 0:
                    stpalg2[j] += sumt2
                    consualg2[j] += tmpsc2
                    avefalg2[j] += tmpsf2

    for i in range(len(x)):
        stphspf[i] /= count
        stpalg1[i] /= count
        stpalg2[i] /= count
        avefhopcount[i] /= count
        avefalg1[i] /= count
        avefalg2[i] /= count
        consuhopcount[i] /= count
        consualg1[i] /= count
        consualg2[i] /= count
        avepathlengthhopcount[i] /= count
        avepathlengthalg1[i] /= count
        avepathlengthalg2[i] /= count
        aveperconhopcount[i] /= count
        aveperconalg1[i] /= count
        aveperconalg2[i] /= count

        fp.write(str(x[i]) + '    ' + str(stphspf[i]) + '    ' + str(stpalg1[i]) + '    ' + str(stpalg2[i]) + '    ' + 
                 str(avefhopcount[i]) + '    ' + str(avefalg1[i]) + '    ' + str(avefalg2[i]) + '    ' + 
                 str(consuhopcount[i]) + '    ' + str(consualg1[i]) + '    ' + str(consualg2[i]) + '    ' + 
                 str(avepathlengthhopcount[i]) + '    ' + str(avepathlengthalg1[i]) + '    ' + str(avepathlengthalg2[i]) + '    ' + 
                 str(aveperconhopcount[i]) + '    ' + str(aveperconalg1[i]) + '    ' + str(aveperconalg2[i]) + '    ' + 
                 str(timeh[i]) + '    ' + str(time1[i]) + '    ' + str(time2[i]) + '\n')

    fp.close()
    fig = plt.figure()
    plt.plot(x, stphspf, color='red')
    plt.plot(x, stpalg1, color='green')
    plt.plot(x, stpalg2, color='black')
    plt.title("")
    plt.xlabel('c')
    plt.ylabel('expect throughput')
    plt.show()