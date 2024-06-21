import hashlib

username = input("帳號: ")
password = input("密碼: ")

'''
正確帳號密碼:
帳號:DD1051210X
密碼:1051210

'''

correct_pw = "5ffdcbb218bdbcf6e1e4e13cece77e80916f42d2cfca450ea060b294"

flag1 = 0 # if the username is 10 letters
flag2 = 0 # if the check number is true
flag3 = 0 # if the password is true

while(flag1 == 0 or flag2 == 0 or flag3 == 0):
    if(len(username) == 10):
        flag1 = 1
    else:
        flag1 = 0
        print("帳號或密碼輸入錯誤!")
        username = input("帳號: ")
        password = input("密碼: ")
    
    if(flag1 == 1):
        check = 0
        for i in range(9):
            check += ord(username[i]) * (10-i)
        check %= 11
        check = 11 - check
        if(check == 10):
            check = ord('X')
        else:
            check += ord('0')
        if(check != ord(username[9])):
            flag2 = 0
            print("帳號或密碼輸入錯誤!")
            username = input("帳號: ")
            password = input("密碼: ")
        else:
            flag2 = 1
    if(flag1 == 1 and flag2 == 1):
        sha224 = hashlib.sha224()
        sha224.update(password.encode('utf-8'))
        hash_digest = sha224.hexdigest()
        if(f"{hash_digest}" != correct_pw):
            flag3 = 0
            print("帳號或密碼輸入錯誤!")
            username = input("帳號: ")
            password = input("密碼: ")
        else:
            flag3 = 1

        # print(f"SHA-224 Hash: {hash_digest}")

        # a = f"{hash_digest}"

print("Welcome!!")