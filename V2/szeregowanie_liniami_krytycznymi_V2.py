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

def dinic(fromNode: int, toNode: int, graph: list, graphUsed: list, nodePriority: list, nodeNames: list):
    n = len(graph)
    
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

            return deltaSum

def color(val: int):
    if val >= 0:
        return '\u001b[4'+str(val % 8)+'m '+str(val+1)+' \u001b[0m'
    return '   '

def taskingFull(n: int, r: list, d: list, p: list, procNum: list):
    tmp = [p[i] + r[i] - d[i] for i in range(n)]
    Lmax = max(tmp)
    print('1.\n Lmax ≥ max({}) = {}'.format(tmp, Lmax))
    
    print('2.')
    tmp = set()
    for i in range(n):
        tmp1 = [r[i] - d[j] for j in range(n) if j != i]
        for j in range(n - 1):
            tmp.add(tmp1[j])
        print(' r{}-dj = {}'.format(i, tmp1))
    tmp = sorted(tmp)
    
    print(' ', end='')
    for i in range(len(tmp) + 1):
        print('({}, {}]'.format(tmp[i - 1] if i != 0 else '-∞', tmp[i] if i != len(tmp) else '+∞'), end='')
    print()

    if max(tmp) > Lmax:
        print('\033[91mLmax is in ranges, I don\'t know what to do in this situation :( ! SOLUTION MAY BE BAD !\033[92m')
    print(' L ∈ {}'.format(Lmax))

    print('3.')
    d = [d[i] + Lmax for i in range(n)]
    print(' New deadlines: d\'={}'.format(d))
    e = sorted(set(r + d))
    print(' Events: e={}'.format(e))

    print('4. ')
    m = 1 + n + len(e)
    graph = []
    for i in range(m):
        graph.append([0] * m)
    
    nodeNames = ['s'] + ['T{}'.format(i + 1) for i in range(n)] + ['[{}, {}]'.format(e[i], e[i+1]) for i in range(len(e) - 1)] + ['t']
    nodePriority = [i for i in range(m - 1)] + [-1]

    intervalLengths = [e[i+1] - e[i] for i in range(len(e) - 1)]
    for t in range(n):
        graph[0][t + 1] = p[t]

        for j in range(len(e) - 1):
            if r[t] < e[j + 1] and e[j] < d[t]:
                graph[t + 1][n + 1 + j] = e[j + 1] - e[j]
            
    for i in range(len(e) - 1):
        graph[1 + n + i][-1] = procNum * (e[i + 1] - e[i])


    print('GRAF:\033[91m')
    for i in range(m):
        print('{}\t'.format(nodeNames[i]), end='')
    print('\033[0m')

    for i in range(m):
        for x in range(m):
            print('{}\t'.format(graph[i][x]), end='')
        print('\033[91m{}\033[0m'.format(nodeNames[i]))
    print()

    graphUsed = []
    for i in range(m):
        graphUsed.append([0] * m)

    delta = dinic(0, m - 1, graph, graphUsed, nodePriority, nodeNames)

    print('WYKORZYSTANO:\033[91m')
    for i in range(m):
        print('{}\t'.format(nodeNames[i]), end='')
    print('\033[0m')

    for i in range(m):
        for x in range(m):
            print('{}\t'.format(graphUsed[i][x]), end='')
        print('\033[91m{}\033[0m'.format(nodeNames[i]))
    print()

    print('Delta = {}'.format(delta))

    if sum([graph[0][i] - graphUsed[0][i] for i in range(m)]) > 0:
        print('\033[91m Rozwiazania dla tego problemu nie istnieje! \033[0m')
        exit()
    
    solution = []
    for i in range(procNum):
        solution.append([-1] * (max(e) - min(e)))
    
    for t in range(n):
        for rg in range(m - (2 + n)):
            for i in range(graphUsed[t + 1][1 + n + rg]):
                proc = 0
                shift = 0
                while True:
                    if solution[proc][e[rg] + shift] == -1:
                        solution[proc][e[rg] + shift] = t
                        break
                    elif e[rg] + shift < e[rg + 1] - 1:
                        shift += 1
                    else:
                        proc += 1
                        shift = 0
    
    for row in range(len(solution)):
        print('M{}'.format(row+1),end='')
        for x in range(len(solution[0])):
            print(color(solution[row][x]),end = '')
        print()

    for i in range(min(e), max(e)):
        print('  {}'.format(i), end='')
    print()



# ilosc procesorow
M = 3
# ilosc zadan
N = 4
# momenty gotowosci
R = [0, 1, 1, 2]
# deadlines
D = [3, 3, 5, 4]
# czas trwanie
P = [3, 2, 4, 4]

taskingFull(N, R, D, P, M)
