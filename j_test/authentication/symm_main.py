import random
from utils import *
from symm import *
import numpy as np

q = 100003
n = 10
scale = 10000
bound = 5

# 輸入要加密的訊息，並檢查長度是否小於 10
print("Enter the message(less than 10 letter): ")
value = input()
while len(value) > 10:
    print("out of range")
    print("Enter the message(less than 10 letter): ")
    value = input()

# 將訊息轉為 ASCII 並存入 array
m = [0 for _ in range(n)]
for i in range(0, len(value)):
    m[10 - len(value) + i] = ord(value[i])

E = LEWSymmetric(n, q, bound, scale)

# 輸入 session key
print("session key: ")
array = list(map(int, input().split(' ')))
session_key = array[0:10]

# 加密訊息
print("\nEncrypt")
c = E.encrypt(session_key, m)
print(c)

# 解密訊息
print("\nDecrypt")
p = E.decrypt(session_key, c)
text_p = ""
for i in p:
    if(i != 0):
        text_p += chr(i)
print(text_p)