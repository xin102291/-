from utils import *
from binary import *

class authentication:
    def __init__(self, n, q, bound, scale, A_size, B_size, sk_size):
        self.n = n
        self.q = q
        self.bound = bound
        self.scale = scale
        self.A_size = A_size
        self.B_size = B_size
        self.sk_size = sk_size

    def encrypt(self, m, pk, sk_binary):
        A_binary = pk[:self.A_size*9]
        # B_binary = pk[self.A_size*9:]
        A = binary_to_A(A_binary, self.A_size)
        sk = binary_to_sk(sk_binary, self.sk_size)
        # print("A enc: ", A)
        # print(type(A[0]))
        # B = binary_to_B(B_binary)
        # (A, B) = pk[0], pk[1]
        r = sample_bounded_vector(self.n, self.bound)
        e2 = sample_bounded_vector(self.n, self.bound)
        e3 = sample_bounded_vector(1, self.bound)[0]
        At = matrix_transpose(A)
        rAs = matrix_vector_multiplication(At, r, self.q)
        rAs = vector_vector_addition(rAs, e2, self.q)
        # print(type(rAs), " ", type(sk))
        rAs = vector_vector_inner_product(rAs, sk, self.q)
        rAs = (rAs + e3) % self.q
        m = m * (self.q // self.scale) % self.q
        c = (rAs + m) % self.q
        # print("C: ", c)
        # c_tmp = c
        r_binary = sk_to_binary(r, 8)
        c_binary = decimal_to_binary(c, self.B_size)
        # c1 = [0 for _ in range(9)]
        # for i in range(9):
        #     c1[8-i] = c_tmp % 10
        #     c_tmp //= 10
        # for i in range(9):
        #     c_binary += decimal_to_binary(c1[i], 8)
        text = r_binary + c_binary
        return (text)
    
    def decrypt(self, ctx, pk):
        r_binary = ctx[:self.sk_size*3]
        c_binary = ctx[self.sk_size*3:]
        r = binary_to_sk(r_binary, self.sk_size)

        c = binary_to_decimal(c_binary)

        # c_block = split_binary(c_binary, 8)
        # c_decimal = [binary_to_decimal(_) for _ in c_block]
        # c = digit_numbers(c_decimal, 9)[0]


        # (A, B) = pk[0], pk[1]
        B_binary = pk[self.A_size*9:]
        B = binary_to_B(B_binary, self.B_size)
        rAs = vector_vector_inner_product(r, B, self.q)
        m = (c - rAs) % self.q
        p = round(m / (self.q // self.scale)) % self.scale
        return p