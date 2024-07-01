import numpy as np
from utils import *
from binary import *
import hashlib

def func(x):
    if x >= 1000:
        x = (x - 1000) * (-1)
    return x

def asym_key(id, pw, n, q, bound, A_size, B_size, sk_size):
# def asym_key(id, n, q, bound):
    A = [[0 for _ in range(n)] for _ in range(n)]
    # A = np.zeros((n,n), dtype=np.int16)
    k=0

    for i in range(n):
        for j in range(n):
            A[i][j] = int(ord(id[k]))
            k += 1

    sk_text = id + pw
    sha224 = hashlib.sha224()
    sha224.update(sk_text.encode('utf-8'))
    hash_dig = sha224.hexdigest()
    sk = [0, 0, 0]
    for i in range(3):
        sk[i] = hash_dig[i*5 : (i+1)*5]
        sk[i] = int(sk[i], 16)
        sk[i] %= 2000
        sk[i] = func(sk[i])

    # sk = sample_bounded_vector(n, 1000)
    # sk = [434, 831, 425]
    # sk = sample_uniform_vector(n, q)
    print("sk: ", sk)
    sk_binary = sk_to_binary(sk, sk_size)

    As = matrix_vector_multiplication(A, sk, q) # As = A * s
    e = sample_bounded_vector(n, bound)
    B = vector_vector_addition(As, e, q) # B = A  * s + e
    print("A: ", A)
    print("B: ", B)
    A_binary = A_to_binary(A, A_size)
    B_binary = B_to_binary(B, B_size)
    pk = (A_binary, B_binary)
    pk = A_binary + B_binary
    # pk = (A, B)
    return (pk, sk_binary)
    # return (pk, sk)

def symm_key(n, q):
    s = sample_uniform_vector(n, q)
    return s