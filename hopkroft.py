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
#1    3
#2    2
#3    4
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
        i+=1
print(freevertices)
connections = []
for freevertex in freevertices:
    connections.append(freevertex)
    for x in range(1,11):
        if graph[x][freevertex] == 1:
            for y in range(1,11):
                if graph[y][x] == 1:
                    print(x,"connects to",y)
            





            
