def greedy(b, w, s):
    items = [[s[i], w[i]] for i in range(len(w))]

    for i in range(len(items)):
        items[i].append(i+1)

    items = sorted(items, key = lambda item: item[1]/item[0], reverse=True)

    print("Reordered items: ")
    for item in items:
        print("ID: {}, SIZE: {}, VALUE: {}, Wi/Si: {}".format(item[2], item[0], item[1], item[1]/item[0]))

    knapsack = []
    i = 0
    while b - items[i][0] >= 0:
        b -= items[i][0]
        knapsack.append(items[i])
        i += 1

    if b != 0:
        items[i][1] = items[i][1] * b / items[i][0]
        items[i][0] = b
        knapsack.append(items[i])

    print("Knapsack value: \u001b[32m{}\u001b[0m".format(sum(x[1] for x in knapsack)))
    print("Items in knapsack: ")
    for item in knapsack:
        print("ID: {}, SIZE: {}, VALUE: {}".format(item[2], item[0], item[1]))

# knapsack size
B = 10
W = [2, 2, 4, 9, 8, 1, 6, 7, 6]     #value
S = [4, 5, 5, 7, 5, 1, 5, 5, 4]     #size

greedy(B, W, S)