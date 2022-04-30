import random

def isprime(num):
    """
    checks whether number is prime
    """
    for i in range(2,int(num**0.5)+1):
        if num % i == 0:
            return False
    return True

def gcd(a, b):
    """
    calculates gcd
    """
    while b != 0:
        a, b = b, a % b
    return a

def coprime(a, b):
    """
    checks wheter two numbers are coprime
    """
    return gcd(a, b) == 1

def euclidean(e, k):
    """
    calculates multiplicative inverses modulo\
    t using extended euclidean algorithm
    """
    x = e
    y = k
    s0 = 1
    s1 = 0
    t0 = 0
    t1 = 1
    while y != 0:
        q, r = x // y, x % y
        x, y = y, r
        s = s0 - q * s1
        t = t0 - q * t1
        s0 = s1
        t0 = t1
        s1 = s
        t1 = t
    return s0

def generate_keys():
    """
    generates public and secret keys
    """
    prime_nums = [num for num in range(10**2) if isprime(num) and num != 0 and num != 1]
    p = random.choice(prime_nums)
    prime_nums.remove(p)
    q = random.choice(prime_nums)
    n = p * q
    t = (p - 1) * (q - 1)
    e = 3
    while not coprime(e, t):
        e += 2
    d = euclidean(e, t)
    if d < 1:
        d += t
    return n, e, d

def encode(message, e, n):
    """
    encodes the message
    """
    message_int = ""
    for letter in message:
        num = ord(letter) - 32
        if num < 10:
            message_int += f"0{num}"
        else:
            message_int += str(num)
    block = ""
    while int(block + "90") <= n:
        block += "90"
    N2 = len(block)
    blocks = []
    if len(block) == 0:
        for element in message_int:
            blocks.append(element)
    else:
        while len(message_int) > 0:
            if len(message_int) > N2:
                blocks.append(message_int[:N2])
            else:
                blocks.append(message_int[:len(message_int)])
            message_int = message_int[N2:]
    end = len(blocks) - 1
    if len(blocks[end]) < N2:
        difference = N2 - len(blocks[end])
        blocks[end] += "0" * difference
        fict_nums = difference
    else:
        fict_nums = 0
    for ind in range(len(blocks)):
        blocks[ind] = str((int(blocks[ind]) ** e) % n)
    to_return = ""
    for element in blocks:
        to_return += f"{element} "
    to_return = to_return[:-1]
    to_return += f"/{N2}/{fict_nums}"
    return to_return

def decode(encoded, d, n, N2, fict_nums):
    """
    decodes the message
    """
    for ind in range(len(encoded)):
        encoded[ind] = str(int(encoded[ind]) ** d % n)
        difference = N2 - len(encoded[ind])
        encoded[ind] = difference * "0" + encoded[ind]
    message = ""
    for element in encoded:
        message += element
    result = ""
    while len(message) > 0:
        letter = message[:2]
        result += chr(int(letter) + 32)
        message = message[2:]
    if fict_nums > 0:
        return result[:-fict_nums]
    return result
