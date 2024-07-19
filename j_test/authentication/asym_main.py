from asym import *
import numpy as np
from key import *
from binary import *

q = 999999937
n = 3
scale = 10000
bound = 5
A_size = 8
B_size = 32
sk_size = 12

E = authentication(n, q, bound, scale, A_size, B_size, sk_size)

# 輸入 pk (binary的形式)，並檢查長度是否正確
pk = input("pk: ")
while len(pk) != A_size*9 + B_size*3:
    print("Wrong format")
    pk = input("pk: ")
# pk: 010010010100111101010100001100010011001000110011001101000011010100110110001110111001100111101100100111010011101110011010001110111011111100111011100110100011001100101011


# 輸入 sk (binary的形式)，並檢查長度是否正確
sk = input("sk: ")
while len(sk) != sk_size*3:
    print("Wrong format")
    sk = input("sk: ")

# sk: 111101011011110110101101000000011101

# 輸入一個數字，作為驗證訊息
print("Enter a number(0 ~ 9999): ")
m = int(input())

# 私鑰產生簽章
print("\nEncrypt")
c = E.encrypt(m, pk, sk)
print("c: ", c)
print(len(c))

# 公鑰驗證簽章
print("\nDecrypt")
p = E.decrypt(c, pk)
print("p: ", p)

# 驗證原本生成的訊息與簽章是否一致
assert m == p
print("\nm = p", "\nSuccessful!!")
