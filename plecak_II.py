#-1 is infinity

class plecak:
    def infSum(self, a: int, b: int):
        if a < 0 or b < 0:
            return -1
        else:
            return a + b

    def infMin(self, a: int, b: int):
        if a < 0 and b < 0:
            return -1
        elif a < 0:
            return b
        elif b < 0:
            return a
        elif a > b:
            return b
        else:
            return a

    def getVal(self, table: list, i: int, j: int, w: list, s: list):
        if w[i - 1] > j:
            table[i][j] = table[i - 1][j]
        else:
            table[i][j] = self.infMin(
                table[i - 1][j], 
                self.infSum(
                    table[i - 1][j - w[i - 1]], 
                    s[i - 1]
                    )
                )

    def plecak2(self, b: int, w: list, s: list):
        table = [[0] + [-1] * (sum(w))]
        
        for i in range(1, len(w) + 1):
            table += [[0] * (sum(w) + 1)]
            for j in range(1, sum(w) + 1):
                self.getVal(table, i, j, w, s)

        j = len(table[0]) - 1
        while table[-1][j] > b:
            j -= 1
        sack = []
        self.backTrack(len(table) - 1, j, table, w, sack)

        self.printTable(table)
        print(sack)

    def backTrack(self, i: int, j: int, table: list, w: list, sack: list):
        if i - 1 < 0:
            return
        elif table[i][j] == table[i-1][j]:
            self.backTrack(i - 1, j, table, w, sack)
        else:
            sack.append(i)
            table[i][j] *= -1
            self.backTrack(i - 1, j - w[i - 1], table, w, sack)

    def printTable(self, table: list):
        print('\033[94m'+'i\\j\t', end='')
        for j in range(len(table[0])):
            print('{}\t'.format(j), end='')
        print('\033[0m')
        for i in range(len(table)):
            print('\033[94m'+'{}\t'.format(i)+'\033[0m', end='')
            for j in range(len(table[0])):
                print('∞ \t' if table[i][j] == -1 else '\033[91m'+'{} \t'.format(table[i][j]*-1)+'\033[0m' if table[i][j] < -1 else '{} \t'.format(table[i][j]), end='')
            print()

    def __init__(self, B, W, S):
        self.B = B
        self.W = W
        self.S = S
    
    def solve(self):
        self.plecak2(B,W,S)
    
B = 8           #rozmiar plecaka
W = [3,4,2,6,1]  #wartosci
S = [5,3,2,4,3]  #rozmiary

p = plecak(B, W, S)
p.solve()