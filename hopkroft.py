import numpy as np
import random
import string
import copy

height,width = 10,10

rawgraph = np.zeros((width+1,height+1),dtype=object)
#1----1
#2-\  2
#3  \-3

# 1 2 3
#1.
#2  .
#3    .


M = []
for i in range(width):
    M.append([0,0])
#u    v
#u1    v3
#u2    v2
#u3    v4
#...

#random initialisation
for i in range(1,width+1):
    for j in range(random.randint(3,4)):
        rawgraph[i][random.randint(1,width)] = 1

#adding labels around the edge
for u in range(width):
    rawgraph[0][u+1] = u+1
for v in range(height):
    rawgraph[v+1][0] = v+1
graph = copy.deepcopy(rawgraph)

#bfs to get initial matching
for u in range(1,height+1):
    M[u-1][0] = u
    for v in range(1,width+1):
        if graph[u][v] == 1:
            M[u-1][1] = v
            for p in range(1,width+1):
                graph[u][p] = 0
                graph[p][v] = 0
            break

#finding free freevertices
graph = copy.deepcopy(rawgraph)
freevertices = []
for node in range(width):
    freevertices.append(node+1)
for m in M:
    if m[1] != 0:
        freevertices[m[1]-1] = "#"

i = 0
while i < len(freevertices):
    if freevertices[i] == "#":
        del freevertices[i]
    else:
        freevertices[i] = "v{}".format(freevertices[i])
        i+=1

#converting adjacency matrix into adjacency list
adjgraph = {}
for u in range(1,height+1):
    temp = []
    for v in range(1,width+1):
        if graph[u][v] == 1:
            temp.append("v{}".format(v))
    adjgraph["u{}".format(u)] = temp

for v in range(1,width+1):
    temp = []
    for u in range(1,height+1):
        if graph[u][v] == 1:
            temp.append("u{}".format(u))
    adjgraph["v{}".format(v)] = temp
print(freevertices)
print(M)

def DepthFirstSearch(visited,node,graph):
    print(node)
    if node not in visited:
        visited.append(node)
        #print(node)
        for n in graph[node]:
            if node[0] == "u":
                if int(n[1:]) == M[int(node[1])-1][1]:
                    DepthFirstSearch(visited,n,graph)
            else:
                DepthFirstSearch(visited,n,graph)
    return visited

#for each free vertex we find the augmenting path between two free vertices
for freevertex in freevertices:
    visited = []
    augmentingpath = DepthFirstSearch(visited,freevertex,adjgraph)
    print(augmentingpath)
    if augmentingpath[-1][0] == "u" and M[int(augmentingpath[-1][1:])-1][1] == 0:
        #symmetric difference between path and matching
        for node in range(1,len(augmentingpath)):
            if augmentingpath[node][0] == "u" and augmentingpath[node-1][0] == "v":
                M[int(augmentingpath[node][1:])-1][1] = int(augmentingpath[node-1][1:])
