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

E = authentication(n, q, bound, scale, A_size, B_size, sk_size)

pk = input("pk: ")
while len(pk) != A_size*9 + B_size*3:
    print("Wrong format")
    pk = input("pk: ")

sk = input("sk: ")
while len(sk) != sk_size*3:
    print("Wrong format")
    sk = input("sk: ")

m = [0 for _ in range(5)]

print("Generate a random message.")
for i in range(5):
    m[i] = random.randint(0, 9999)
    print(m[i] ,end=" ")
print("")

c = [0 for _ in range(5)]

print("\nEncrypt")
print("c: ")
for i in range(5):
    c[i] = E.encrypt(m[i], pk, sk)
    print(c[i], end="\n")
print("")

p = [0 for i in range(5)]

print("\nDecrypt")
print("p: ")
for i in range(5):
    p[i] = E.decrypt(c[i], pk)
    print(p[i], end=" ")
print("")


session_key = [0 for _ in range(10)]
count=0
for i in range(5):
    session_key[count] = p[i]//100
    count += 1
    session_key[count] = p[i] % 100
    count += 1

print("session key: ", session_key)