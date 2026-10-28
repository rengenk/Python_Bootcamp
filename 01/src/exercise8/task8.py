amount = int(input())
unique = set()

for i in range(amount):
    number = int(input())
    unique.add(number)
print(len(unique))