'''
https://zh.wikipedia.org/zh-tw/%E5%9B%BD%E9%99%85%E6%A0%87%E5%87%86%E4%B9%A6%E5%8F%B7#10_%E4%BD%8D

'''


from key import *
from utils import *
import numpy as np

q = 999999937
n = 3
scale = 10000
bound = 5
A_size = 8
B_size = 32
sk_size = 12

id = input("Enter the ID (10 letters): ")
pw = input("Enter the password (8~15 letters): ")
flag1 = 0 # if the ID is 10 letter
flag2 = 0 # if the check code is true
flag3 = 0 # if the password's length between 8-15

# Check if the format of ID and password is correct
while 1:
    if len(id) == 10:
        flag1 = 1
    else:
        flag1 = 0

    if flag1 == 1:
        check = 0
        for i in range(9):
            check += ord(id[i]) * (10-i)
        check %= 11
        check = 11 - check
        if check == 10:
            check = ord('X')
        else:
            check += ord('0')

        if check != ord(id[9]):
            flag2 = 0
            # print("Wrong format.")
            # id = input("Enter the ID (10 letters): ")
        else:
            flag2 = 1
    if flag1 == 1 and flag2 == 1:
        if len(pw) < 8 or len(pw)>15:
            flag3 = 0
            # print("Wrong format.")
        else:
            flag3 = 1
    if flag1 == 1 and flag2 == 1 and flag3 == 1:
        break
    else:
        print("The ID or password format is incorrect")
        id = input("Enter the ID (10 letters): ")
        pw = input("Enter the password (8~15 letters): ")

# Generate the keys to the ID
print("This is your public key and private key.")
(pk, sk) = asym_key(id, pw, n, q, bound, A_size, B_size, sk_size)

print("pk: \n", pk)
print("sk:\n", sk)
