from asym import *
import numpy as np
from key import *

q = 999999937
n = 3
scale = 10000
bound = 5
A_size = 8
B_size = 32
sk_size = 12

# E = authentication(n, q, bound, scale, A_size, B_size, sk_size)
E = LWEasym(n, q, bound, scale, A_size, B_size, sk_size)

# 輸入 pk (以 binary 的形式)，並判斷長度是否正確
pk = input("pk: ")
while len(pk) != A_size*9 + B_size*3:
    print("Wrong format")
    pk = input("pk: ")
# pk: 010010010100111101010100001100010011001000110011001101000011010100110110001110111001100111101100100111010011101110011010001110111011111100111011100110100011001100101011

# 輸入 sk (以 binary 的形式)，並判斷長度是否正確
sk = input("sk: ")
while len(sk) != sk_size*3:
    print("Wrong format")
    sk = input("sk: ")
# sk: 111101011011110110101101000000011101

# 產生五個隨機數，存入 m array
m = [0 for _ in range(5)]
print("Generate a random message.")
for i in range(5):
    m[i] = random.randint(0, 9999)
    print(m[i] ,end=" ")
print("")

# 將 m array 加密，存入 c array
c = [0 for _ in range(5)]
print("\nEncrypt")
print("c: ")
for i in range(5):
    c[i] = E.encrypt(m[i], pk)
    print(c[i], end="\n")
print("")

# 將 c array 解密，存入 p array
p = [0 for i in range(5)]
print("\nDecrypt")
print("p: ")
for i in range(5):
    p[i] = E.decrypt(c[i], sk)
    print(p[i], end=" ")
print("")

# 生成 session key
session_key = [0 for _ in range(10)]
count=0
for i in range(5):
    # 將每個 p array 中的數再拆成兩組
    session_key[count] = p[i]//100
    count += 1
    session_key[count] = p[i] % 100
    count += 1
# 最後會有 10 組數字，作為 session key 使用
print("session key: ", session_key)