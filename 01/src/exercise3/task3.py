def readFile(filename):
    with open("input.txt") as f:
        matrix = [list(map(int, line.split())) for line in f]
    return matrix

def is_square(shape, rows, cols):
    rows = [x for x, y in shape]
    cols = [y for x, y in shape]

    area = (max(rows) - min(rows) + 1) * (max(cols) - min(cols) + 1)
    return area == len(shape)

def shapes(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    squares, circles = 0, 0

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 1 and not visited[i][j]:
                shape = []
                queue = [(i, j)]
                visited[i][j] = True

                while queue:
                    x, y = queue.pop(0)
                    shape.append((x, y))

                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols:
                            if matrix[nx][ny] == 1 and not visited[nx][ny]:
                                visited[nx][ny] = True
                                queue.append((nx, ny))
                if is_square(shape, rows, cols):
                    squares += 1
                else:
                    circles += 1
    return squares, circles

matrix = readFile("input.txt")
squares, circles = shapes(matrix)
print(squares, circles)
