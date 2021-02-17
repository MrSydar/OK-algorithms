def plecak2(b: int, w: list, p: list):
    table = [[0 for x in range(b + 1)] for x1 in range(len(w) + 1)]
    
    for i in range(1, len(w) + 1):
        for j in range(1, b + 1):
            table[i][j] = table[i-1][j] if w[i - 1] > j else max(table[i - 1][j], table[i - 1][j - w[i - 1]] + p[i - 1])

    sack = []
    backTrack(len(table) - 1, len(table[0]) - 1, table, w, sack)

    printTable(table)
    print(sack)

def backTrack(i: int, j: int, table: list, w: list, sack: list):
    if i - 1 < 0:
        return
    elif table[i][j] == table[i-1][j]:
        backTrack(i - 1, j, table, w, sack)
    else:
        sack.append(i)
        table[i][j] *= -1
        backTrack(i - 1, j - w[i - 1], table, w, sack)

def printTable(table: list):
    print('\033[94m'+'i\\j\t', end='')
    for j in range(len(table[0])):
        print('{}\t'.format(j), end='')
    print('\033[0m')
    for i in range(len(table)):
        print('\033[94m'+'{}\t'.format(i)+'\033[0m', end='')
        for j in range(len(table[0])):
            print('\033[91m'+'{} \t'.format(table[i][j]*-1)+'\033[0m' if table[i][j] < -1 else '{} \t'.format(table[i][j]), end='')
        print()

B = 8           #rozmiar plecaka
W = [2,1,4,4]  #rozmiary
P = [4,3,6,8]  #wartosci

plecak2(B, W, P)
