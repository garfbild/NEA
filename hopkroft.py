import numpy as np
import random
import string
import copy


u = list(range(1,11))

rawgraph = np.zeros((11,11),dtype=object)
#1----1
#2-\  2
#3  \-3

# 1 2 3
#1.
#2  .
#3    .


M = [[0,0],
     [0,0],
     [0,0],
     [0,0],
     [0,0],
     [0,0],
     [0,0],
     [0,0],
     [0,0],
     [0,0]]
#u    v
#u1    v3
#u2    v2
#u3    v4
#...

#random initialisation
for i in range(1,11):
    for j in range(random.randint(2,4)):
        rawgraph[i][random.randint(1,10)] = 1

for x in range(10):
    rawgraph[0][x+1] = u[x]
for y in range(10):
    rawgraph[y+1][0] = u[y]
graph = copy.deepcopy(rawgraph)
print(graph)


for k in range(1,11):
    if M[k-1][0] == 0:# if no path exists for kth node then bredth first search
        #breadth first search
        M[k-1][0] = k
        for l in range(1,11):
            if graph[k][l] == 1:
                M[k-1][0] = graph[k][0]
                M[k-1][1] = graph[0][l]
                for p in range(1,11):
                    #removing all connections between k and l nodes
                    graph[k][p] = 0
                    graph[p][l] = 0
                break
print(M)
graph = copy.deepcopy(rawgraph)
freevertices = []
for node in range(10):
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

print(freevertices)

adjgraph = {}
for u in range(1,11):
    adjgraph["u{}".format(u)] = []
    for v in range(1,11):
        if graph[u][v] == 1:
            adjgraph["u{}".format(u)].append("v{}".format(v))

for v in range(1,11):
    adjgraph["v{}".format(v)] = []
    for u in range(1,11):
        if graph[v][u] == 1:
            adjgraph["v{}".format(v)].append("u{}".format(u))

def DepthFirstSearch(visited,node,graph):
    print(visited)
    if node not in visited:
        if visited != []:
            if visited[-1][0] == "u" and M[int(visited[-1][1:])-1][1] == 0:
                return visited
        visited.append(node)
        for n in graph[node]:
            if node[0] == "u":
                if int(n[1:]) == M[int(node[1])-1][1]:
                    DepthFirstSearch(visited,n,graph)
            else:
                DepthFirstSearch(visited,n,graph)
    return visited


for freevertex in freevertices:
    visited = []
    augmentingpath = DepthFirstSearch(visited,freevertex,adjgraph)
    for node in range(len(augmentingpath)):
        if augmentingpath[node][0] == "u":
            M[int(augmentingpath[node][1:])-1][1] = int(augmentingpath[node-1][1:])
    print(M)
    print(augmentingpath)
print(adjgraph)
