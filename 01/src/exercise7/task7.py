def robot(arr, rows, cols):
    coins = [[0] * cols for _ in range(rows)]
    coins[0][0] = arr[0][0]

    for i in range(1, rows):
        coins[i][0] = coins[i-1][0] + arr[i][0]

    for j in range(1, cols):
        coins[0][j] = coins[0][j - 1] + arr[0][j]

    for i in range(1, rows):
        for j in range(1, cols):
            coins[i][j] = max(coins[i - 1][j], coins[i][j - 1]) + arr[i][j]


    return coins[-1][-1]

def main():
    data = list(map(int, input().split()))
    n, m = data[0], data[1]
    arr = []
    for i in range(n):
        row = list(map(int, input().split()))
        arr.append(row)
    print(robot(arr, n, m))
main()