def get_number():
    try:
        return int(input())
    except ValueError:
        return None

def next_row(row):
    new_row = [1]
    for j in range(len(row) - 1):
        new_row.append(row[j] + row[j + 1])
    new_row.append(1)
    return new_row

def pascal_triangle(n):
    row = [1]
    for i in range(n):
        print(*row)
        row = next_row(row)

def main():
    n = get_number()
    if n is None or n <= 0:
        print("Natural number was expected")
    else:
        pascal_triangle(n)

main()