

def gcd(a, b):
    result = 0
    while b != 0:
        result = b
        a, b = b, a % b
    return result

print("GCD: {}".format(gcd(20000, 775)))


def fib_generator():
    a, b = 0, 1
    while True:
        yield b
        a, b = b, a+b

fibg = fib_generator()
print("Fibo generator:", fibg.__next__(), fibg.__next__(), fibg.__next__(), fibg.__next__(), fibg.__next__())


# nth element in fibonacci
def fib(n):
    if n < 3:
        return 1
    a, b = 0, 1
    count = 1
    while count < n:
        a, b = b, a+b
        count += 1
    return b

print("10th Fibo num: {}".format(fib(10)))


# recursive fibonacci nth element
def fib_rec(n):
    if n < 3:
        return 1
    return fib_rec(n - 1) + fib_rec(n-2)

print("10th Fibo rec: {}".format(fib_rec(10)))


# fibonacci sequence of first n elements
def fib_seq(n):
    seq = [0, 1]
    if n < 3:
        return seq[:n]
    count = 1
    while count < n:
        seq.append(seq[count-1] + seq[count])
        count += 1
    return seq

print("First 10 Fibo seq: {}".format(fib_seq(10)))


def is_prime(n):
    for j in range(2, int(n**(1/2)+1)):
        if n % j == 0:
            return False
    return True

print("is_prime(13): {}".format(is_prime(113)))


def find_prime_factors(n):
    divisors = [d for d in range(2, n//2 + 1) if n % d == 0]
    primes = [d for d in divisors if is_prime(d)]
    return primes

print("Prime factors of 8802351: {}".format(find_prime_factors(8802351)))


def permutations(lst):
    if len(lst) <= 1:
        return lst
    if len(lst) == 2:
        return [lst, lst[::-1]]
    perms = []
    for i in lst:
        perms.extend([i] + perm for perm in permutations([x for x in lst if x != i]))
    return perms


print("Permutations for [3,1,2]: {}".format(permutations([3, 1, 2])))


def is_palindrome(st):
    st = st.strip()
    if len(st) < 2:
        return True
    if st[0] == st[-1]:
        return is_palindrome(st[1:-1])
    else:
        return False

print("Palindrome subi no onibus : {}".format(is_palindrome('subi no onibus')))


def is_anagram(s1, s2):
    cts = {}
    for c in s1:
        if cts.get(c):
            cts[c] += 1
        else:
            cts[c] = 1
    for c in s2:
        if cts.get(c):
            cts[c] -= 1
        else:
            cts[c] = -1
    for i in cts.values():
        if i != 0:
            return False
    return True

print("Anagrams cat tac:", is_anagram('cat', 'tac'))

# change to use regex also
def grep_from_files(word, files):
    for filename in files:
        with open(filename) as file:
            for lino, line in enumerate(file, start=1):
                if word in line:
                    print("{0}:{1}:{2:.40}".format(filename, lino, line.rstrip()))


grep_from_files('List', ['linkedlist.py', 'others.py'])
