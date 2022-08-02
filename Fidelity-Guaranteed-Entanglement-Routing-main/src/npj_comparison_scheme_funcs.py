#!/usr/bin/env python
# coding: utf-8
## Functions ##

import networkx as nx
from matplotlib import pyplot as plt
import math
import numpy as np
import random
import copy
import statistics as stat
from itertools import islice


def k_shortest_paths(G, source, target, k, weight=None):
    return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))


def Weighted_Adaptive_Cancellation(total_cancellation, max_cancellation, weight):
    cancellation = [None] * len(max_cancellation)

    remaining_cancellation = total_cancellation

    # Neglect zero max_cancellation

    count_inf = 0
    remaining_vector = [i for i in range(len(max_cancellation))]
    for i in range(len(max_cancellation)):
        if max_cancellation[i] == 0:
            cancellation[i] = 0
            weight[i] = 0
            max_cancellation[i] = np.inf
            count_inf = count_inf + 1
            remaining_vector.remove(i)

    to_do_order = list(np.argsort(max_cancellation))

    for i in range(len(to_do_order) - count_inf):  # start from the smallest max_cancellation

        fraction = weight[to_do_order[i]] * max_cancellation[to_do_order[i]] / sum(
            [weight[j] * max_cancellation[j] for j in remaining_vector])
        if fraction < 0:
            print('Warning! Fraction of allocation < 0')
        temp_cancellation = np.ceil(remaining_cancellation * fraction)

        if temp_cancellation > max_cancellation[to_do_order[i]]:
            temp_cancellation = max_cancellation[to_do_order[i]]

        cancellation[to_do_order[i]] = temp_cancellation
        # print([to_do_order[i],temp_cancellation]) #--------

        ## update
        remaining_cancellation = remaining_cancellation - temp_cancellation
        if remaining_cancellation < 0:
            print('Warning! Remaining_cancellation < 0.')
            remaining_cancellation = 0
        remaining_vector.remove(to_do_order[i])

    # if remaining_cancellation > 0:
    #    print('before:' + str(cancellation))
    #    print('Warning! Remaining_cancellation = '+ str(remaining_cancellation) + '. Allocation not complete.')

    while remaining_cancellation > 0:  # still some cancellation remains

        # non_inf = [max_cancellation[nf] != math.inf for nf in range(len(max_cancellation))]
        # to_do_order = list(np.flip(list(np.argsort(max_cancellation[nf for nf in non_inf]))))  # start from the largest non-inf max_cancellation

        for i in range(len(to_do_order) - count_inf):

            if cancellation[to_do_order[i]] < max_cancellation[to_do_order[i]]:
                diff_cancel = min(max_cancellation[to_do_order[i]] - cancellation[to_do_order[i]],
                                  remaining_cancellation)
                cancellation[to_do_order[i]] = cancellation[to_do_order[i]] + diff_cancel
                remaining_cancellation = remaining_cancellation - diff_cancel

            if remaining_cancellation == 0:
                break

    if remaining_cancellation > 0:  # still some cancellation remains
        print('Warning! Remaining_cancellation = ' + str(remaining_cancellation) + '. Allocation not complete.')

    if None in cancellation:
        print('Warning! Adapative cancellation unsuccessful.')
    return cancellation


def PurificationNum(edge_fid, fid_th):
    mm = 0;
    p_suc = [];
    for i in range(50):

        if edge_fid < fid_th:
            p_suc.append((edge_fid ** 2 + (1 - edge_fid) ** 2))
            edge_fid = edge_fid ** 2 / (edge_fid ** 2 + (1 - edge_fid) ** 2);
            mm += 1;

    NeedPair = int(round(2 ** mm / (np.prod(p_suc))))
    return NeedPair, edge_fid


def Network_failure(failure, failure_num, G):
    removed_edges = []
    if failure == 1:  # random edge failure
        for i in range(failure_num):
            edge_remove = random.choice(
                [k for k in [kk for kk in G.edges() if G.edges[kk]['request_ID_on_edge'] != []]])
            G.edges[edge_remove]['flow_on_edge'] = [0] * len(G.edges[edge_remove]['flow_on_edge'])
            G.edges[edge_remove]['request_ID_on_edge'] = []
            removed_edges.append(edge_remove)

    if failure == 2:  # random node failure
        for i in range(failure_num):

            while True:

                node_remove = random.choice([k for k in G.nodes()])
                node_path_list = []
                for kk in list(G.edges(node_remove)):
                    node_path_list = node_path_list + G.edges[kk]['request_ID_on_edge']

                if node_path_list != []:
                    break

            for kkk in list(G.edges(node_remove)):  # all edges linked to the node
                G.edges[kkk]['flow_on_edge'] = [0] * len(G.edges[kkk]['flow_on_edge'])
                G.edges[kkk]['request_ID_on_edge'] = []
                removed_edges.append(kkk)

    return G, removed_edges