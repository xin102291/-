'''
判斷身份證字號檢查碼
'''

id = input("ID: ")
# 將身分證分為戶籍碼、流水號、檢查碼
letter = id[0]
digit = id[1:9]
check_num = id[9]

# 計算戶籍碼編號
letter_array = [10, 11, 12, 13, 14, 15, 16, 17, 34, 18, 19, 20, 21, 22, 35, 23, 24, 25, 26, 27, 28, 29, 32, 30, 31, 33]
letter_num = letter_array[ord(letter) - ord('A')]

# 計算流水號
digit_num = 0
for i in range(8):
    digit_num += int(digit[i]) * (8-i)
digit_num = digit_num + (letter_num//10) + (letter_num%10) * 9

# 判斷檢查碼是否正確
if 10 - (digit_num%10) != int(check_num):
    print("Error")
else:
    print("Welcome")