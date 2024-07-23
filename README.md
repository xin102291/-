# 使用網站時請記得創建pqc使用者與server資料庫
dbConn = myconn.connect(
    host = 'localhost',   
    user = 'pqc',         
    password = '123456',  
    database = 'server'   
)

# Lattice
B = A * (sk) + e

public key = (A, B)

private key = sk

# authentication資料夾 流程
先用check.py找檢查碼，生成編號

再用key_main.py輸入編號，生成公私鑰

接下來就可以使用asym_main.py進行身分驗證或是session_key.py產生會議金鑰

