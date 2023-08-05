def is_prime(num):
    '''Returns whether a number is prime or not'''

    if num == 1 or num == 0:
        return False

    prime_is = True
    for i in range(2, (num // 2) + 1):
        if num % i == 0:
            prime_is = False
            break

    return prime_is


def next_prime(num):
    '''Returns the next prime number'''

    next = num + 1
    while not is_prime(next):
        next += 1
    return next


def prime_factorize(num):
    'Returns a dictionary where the key is a prime factor of the given num and the value is the power of that prime factor'
    prime_factors = {}
    p = 1
    while num != 1:
        p = next_prime(p)
        while (num % p == 0):
            num //= p
            if not p in prime_factors.keys():
                prime_factors[p] = 0
            prime_factors[p] += 1
    return prime_factors
