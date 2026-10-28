n, x = map(float, input().split())
n = int(n)

coef = []
for _ in range(n):
    num = float(input())
    coef.append(num)
coef.reverse()
free = float(input())

result = 0.0
for i in range(1, n + 1):
    result += i * coef[i - 1] * (x ** (i - 1))
print(f"{result:.3f}")