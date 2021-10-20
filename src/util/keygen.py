import random
from .primes import erastotenes
from .primes import miller_rabin

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

def generate():
    p = generate_prime_number()
    q = generate_prime_number()

    n = p*q
    phi = (p-1) * (q-1)
    e = 65537               # TODO: 'e' needs to be coprime with 'phi'

    d = pow(e, -1, phi)     # multiplicative inverse

    public = (n, e)
    private = (d, p, q)

    return public, private
