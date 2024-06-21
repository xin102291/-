
'''
https://zh.wikipedia.org/zh-tw/%E5%9B%BD%E9%99%85%E6%A0%87%E5%87%86%E4%B9%A6%E5%8F%B7
'''

id = input("Enter 9 letters: ")

while(len(id) != 9):
    print("Wrong Format.")
    id = input("Enter 9 letters: ")

check = 0
for i in range(9):
    check += ord(id[i]) * (10-i)
check %= 11
check = 11 - check
if(check == 10):
    print("Your ID is: ", id + "X")
else:
    print("Your ID is: ", id, end="")
    print(check)
