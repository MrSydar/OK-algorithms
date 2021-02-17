def printSolution(graph: list, names: list):
    for i in range(n):
        for j in range(n):
            if graph[i][j] == 1:
                print('\033[94m' + names[i] + '\033[91m -> \033[94m' + names[j] + '\033[0m')
                break

def hopkroft_karp(graph: list, names: list):
    n = len(graph)
    visitedGraph = [[0] * n for i in n]

    added = [False] * n
    for i in range(n):
        for j in range(n):
            if graph[i][j] == 1:
                visitedGraph[i][j] = 1
                added[i] = True
            break
    
    if all(added):
        printSolution(graph, names)
        return
    
    
    

# WORK IN PROGRESS ...    

graph = [
#to  1 2 3 4   from
    [1,0,0,1],#A
    [1,0,0,1],#B
    [0,1,1,0],#C
    [0,1,1,1] #D
]