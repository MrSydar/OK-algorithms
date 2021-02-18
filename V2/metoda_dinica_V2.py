from sys import maxsize
from copy import deepcopy

class sharedInt:
    def __init__(self, val: int):
        self.val = val

    def getVal(self):
        return self.val

    def setVal(self, newVal: int):
        self.val = newVal

    def increment(self):
        self.val += 1

def getPath(currNode: int, toNode: int, graph: list, nodePriority: list, graphUsed: list, visitedNodes: list, path: list, minDepth: sharedInt, depth: int):  
    if minDepth.getVal() != -1 and minDepth.getVal() <= depth:
        return False
    
    if currNode == toNode:
            minDepth.setVal(depth)
            path.clear()
            path.append(currNode)
        
    nodeNum = len(graph)

    nextNodes = []
    for nodeIndex in range(nodeNum):
        if not visitedNodes[nodeIndex] and ((graph[currNode][nodeIndex] - graphUsed[currNode][nodeIndex]) != 0 or graphUsed[nodeIndex][currNode] != 0):
            nextNodes.append(nodeIndex)
            visitedNodes[nodeIndex] = True
    
    nextNodes = sorted(nextNodes, key= lambda x: nodePriority[x])
    
    oldVal = int(minDepth.getVal())
    for nodeIndex in nextNodes:
        getPath(nodeIndex, toNode, graph, nodePriority, graphUsed, deepcopy(visitedNodes), path, minDepth, depth + 1)
    
    if minDepth.getVal() != oldVal:
        path.append(currNode)
        return True
    else:
        return False
    
def applyPath(pIndex: int, maxFlow: int, path: list, graph: list, graphUsed: list):
    if pIndex != len(path) - 1:
        if graph[path[pIndex]][path[pIndex + 1]] - graphUsed[path[pIndex]][path[pIndex + 1]] != 0:
            maxFlow = applyPath(
                pIndex + 1,
                min(maxFlow, graph[path[pIndex]][path[pIndex + 1]] - graphUsed[path[pIndex]][path[pIndex + 1]]),
                path,
                graph,
                graphUsed
            )
            graphUsed[path[pIndex]][path[pIndex + 1]] += maxFlow
        else:
            maxFlow = applyPath(
                pIndex + 1,
                min(maxFlow, graphUsed[path[pIndex + 1]][path[pIndex]]),
                path,
                graph,
                graphUsed
            )
            graphUsed[path[pIndex + 1]][path[pIndex]] -= maxFlow
    return maxFlow

def dinic(fromNode: int, toNode: int, graph: list, nodePriority: list, nodeNames: list):
    n = len(graph)
    
    graphUsed = []
    for i in range(n):
        graphUsed.append([0] * n)
    
    deltaSum = 0
    while True:
        path = []
        visitedNodes = [False] * n
        visitedNodes[fromNode] = True
        if getPath(fromNode, toNode, graph, nodePriority, graphUsed, [False] *  n, path, sharedInt(-1), -1):
            path.reverse()
            delta = applyPath(0, maxsize, path, graph, graphUsed)

            # print section [can be safely removed]
            print('Path: \033[94m ', end='')
            for i in range(len(path)):
                print(' {}\t'.format(nodeNames[path[i]]), end='')
            print('\033[0m delta = {}'.format(delta))
            # end: print section

            deltaSum += delta
        else:
            print('\nNasycone krawedzi: \033[92m')
            for i in range(n):
                for x in range(n):
                    if graph[i][x] != 0 and (graph[i][x] - graphUsed[i][x]) == 0 and i != x:
                        print('{} -> {}'.format(nodeNames[i], nodeNames[x]))
            print('\033[0m')

            print('DeltaSum: {}'.format(deltaSum))
            return sum([x for x in graphUsed[0]])

myNodeNames = ['s', '2', '3', '4', '5', 't']
#             s  2  3  4  5  t
myPriority = [0, 1, 2, 3, -1] # priorytet obrania wierszchołków przy budowaniu ścieżki. Im mniejszy tym lepszy. (użyteczne np. jeżeli ważna jest kolejność obrania krawędzi). Nie wpływa na ostateczny wynik, tylko na ścieżki.
myGraph = [
# to:s  1  2  3  t      from
    [0, 1, 0, 1, 0],  # s
    [0, 0, 1, 0, 0],  # 1
    [0, 0, 0, 0, 1],  # 2
    [0, 0, 0, 0, 1],  # 3
    [0, 0, 0, 0, 0]   # t
]

myDeltaSum = dinic(0, len(myGraph) - 1, myGraph, myPriority, myNodeNames)
print('Max flow is {}'.format(myDeltaSum))