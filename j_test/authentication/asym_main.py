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
sk_size = 8

E = authentication(n, q, bound, scale, A_size, B_size, sk_size)

pk = input("pk: ")
while len(pk) != A_size*9 + B_size*3:
    print("Wrong format")
    pk = input("pk: ")

sk = input("sk: ")
while len(sk) != sk_size*3:
    print("Wrong format")
    sk = input("sk: ")

print("Enter a number(0 ~ 9999): ")
m = int(input())

print("\nEncrypt")
c = E.encrypt(m, pk, sk)
print("c: ", c)

print("\nDecrypt")
p = E.decrypt(c, pk)
print("p: ", p)

assert m == p
print("\nm = p", "\nsuccessful!!")
