from __future__ import division
from operator import itemgetter
from copy import deepcopy
import sys
from itertools import combinations


def net_stats(network):
    num_edges = len(network)
    num_homodimers = 0
    nodes = set()

    for edge in network:
        nodes.add(edge[0])
        nodes.add(edge[1])
        if edge[0] == edge[1]:
            num_homodimers += 1

    num_nodes = len(nodes)
    total_degree = 0
    for node in nodes:
        total_degree += degree(network, node)

    avg_degree = total_degree / float(num_nodes)

    return num_nodes, num_edges, num_homodimers, avg_degree


def trian(G, nodes=None):
    return dict((v, t // 2) for v, d, t in _get_td(G, nodes))


def get_td(G):
    nodes_nbrs = G.items()
    for v, v_nbrs in nodes_nbrs:
        vs = set(v_nbrs) - set([v])
        ntrian = 0
        for w in vs:
            ws = set(G[w]) - set([w])
            ntrian += len(vs.intersection(ws))
        yield (v, len(vs), ntrian)


def clust(G):
    r"""
    References:
       "http://www.cl.cam.ac.uk/~cm542/teaching/2011/stna-pdfs/stna-lecture11.pdf"
    """
    td_iter = get_td(G)

    clusterc = {}

    for v, d, t in td_iter:
        if t == 0:
            clusterc[v] = 0.0
        else:
            clusterc[v] = t / float(d * (d - 1.0))

    return clusterc


def get_adj(edge, n1, n2):
    """
    References:
       https://www.udacity.com/course/cs215
    """
    if n1 not in edge:
        edge[n1] = {}
    if n1 == n2:
        (edge[n1])[n2] = {}
    else:
        (edge[n1])[n2] = {}
    if n2 not in edge:
        edge[n2] = {}
    if n1 == n2:
        (edge[n2])[n1] = {}
    else:
        (edge[n2])[n1] = {}
    return edge

def avg_clust(G):
    cs = clust(G)
    avg_cs = sum(cs.values()) / float(len(cs))
    return avg_cs


netfile = open(sys.argv[1])
#netfile = open("dmNet.txt")
net = [n.split() for n in netfile]

ppi = []
for p in net:
    ppi.append((p[0], p[1]))

adj = {}
for a, b in ppi:
    get_adj(adj, a, b)

cs = clust(adj)
#avg_cs = sum(cs.values()) / float(len(cs))
avg_cs = avg_clust(adj)
avg_cs_round = round(avg_cs, 6)
print avg_cs_round