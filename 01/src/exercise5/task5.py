def parse_number(s):
    if not s:
        raise ValueError
    sign = 1
    start = 0
    if s[0] == '-':
        sign = -1
        start = 1
    elif s[0] == '+':
        start = 1
    if start == len(s):
        raise ValueError
    s = s[start:]
    if s.count('.') > 1:
        raise ValueError
    parts = s.split('.')
    if len(parts) == 1:
        integer_part = parts[0]
        fractional_part = ''
    else:
        integer_part = parts[0]
        fractional_part = parts[1]
        
    if not integer_part and not fractional_part:
        raise ValueError
    if integer_part and not all('0' <= c <= '9' for c in integer_part):
        raise ValueError
    if fractional_part and not all('0' <= c <= '9' for c in fractional_part):
        raise ValueError

    return sign, integer_part, fractional_part

def convert_to_number(integer_part, fractional_part):
    integer_value = 0
    for c in integer_part:
        integer_value = integer_value * 10 + (ord(c) - ord('0'))
    fractional_value = 0.0
    divisor = 10.0
    for c in fractional_part:
        fractional_value += (ord(c) - ord('0')) / divisor
        divisor *= 10
    return integer_value + fractional_value

def main():
    s = input().strip()
    try:
        sign, integer_part, fractional_part = parse_number(s)
        number = convert_to_number(integer_part, fractional_part)
        number *= sign
        print(f"{number * 2:.3f}")
    except (ValueError, OverflowError):
        print("Invalid input")

main()