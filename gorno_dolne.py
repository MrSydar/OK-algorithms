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
            return deltaSum

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

    print('NEW GRAPH:\033[91m')
    for i in range(n):
        print('{}\t'.format(nodeNames[i]), end='')
    print('\033[0m')

    for i in range(n):
        for x in range(n):
            print('{}\t'.format(graph[i][x]), end='')
        print('\033[91m{}\033[0m'.format(nodeNames[i]))

    return dinic(0, n - 1, graph, nodePriority, nodeNames)



myNodeNames = ['s', 'A', 'B', 't']
#             s  A  B  t
myPriority = [0, 1, 2, -1]
myGraphLowerBound = [
# fr:s  A  B  t     to
    [0, 0, 1, 0], # s
    [0, 0, 0, 2], # A
    [0, 0, 0, 2], # B
    [0, 0, 0, 0]  # t
]
myGraphUpperBound = [
# fr:s  A  B  t     to
    [0, 1, 2, 0], # s
    [0, 0, 0, 3], # A
    [0, 0, 0, 3], # B
    [0, 0, 0, 0]  # t
]

myDeltaSum = upperlower(0, 3, myGraphLowerBound, myGraphUpperBound, myPriority, myNodeNames)
print('Max flow is {}'.format(myDeltaSum))