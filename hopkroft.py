import numpy as np
import random
import string
import copy

height,width = 10,10
u = list(range(1,height+1))

rawgraph = np.zeros((width+1,height+1),dtype=object)
#1----1
#2-\  2
#3  \-3

# 1 2 3
#1.
#2  .
#3    .


M = [[0,0]]*width

#u    v
#u1    v3
#u2    v2
#u3    v4
#...

#random initialisation
for i in range(1,width+1):
    for j in range(random.randint(3,4)):
        rawgraph[i][random.randint(1,width)] = 1

for x in range(width):
    rawgraph[0][x+1] = u[x]
for y in range(height):
    rawgraph[y+1][0] = u[y]
graph = copy.deepcopy(rawgraph)
print(graph)


for k in range(1,height+1):
    if M[k-1][0] == 0:# if no path exists for kth node then bredth first search
        #breadth first search
        M[k-1][0] = k
        for l in range(1,width+1):
            if graph[k][l] == 1:
                M[k-1][0] = graph[k][0]
                M[k-1][1] = graph[0][l]
                for p in range(1,width+1):
                    #removing all connections between k and l nodes
                    graph[k][p] = 0
                    graph[p][l] = 0
                break
print(M)
graph = copy.deepcopy(rawgraph)
freevertices = []
for node in range(width):
    freevertices.append(node+1)
for m in M:
    if m[1] != 0:
        freevertices[m[1]-1] = "#"

for match in M:
    if graph[match[0]][match[1]] == 1:
        print("True")
    else:
        print(match)
i = 0
while i < len(freevertices):
    if freevertices[i] == "#":
        del freevertices[i]
    else:
        freevertices[i] = "v{}".format(freevertices[i])
        i+=1

print("freevertices",freevertices)

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

print(adjgraph)

def DepthFirstSearch(visited,node,graph):
    if visited != []:
        if visited[-1][0] == "u" and M[int(visited[-1][1:])-1][1] == 0:
            return visited
    if node not in visited:
        visited.append(node)
        print(node)
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
    if augmentingpath[-1][0] == "u" and M[int(augmentingpath[-1][1:])-1][1] == 0:
        for node in range(len(augmentingpath)):
            if augmentingpath[node][0] == "u":
                M[int(augmentingpath[node][1:])-1][1] = int(augmentingpath[node-1][1:])
    print("testing")
    for match in M:
        if graph[match[0]][match[1]] == 1:
            print("True")
        else:
            print(match)
    print(M)
    print(freevertex,"augmentingpath",augmentingpath)
print(graph)
print(M)
