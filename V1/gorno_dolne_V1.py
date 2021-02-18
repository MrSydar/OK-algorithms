from sys import maxsize
from copy import deepcopy

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

def dinic(fromNode: int, toNode: int, graph: list, graphUsed: list, nodePriority: list, nodeNames: list):
    n = len(graph)
    
    deltaSum = 0
    while True:
        path = []
        visitedNodes = [False] * n
        visitedNodes[fromNode] = True
        if getPath(fromNode, toNode, graph, nodePriority, graphUsed, [False] *  n, path):
            path.reverse()
            delta = applyPath(0, maxsize, path, graph, graphUsed)
            deltaSum += delta
            # print section [can be safely removed]
            print('Path: \033[94m ', end='')
            for i in range(len(path)):
                print(' {}\t'.format(nodeNames[path[i]]), end='')
            print('\033[0m delta = {}'.format(delta))
            # end: print section
        else:
            print('\nNasycone krawedzi: \033[92m')
            for i in range(n):
                for x in range(n):
                    if graph[i][x] != 0 and (graph[i][x] - graphUsed[i][x]) == 0 and i != x:
                        print('{} -> {}'.format(nodeNames[i], nodeNames[x]))
            print('\033[0m')
            
            print('DeltaSum: {}'.format(deltaSum))
            return sum([x for x in graphUsed[0]])

def upperlower(fromNode: int, toNode: int, graphLowerBound: list, graphUpperBound: list, nodePriority: list, nodeNames: list):
    n = len(nodePriority) + 2
    
    graph = []
    for y in range(n):
        graph.append([0] * n)

    for y in range(n - 2):
        for x in range(n - 2):
            graph[y + 1][x + 1] = graphUpperBound[y][x] - graphLowerBound[y][x]
            
        lowerOut = sum(graphLowerBound[y])
        graph[y + 1][-1] = lowerOut
        upperInner = sum([graphLowerBound[i][y] for i in range(n - 2)])
        graph[0][y + 1] = upperInner

    graph[-2][1] = float('inf')

    nodeNames.insert(0, 's\'')
    nodeNames.append('t\'')

    nodePriority.insert(0, 0)
    nodePriority.append(min(nodePriority) - 1)

    print('GORNO DOLNY GRAF:\033[91m')
    for i in range(n):
        print('{}\t'.format(nodeNames[i]), end='')
    print('\033[0m')

    for i in range(n):
        for x in range(n):
            print('{}\t'.format(graph[i][x]), end='')
        print('\033[91m{}\033[0m'.format(nodeNames[i]))
    print()

    graphUsed = []
    for i in range(n):
        graphUsed.append([0] * n)

    d1 = dinic(0, n - 1, graph, graphUsed, nodePriority, nodeNames)
    print('Delta z sieci gorno-dolnej: {}'.format(d1))

    if sum([graph[0][i] - graphUsed[0][i] for i in range(n)]) + sum([graph[i][-1] - graphUsed[i][-1] for i in range(n)]) != 0:
        print('\033[91mNie istnieje poprawnego dopuszczalnego rozwiazania w tej sieci, poniewaz nie wszystkie luki nasycone\033[0m')
        return d1
    
    n -= 2
    newGraph = []
    for i in range(n):
        newGraph.append([0] * (n))
        for x in range(n):
            newGraph[i][x] = graphLowerBound[i][x] + graphUsed[i + 1][x + 1]
    newGraph[-1][0] = 0

    print('\nWartosci \033[92mmin + przeplyw\033[0m w grafie po sieci gorno-dolnej: \033[91m')
    for i in range(n):
        print('{}\t'.format(nodeNames[i + 1]), end='')
    print('\033[0m\033[92m')

    for i in range(n):
        for x in range(n):
            print('{}\t'.format(newGraph[i][x]), end='')
        print('\033[0m\033[91m{}\033[0m\033[92m'.format(nodeNames[i + 1]))
    print('\033[0m')
    
    for i in range(n):
        for x in range(n):
            newGraph[i][x] = graphUpperBound[i][x] - newGraph[i][x]

    print('Nowy \033[92mmax - (min + przeplyw)\033[0m graf po sieci gorno-dolnej: \033[91m')
    for i in range(n):
        print('{}\t'.format(nodeNames[i + 1]), end='')
    print('\033[0m\033[92m')

    for i in range(n):
        for x in range(n):
            print('{}\t'.format(newGraph[i][x]), end='')
        print('\033[0m\033[91m{}\033[0m\033[92m'.format(nodeNames[i + 1]))
    print('\033[0m')
    
    graphUsed = []
    for i in range(n):
        graphUsed.append([0] * n)
 
    d2 = dinic(0, n - 1, newGraph, graphUsed, nodePriority[1:-1], nodeNames[1:-1])
    print('Delta z drugiej sieci: {}\n'.format(d2))


myNodeNames = ['s', '2', '3', '4', '5', 't']
#             s  2  3  4  t
myPriority = [0, 1, 2, 3, 4, -1]
myGraphLowerBound = [
# to:s  1  2  3  4  t     from
    [0, 2, 3, 0, 0, 0], # s
    [0, 0, 0, 1, 1, 0], # 1
    [0, 0, 0, 1, 0, 2], # 2
    [0, 0, 0, 0, 3, 0], # 3
    [0, 0, 0, 0, 0, 1], # 4
    [0, 0, 0, 0, 0, 0]  # t
]
myGraphUpperBound = [
# to:s  1  2  3  4  t     from
    [0, 6, 5, 0, 0, 0], # s
    [0, 0, 0, 2, 3, 0], # 1
    [0, 0, 0, 5, 0, 4], # 2
    [0, 0, 0, 0, 5, 0], # 3
    [0, 0, 0, 0, 0, 4], # 4
    [0, 0, 0, 0, 0, 0]  # t
]
upperlower(0, len(myGraphLowerBound) - 1, myGraphLowerBound, myGraphUpperBound, myPriority, myNodeNames)