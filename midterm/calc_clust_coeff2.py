from __future__ import division
from operator import itemgetter
from copy import deepcopy
import sys
from itertools import combinations


def triangles(G, nodes=None):
    r"""
    References:
       Generalizations of the clustering coefficient to weighted
       complex networks. J. Saramäki, et al.  Physical Review (2007).
       http://jponnela.com/web_documents/a9.pdf
    """
    return dict( (v,t // 2) for v,d,t in _triangles_and_degree_iter(G,nodes))

def triangles_and_degree_iter(G):
    #nodes_nbrs = G.adj.items()
    nodes_nbrs = G.items()
    for v,v_nbrs in nodes_nbrs:
        vs=set(v_nbrs)-set([v])
        ntriangles=0
        for w in vs:
            ws=set(G[w])-set([w])
            ntriangles+=len(vs.intersection(ws))
        yield (v,len(vs),ntriangles)

def average_clustering(G):

    c=clustering(G,nodes,weight=weight).values()
    return sum(c)/float(len(c))

def clustering(G):
       r"""
    References:
       http://www.cl.cam.ac.uk/~cm542/teaching/2011/stna-pdfs/stna-lecture11.pdf
    """
    td_iter= triangles_and_degree_iter(G)

    clusterc={}

    for v,d,t in td_iter:
        if t==0:
            clusterc[v]=0.0
        else:
            clusterc[v]=t/float(d*(d-1))

    return clusterc




def get_adj(edge, n1, n2):
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
        (edge[n2])[n1] =  {}
    return edge

netfile= open(sys.argv[1])
#netfile = open("dmNet.txt")
net = [n.split() for n in netfile]

ppi = []
for p in net:
    ppi.append((p[0], p[1]))

adj = {}
for a, b in ppi:
    get_adj(adj, a, b)

cs = clustering(adj)
avg_cs = sum(cs.values())/float(len(cs))
print avg_cs