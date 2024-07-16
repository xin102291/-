import numpy as np
from utils import *
from binary import *
import hashlib

def func(x):
    if x >= 1000:
        x = (x - 1000) * (-1)
    return x
'''
因為 sk 數值範圍在 -1000 ~ +1000 之間
所以將生成的數 mod 2000
再將超過1000的數減掉1000變成負數
'''

# 生成公私鑰
def asym_key(id, pw, n, q, bound, A_size, B_size, sk_size):

    A = [[0 for _ in range(n)] for _ in range(n)]
    k=0
    # 將 id 的 ASCII 轉為 A matrix
    for i in range(n):
        for j in range(n):
            A[i][j] = int(ord(id[k]))
            k += 1

    # 計算 sk vector
    sk = [0, 0, 0]
    for i in range(3):
        sk[i] = pw[i*5 : (i+1)*5]
        sk[i] = int(sk[i], 16)
        sk[i] %= 2000
        sk[i] = func(sk[i])
    # print("sk: ", sk)
    sk_binary = sk_to_binary(sk, sk_size) # 將 sk 轉為 binary string

    e = sample_bounded_vector(n, bound) # 隨機生成一個 vector 作為干擾值
    As = matrix_vector_multiplication(A, sk, q) # As = A * s
    B = vector_vector_addition(As, e, q) # B = A  * s + e
    # print("A: ", A)
    # print("B: ", B)

    # 將 A, B 轉為字串，接在一起做為 pk
    A_binary = A_to_binary(A, A_size)
    B_binary = B_to_binary(B, B_size)
    pk = A_binary + B_binary

    return (pk, sk_binary)

# 生成對稱式金鑰
def symm_key(n, q):
    s = sample_uniform_vector(n, q) # 隨機生成一個 vector 作為金鑰
    return s