n = int(input("Enter number: "))

if n < 0:
    print(False)
else:
    orig = n
    reversed = 0

    while n > 0:
        reversed = reversed * 10 + n % 10
        n //= 10

    print(orig == reversed)