def printFloydMatrix(i: int, matrix: list):
    print('{}.'.format(i))
    for j in range(len(matrix)):
        for k in range(len(matrix)):
            if j == i or k == i:
                print('\033[91m{}\033[0m\t'.format('-' if matrix[j][k] is None else matrix[j][k]), end='')
            else: 
                print('{}\t'.format('-' if matrix[j][k] is None else matrix[j][k]), end='')
        print()
    print('\n')

def floyd(i: int, matrix: list):
    if i >= len(matrix):
        return
    
    for horizontal in range(len(matrix)):
        for vertical in range(len(matrix)):
            if vertical != horizontal:
                if not (matrix[horizontal][i] is None) and not (matrix[i][vertical] is None):
                    if matrix[horizontal][vertical] is None:
                        matrix[horizontal][vertical] = matrix[horizontal][i] + matrix[i][vertical]
                    else:
                        val = min(matrix[horizontal][i] + matrix[i][vertical], matrix[horizontal][vertical])
                        if val != -1:
                            matrix[horizontal][vertical] = val
    printFloydMatrix(i, matrix)
    floyd(i+1, matrix)

_ = None
# change matrix and go
matrix = [
    [ 0, 5, _, 2, _, _],
    [ _, 0, 3, _, _, 1],
    [ 8, _, 0, _, 2, _],
    [ _, _, 5, 0, _, 2],
    [ _, 6, _, 3, 0, _],
    [ 9, _, _, _, 1, 0]
]

floyd(0, matrix)