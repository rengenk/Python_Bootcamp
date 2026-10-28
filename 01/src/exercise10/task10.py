def get_min_cost(arr, hour):
    year_group = {}
    for year, cost, time in arr:
        if year not in year_group:
            year_group[year] = []
        year_group[year].append((cost, time))

    min_cost = float('inf')
    for year, param in year_group.items():
        if len(param) < 2:
            continue

        for i in range(len(param)):
            for j in range(i + 1, len(param)):
                total_cost = param[i][0] + param[j][0]
                total_time = param[i][1] + param[j][1]

                if total_time == hour and total_cost < min_cost:
                    min_cost = total_cost

    return min_cost

def main():
    try:
        amount, required = map(int, input().split())
        if amount < 2:
            print("Error")
            return
        arr = []
        for i in range(amount):
            row = list(map(int, input().split()))
            if len(row) != 3:
                print("Error")
                return
            year, cost, time = row
            arr.append((year, cost, time))
        print(get_min_cost(arr, required))
    except ValueError:
        print("Error: Invalid input")
main()