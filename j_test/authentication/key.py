import numpy as np
from utils import *
from binary import *

def asym_key(id, n, q, bound, A_size, B_size, sk_size):
    A = [[0 for _ in range(n)] for _ in range(n)]
    # A = np.zeros((n,n), dtype=np.int16)
    k=0

    for i in range(n):
        for j in range(n): 
            A[i][j] = int(ord(id[k]))
            k += 1

    sk = sample_bounded_vector(n, bound)
    print("sk: ", sk)
    sk_binary = sk_to_binary(sk, sk_size)

    As = matrix_vector_multiplication(A, sk, q) # As = A * s
    e = sample_bounded_vector(n, bound)
    B = vector_vector_addition(As, e, q) # B = A  * s + e
    print("A: ", A)
    print("B: ", B)
    A_binary = A_to_binary(A, A_size)
    B_binary = B_to_binary(B, B_size)
    # pk = (A_binary, B_binary)
    pk = A_binary + B_binary
    return (pk, sk_binary)

def symm_key(n, q):
    s = sample_uniform_vector(n, q)
    return s