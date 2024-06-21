import random
from utils import *
from symm import *
import numpy as np

q = 100003
n = 10
scale = 1000
bound = 5

print("Enter the message(less than 10 letter): ")
value = input()
while len(value) > 10:
    print("out of range")
    print("Enter the message(less than 10 letter): ")
    value = input()

m = [0 for _ in range(n)]
for i in range(0, len(value)):
    m[10 - len(value) + i] = ord(value[i])

E = LEWSymmetric(n, q, bound, scale)

print("session key: ")
array = list(map(int, input().split(' ')))
s = array[0:10]

print("\nEncrypt")
c = E.encrypt(s, m)
print(c)

print("\nDecrypt")
p = E.decrypt(s, c)
text_p = ""
for i in p:
    if(i != 0):
        text_p += chr(i)

print(text_p)