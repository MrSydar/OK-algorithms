from copy import deepcopy

def initColors(graph: list):
    n = len(graph)
    colors = [-1] * n
    for v in range(n):
        badColors = []
        for v2 in range(n):
            if graph[v][v2] == 1:
                badColors.append(colors[v2])
        c = 1
        while c in badColors:
            c += 1
        colors[v] = c
    return colors

def forward(v: int, graph: list, actualColors: list, usedColors: list, ub: int):
    if v == len(graph):
        return True
    
    c = 1
    if v == 4:
        print('lakaka')
    while c < ub:
        print('Color: {}'.format(c))
        bad = False
        for v2 in range(len(graph)):
            if graph[v][v2] == 1 and c == actualColors[v2] or c in usedColors[v]:
                bad = True
                break
        if bad:
            c += 1
        else:
            actualColorsCopy = deepcopy(actualColors)
            actualColorsCopy[v] = c
            if forward(v + 1, graph, deepcopy(actualColors), usedColors, ub):
                actualColors[v] = c
                usedColors[v].append(c)
                return True
            else:
                c += 1
    return False

def brown(graph: list):
    colors = initColors(graph)
    usedColors = [[c] for c in colors]
    ub = max(colors)
    
    print(colors)
    
    v = 0
    for vi in range(len(graph)):
        if colors[vi] == ub:
            v = vi
            for vi2 in range(vi, len(graph)):
                colors[vi2] = 0
    
    toPrint = deepcopy(colors)
    while v != 0:
        if forward(v, graph, colors, usedColors, ub):
            ub = max(colors)
            v = 0
            for vi in range(len(graph)):
                if colors[vi] == ub:
                    v = vi
                    for vi2 in range(vi, len(graph)):
                        colors[vi2] = 0
        else:
            colors[v] = 0
            v -= 1
        print(colors)

########################################################

# myNames = ['A','B','C','D','E','F']
# myGraph = [
# #    A B C D E F
#     [0,1,0,1,1,1],# A
#     [1,0,0,1,0,1],# B
#     [0,0,0,1,0,0],# C
#     [1,1,1,0,0,0],# D
#     [1,0,0,0,0,1],# E
#     [1,1,0,0,1,0] # F
# ]

myNames = ['1','2','3','4','5','6']
myGraph = [
#    1 2 3 4 5 6
    [0,1,1,0,0,0],# 1
    [1,0,1,1,1,0],# 2
    [1,1,0,0,1,1],# 3
    [0,1,0,0,1,0],# 4
    [0,1,1,1,0,1],# 5
    [0,0,1,0,1,0] # 6
]

brown(myGraph)