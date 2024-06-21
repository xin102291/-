# asym.py
import random
from utils import *

# 傳訊
class LWEAsymmetric:
    def __init__(self, n, q, B, scale):
        self.n = n
        self.q = q
        self.B = B
        self.scale = scale

    def encrypt(self, m, pk):
        (A, b) = pk[0], pk[1]
        r = sample_bounded_vector(self.n, self.B)
        e2 = sample_bounded_vector(self.n, self.B)
        e3 = sample_bounded_vector(1, self.B)[0]
        At = matrix_transpose(A)
        u = matrix_vector_multiplication(At, r, self.q)
        u = vector_vector_addition(u, e2, self.q)
        rAs = vector_vector_inner_product(r, b, self.q)
        rAs = (rAs + e3) % self.q
        m = m * (self.q//self.scale)
        c = (rAs + m) % self.q
        return (u, c)
    
    def decrypt(self, ctx, s):
        (u, c) = ctx[0], ctx[1]
        rAs = vector_vector_inner_product(u, s, self.q)
        m = (c - rAs) % self.q
        p = round(m / (self.q // self.scale)) % self.scale
        return p

# 身分驗證
class authentication:
    def __init__(self, n, q, B, scale):
        self.n = n
        self.q = q
        self.B = B
        self.scale = scale

    def encrypt(self, m, pk, sk):
        (A, b) = pk[0], pk[1]
        r = sample_bounded_vector(self.n, self.B)
        e2 = sample_bounded_vector(self.n, self.B)
        e3 = sample_bounded_vector(1, self.B)[0]
        At = matrix_transpose(A)
        rAs = matrix_vector_multiplication(At, r, self.q)
        rAs = vector_vector_addition(rAs, e2, self.q)
        rAs = vector_vector_inner_product(rAs, sk, self.q)
        rAs = (rAs + e3) % self.q
        m = m * (self.q // self.scale) % self.q
        c = (rAs + m) % self.q
        return (r, c)
    
    def decrypt(self, ctx, pk):
        (r, c) = ctx[0], ctx[1]
        # print('r: ')
        # print(r)
        # print('c')
        # print(c)
        (A, b) = pk[0], pk[1]
        # print('b: ')
        # print(b)
        rAs = vector_vector_inner_product(r, b, self.q)
        m = (c - rAs) % self.q
        p = round(m / (self.q // self.scale)) % self.scale
        return p