import random
import string
import copy


rawgraph = []

height,width = 10,10
for x in range(width+1):
    rawgraph.append([])
    for y in range(height+1):
        rawgraph[x].append(0)
    
#1----1
#2-\  2
#3  \-3

# 1 2 3
#1.
#2  .
#3    .


M = []
for i in range(width):
    M.append(0)
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
    for v in range(1,width+1):
        if graph[u][v] == 1:
            M[u-1] = v
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
    if m != 0:
        freevertices[m-1] = "#"

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

global path
visited = []
path = []
#depth first search.
def DepthFirstSearch(visited,node,graph):
    #we pass the path as we back up through the recursion
    global path
    if visited != []:
        if visited[-1][0] == "u" and M[int(visited[-1][1:])-1] == 0:
            path.append(node)
            return visited
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            if visited != []:
                if visited[-1][0] == "u" and M[int(visited[-1][1:])-1] == 0:
                    path.append(node)
                    return visited
            if node[0] == "u":
                if int(n[1:]) == M[int(node[1])-1]:
                    visited = DepthFirstSearch(visited,n,graph)
            else:
                visited = DepthFirstSearch(visited,n,graph)
    if visited != []:
        if visited[-1][0] == "u" and M[int(visited[-1][1:])-1] == 0:
            path.append(node)
            return visited

    return visited

print(freevertices)
for freevertex in freevertices:
    path = []
    DepthFirstSearch(visited,freevertex,adjgraph)
    path.reverse()
    print(path)
    if path != []:
        if M[int(path[-1][1:])-1] == 0:
            #symmetric difference of a path and matching
            for x in range(len(path)):
                if path[x][0] == "u":
                    M[int(path[x][1:])-1] = int(path[x-1][1:])
        else:
            print(freevertex,"has no augmentingpath")
    else:
        print(freevertex,"has no augmentingpath")

print(M)
    
    
