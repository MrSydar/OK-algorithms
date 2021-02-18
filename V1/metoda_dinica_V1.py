from sys import maxsize

def getPath(currNode: int, toNode: int, graph: list, nodePriority: list, graphUsed: list, visitedNodes: list, path: list):
    if currNode == toNode:
        path.append(currNode)
        return True
    
    nodeNum = len(graph)

    nextNodes = []
    for nodeIndex in range(nodeNum):
        if not visitedNodes[nodeIndex] and ((graph[currNode][nodeIndex] - graphUsed[currNode][nodeIndex]) != 0 or graphUsed[nodeIndex][currNode] != 0):
            nextNodes.append(nodeIndex)
            visitedNodes[nodeIndex] = True
    
    nextNodes = sorted(nextNodes, key= lambda x: nodePriority[x])
    
    for nodeIndex in nextNodes:
        if getPath(nodeIndex, toNode, graph, nodePriority, graphUsed, visitedNodes, path):
            path.append(currNode)
            return True
    
    for nodeIndex in nextNodes:
        visitedNodes[nodeIndex] = False

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
        if getPath(fromNode, toNode, graph, nodePriority, graphUsed, [False] *  n, path):
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

myNodeNames = ['s', '2', '3', '4', 't']
#             s  2  3  4  t
myPriority = [0, 1, 3, 2, -1] # priorytet obrania wierszchołków przy budowaniu ścieżki. Im mniejszy tym lepszy. (użyteczne np. jeżeli ważna jest kolejność obrania krawędzi). Nie wpływa na ostateczny wynik, tylko na ścieżki.
myGraph = [
# to:s  2  3  4  t      from
    [0, 5, 6, 1, 1],  # s
    [0, 0, 3, 2, 0],  # 2
    [0, 0, 0, 2, 9],  # 3
    [0, 0, 0, 0, 7],  # 4
    [0, 0, 0, 0, 0]   # t
]

myDeltaSum = dinic(0, len(myGraph) - 1, myGraph, myPriority, myNodeNames)
print('Max flow is {}'.format(myDeltaSum))