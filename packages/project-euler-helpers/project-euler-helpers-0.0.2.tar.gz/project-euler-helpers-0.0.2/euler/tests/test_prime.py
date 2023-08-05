from os import confstr
from euler.prime import is_prime, next_prime, prime_factorize
import random


def test_is_prime():
    primes = [2, 3, 5, 7, 11, 13, 41, 43, 47, 53, 59, 61, 67, 71,  83, 89, 97,
              101, 103, 107, 139,  167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419,  479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 907, 911, 919, 929, 967, 971, 977, 983, 991, 997, 1179973, 1179977, 1179979, 1179989, 1179991, 1180009, 1180013, 1180019, 1180027]

    non_primes = [0, 1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, 32,
                  33, 34, 35, 36, 38, 39, 40, 42, 44, 45, 46, 48, 49, 50, 51, 52, 54, 55, 56, 57, 58, 60, 62, 63]

    for num in primes:
        assert is_prime(num)

    for num in non_primes:
        assert not is_prime(num)


def test_next_prime():
    series = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
              101, 103, 107]
    desired = 2
    for i in series:
        assert i == desired
        desired = next_prime(desired)


def test_prime_factorize():
    for i in range(100):
        construct = 1
        num = random.randint(100, 10000)
        factors = prime_factorize(num)
        for factor, power in factors.items():
            construct *= factor**power
        assert num == construct
