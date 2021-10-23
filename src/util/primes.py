import random

def erastotenes(n=1000):
    sieve = [True for _ in range(n)]
    sieve[0] = sieve[1] = False
    primes = []

    for i in range(2, n):
        if not sieve[i]:
            continue

        primes.append(i)
        for j in range(i, n, i):
            sieve[j] = False

    return primes

def miller_rabin(n, rounds=20):
    def probably_prime(n, r):
        e = n-1
        while e & 1 == 0:
            e >>= 1
        
        if pow(r, e, n) == 1:
            return True

        while e < n - 1:
            if pow(r, e, n) == n-1:
                return True

            e <<= 1

        return False
        
    for _ in range(rounds):
        r = random.randrange(2, n-1)
        if not probably_prime(n, r):
            return False

    return True

def generate_prime_number(size=1024):
    prime_numbers = erastotenes()
    n = 0
    while True:
        n = random.randrange(1 << (size-1), (1 << size)-1)
        divisible = False
        for prime in prime_numbers:
            if n%prime == 0:
                divisible = True
                break
        
        if not divisible and miller_rabin(n):
            break

    return n
