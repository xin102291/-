# symm.py

import random
from utils import *
import numpy as np

class LEWSymmetric:
    def __init__(self, n, q, B, scale):
        self.n = n
        self.q = q
        self.B = B
        self.scale = scale

    def encrypt(self, s, m):
        A = sample_uniform_matrix(self.n, self.q)
        b = matrix_vector_multiplication(A, s, self.q) #As
        e = sample_bounded_vector(self.n, self.B)
        b = vector_vector_addition(b, e, self.q)
        scale_m = [self.q // self.scale * m[i] % self.q for i in range(self.n)]
        c = vector_vector_addition(b, scale_m, self.q)
        text_A = ""
        for i in range(self.n):
            for j in range(self.n):
                text_A += "%03d" % A[i][j]
        text_c = ""
        for i in c:
            text_c += "%03d" % i
        text = text_A + text_c
        return(text)
    
    def decrypt(self, s, ctx):
        j=0
        k=0
        n = self.n
        text_A = ctx[0 : 3 * n * n]
        text_c = ctx[3 * n * n : len(ctx)]
        A = np.zeros((self.n, self.n), dtype=np.int16)
        c = np.zeros((self.n), dtype=np.int16)

        for i in range(0, 3 * n * n, 3):
            A[j][k] = int(text_A[i] + text_A[i+1] + text_A[i+2])
            k += 1
            if(k == 10):
                k = 0
                j +=1

        for i in range(0, n):
            c[i] = int(text_c[3 * i] + text_c[3 * i + 1] + text_c[3 * i + 2])



        As = matrix_vector_multiplication(A, s, self.q)
        b = [(c[i] - As[i]) % self.q for i in range(self.n)]
        m = [round(b[i] / (self.q//self.scale)) % self.scale for i in range(self.n)]
        return m