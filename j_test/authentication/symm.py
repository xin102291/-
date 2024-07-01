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
                text_A += "%05d" % A[i][j]
        text_c = ""
        for i in c:
            text_c += "%05d" % i
        text = text_A + text_c
        return(text)
    
    def decrypt(self, s, ctx):
        j=0
        k=0
        n = self.n
        digit = 5
        text_A = ctx[0 : digit * n * n]
        text_c = ctx[digit * n * n : len(ctx)]
        # print("text_c\n",text_c)
        A = [[0 for _ in range(n)] for _ in range(n) ]
        c = [0 for _ in range(n)]

        row = 0
        col = 0
        for i in range(0, len(text_A), digit):
            tmp = ""
            for j in range(digit):
                tmp += text_A[i + j]
            A[row][col] = int(tmp)
            col+=1
            if(col == n):
                col = 0
                row += 1

        col = 0
        for i in range(0, len(text_c), digit):
            tmp = ""
            for j in range(digit):
                tmp += text_c[i + j]
            c[col] = int(tmp)
            col += 1

        As = matrix_vector_multiplication(A, s, self.q)
        b = [(c[i] - As[i]) % self.q for i in range(self.n)]
        m = [round(b[i] / (self.q//self.scale)) % self.scale for i in range(self.n)]
        return m