
def decimal_to_binary(x, size):
    if x >= 0:
        binary_str = bin(x)
    else:
        binary_str = bin((1 << size) + x)
    return binary_str[2:].zfill(size)

def binary_to_decimal(binary_str):
    sign = binary_str[0]
    value = binary_str[1:]
    if sign == '0':
        decimal = int(value, 2)
    else:
        abs_value = ''.join('1' if bit == '0' else '0' for bit in value)
        abs_decimal = int(abs_value, 2) + 1
        decimal = -abs_decimal
    return decimal

def split_binary(binary_str, size):
    return [binary_str[i:i+size] for i in range(0, len(binary_str), size)]

def A_to_binary(A, size):
    binary_str = ""
    for i in range(3):
        for j in range(3):
            binary = decimal_to_binary(A[i][j], size)
            binary_str += binary
    return binary_str

def binary_to_A(binary_str, size):
    block = split_binary(binary_str, size)
    decimal = [binary_to_decimal(i) for i in block]
    dec = [[0 for _ in range(3)] for _ in range(3)]
    m=0
    for i in range(3):
        for j in range(3):
            dec[i][j] = decimal[m]
            m += 1
    return dec

def B_to_binary(B, size):
    binary_str = ""
    for i in range(3):
        binary_str += decimal_to_binary(B[i], size)
    return binary_str

def binary_to_B(binary_str, size):
    block = split_binary(binary_str, size)
    decimal = [binary_to_decimal(i) for i in block]
    return decimal

def sk_to_binary(sk, size):
    binary_str = ""
    for i in range(3):
        binary_str += decimal_to_binary(sk[i], size)
    return binary_str

def binary_to_sk(binary_str, size):
    block = split_binary(binary_str, size)
    decimal = [binary_to_decimal(i) for i in block]
    return decimal