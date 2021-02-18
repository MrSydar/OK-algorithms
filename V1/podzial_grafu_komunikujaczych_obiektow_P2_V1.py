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

def tasking2Processors(w: list, c: list):
    n = len(w) + 2

    graph = []
    for i in range(n):
        graph.append([0] * n)
    
    for i in range(n - 2):
        graph[0][i + 1] = w[i][1]
        graph[i + 1][-1] = w[i][0]
    
    for connection in c:
        graph[connection[0] + 1][connection[1] + 1] = connection[2]

    nodePriority = [0] + [i for i in range(n - 2)] + [-1]
    nodeNames = ['P1'] + ['T{}'.format(i) for i in range(1, n - 1)] + ['P2']
    
    graphUsed = []
    for i in range(n):
        graphUsed.append([0] * n)
    
    print('GRAF:\033[91m')
    for i in range(n):
        print('{}\t'.format(nodeNames[i]), end='')
    print('\033[0m')

    for i in range(n):
        for x in range(n):
            print('{}\t'.format(graph[i][x]), end='')
        print('\033[91m{}\033[0m'.format(nodeNames[i]))
    print()

    delta = dinic(0, n - 1, graph, graphUsed, nodePriority, nodeNames)
    print('Delta: {}\033[92m\n'.format(delta))

    print('WYKORZYSTANO:\033[91m')
    for i in range(n):
        print('{}\t'.format(nodeNames[i]), end='')
    print('\033[0m')

    for i in range(n):
        for x in range(n):
            print('{}\t'.format(graphUsed[i][x]), end='')
        print('\033[91m{}\033[0m'.format(nodeNames[i]))
    print()

    print('Solution: ')
    for i in range(1, n - 1):
        if graph[i][-1] - graphUsed[i][-1] == 0:
            print('T{} -> P1'.format(i))
        elif graph[0][i] - graphUsed[0][i] == 0:
            print('T{} -> P2'.format(i))
        else:
            print('\033[91mProgram is not working correctly or has a bug (there are not satisfied lines for T{}), please solve this task manually ;(\033[92m'.format(i))
    print('\033[0m')

#####################################################################################

W = [
#   P1  P2
    [3, 5], #T1
    [8, 2], #T2
    [4, 11],#T3
    [1, 9],#T4
    [7, 6] #T5
]

# indexes from ZERO !
C = [
#   Ta  Tb  cValue
    [0, 1, 2],  #C1,2=1 (T1 -> T2 = 1)
    [1, 0, 2],
    [1, 2, 3],
    [2, 1, 3],
    [2, 3, 1],
    [3, 2, 1],
    [3, 4, 4],
    [4, 3, 4]
]

tasking2Processors(W, C)