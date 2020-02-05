import numpy as np
import random
import string
import copy

def f(a):
    for i in range(len(v)):
        if a == v[i]:
            return i
    return -1
u = list(range(1,11))
v = string.ascii_lowercase[0:10]

rawgraph = np.zeros((11,11),dtype=object)
#1----a
#2-\  b
#3  \-c

# a b c 
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
#1    a
#2    b
#3    d
#...

#random initialisation
for i in range(1,11):
    for j in range(random.randint(2,4)):
        rawgraph[i][random.randint(0,9)] = 1

for x in range(10):
    rawgraph[0][x+1] = v[x]
for y in range(10):
    rawgraph[y+1][0] = u[y]
graph = copy.deepcopy(rawgraph)
print(graph)


for k in range(1,11):
    if M[k-1][0] == 0:# if no path exists for kth node then bredth first search
        #breadth first search
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
for letter in range(10):
    freevertices.append([v[letter],[]])
i = 0
while i < len(freevertices):
    if f(M[i][1]) != -1:
        
    
    




            
