from App.utils import *
from App.binary import *

class authentication:
    def __init__(self, n, q, bound, scale, A_size, B_size, sk_size):
        self.n = n
        self.q = q
        self.bound = bound
        self.scale = scale
        self.A_size = A_size
        self.B_size = B_size
        self.sk_size = sk_size

    # 私鑰產生簽章
    def encrypt(self, m, pk, sk_binary):

        # 對 A 與 sk 做處理 (這個 function 沒有使用到 B，所以沒對 B 做處理)
        A_binary = pk[:self.A_size*9] # 從 pk 拆出 A (binary 的形式) 
        A = binary_to_A(A_binary, self.A_size) # 把 A 轉為 matrix
        sk = binary_to_sk(sk_binary, self.sk_size) # 把 sk 轉為 vector

        # 計算
        r = sample_bounded_vector(self.n, self.bound) # 生成隨機 vector，作為 r
        e2 = sample_bounded_vector(self.n, self.bound) # 生成隨機 vector，作為干擾值
        e3 = sample_bounded_vector(1, self.bound)[0] # 生成隨機數(只有一個數)，作為干擾值
        At = matrix_transpose(A) # 將 A 轉置成At
        rAs = matrix_vector_multiplication(At, r, self.q) # rAs = At * r (vector)
        rAs = vector_vector_addition(rAs, e2, self.q) # rAs = At * r + e2 (vector)
        rAs = vector_vector_inner_product(rAs, sk, self.q) # rAs = (At * r + e2) * sk (單一個數)
        rAs = (rAs + e3) % self.q # rAs = (At * r + e2) * sk + e3(單一個數)
        m = m * (self.q // self.scale) % self.q # 將 m 做處理 (先 *(q/scale)，在 mod q) 
        c = (rAs + m) % self.q # c = rAs + m ，產生密文

        
        r_binary = sk_to_binary(r, self.sk_size) # 將剛剛隨機生成的 r vector 轉為 binary 字串
        c_binary = decimal_to_binary(c, self.B_size) # 將生成的密文 c 轉為 binary 字串
        text = r_binary + c_binary # 兩字串做相加，作為輸出
        return (text)
    
    # 公鑰驗證簽章
    def decrypt(self, ctx, pk):
        # 處理收到的密文，找出 r 與 c
        r_binary = ctx[ :self.sk_size*3]
        c_binary = ctx[self.sk_size*3: ]
        r = binary_to_sk(r_binary, self.sk_size) # 將 r 轉回 vector 形式
        c = binary_to_decimal(c_binary) # 將 c 轉回 decimal

        # 利用 pk 找出 B
        B_binary = pk[self.A_size*9:] 
        B = binary_to_B(B_binary, self.B_size) # 將 B 轉回 vector 的形式
        rAs = vector_vector_inner_product(r, B, self.q) # 計算出 rAs = r * B
        m = (c - rAs) % self.q # m = c - rAs
        p = round(m / (self.q // self.scale)) % self.scale # (明文)p = m / (q/scale) 
        return p

class LWEasym:
    def __init__(self, n, q, bound, scale, A_size, B_size, sk_size):
        self.n = n
        self.q = q
        self.bound = bound
        self.scale = scale
        self.A_size = A_size
        self.B_size = B_size
        self.sk_size = sk_size
    
    # 公鑰加密訊息
    def encrypt(self, m, pk):
        A_binary = pk[ : self.A_size*9] # 從 pk 拆出 A (binary) 
        B_binary = pk[self.A_size*9 : ] # 從 pk 拆出 B (binary)
        A = binary_to_A(A_binary, self.A_size) # 把 A 轉回 matrix
        B = binary_to_B(B_binary, self.B_size) # 把 B 轉回 vector
        r = sample_bounded_vector(self.n, self.bound) # 生成隨機 vector，作為 r
        e2 = sample_bounded_vector(self.n, self.bound) # 生成隨機 vector，作為干擾值
        e3 = sample_bounded_vector(1, self.bound)[0]  # 生成隨機數(只有一個數)，作為干擾值
        At = matrix_transpose(A) # 將 A 轉置為 At
        u = matrix_vector_multiplication(At, r, self.q) # u = At * r = r * A
        u = vector_vector_addition(u, e2, self.q) # u = r * A + e2
        rAs = vector_vector_inner_product(r, B, self.q) # rAs = r * B
        rAs = (rAs + e3) % self.q # rAs = r * B + e3
        m = m * (self.q//self.scale) # m = m * (q/scale)
        c = (rAs + m) % self.q # c = rAs + m
        u_binary = B_to_binary(u, self.B_size)
        c_binary = decimal_to_binary(c, self.B_size)
        ctx = u_binary + c_binary
        # return (u, c)
        return ctx
    
    def decrypt(self, ctx, sk_binary):
        sk = binary_to_sk(sk_binary, self.sk_size)
        u_binary = ctx[ : self.B_size*3]
        c_binary = ctx[self.B_size*3 : ]
        # (u, c) = ctx[0], ctx[1]
        u = binary_to_B(u_binary, self.B_size)
        c = binary_to_decimal(c_binary)
        rAs = vector_vector_inner_product(u, sk, self.q)
        m = (c - rAs) % self.q
        p = round(m / (self.q // self.scale)) % self.scale
        return p