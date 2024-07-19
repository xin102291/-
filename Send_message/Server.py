import socket
from threading import Thread
import time
import json
from asym import *
from key import *
from symm import *
import os
q = 999999937
n = 3
scale = 10000
bound = 5
A_size = 8
B_size = 32
sk_size = 12



E_iot = authentication(n, q, bound, scale, A_size, B_size, sk_size)
pk_iot = ""

E_server = authentication(n, q, bound, scale, A_size, B_size, sk_size)
pk_server = ""
sk_server = ""

def get_key(iot_id):
    global pk_server,sk_server,pk_iot
    filename = "items.json"
    target_dir = 'Send_message'
    os.makedirs(target_dir, exist_ok=True)
    file_path = os.path.join(target_dir, filename)
    try:
        with open(file_path, "r") as file:
            items = json.load(file)
    except FileNotFoundError:
        print("找不到文件，無法更新數據")

    for item in items:
        if item["id"] == "SERVER1231":
            pk_server = item["pk"]
            sk_server = item["sk"]
        if item["id"] == iot_id:
            pk_iot = item["pk"]
ADDRESS = ("192.168.50.173",88)

g_socket_server = None 
g_conn_pool = {}

#初始化伺服器
def init():
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    g_socket_server.bind(ADDRESS)
    g_socket_server.listen(5) 
    print("server start,wait for client connecting...")

def accp_client():
    while True:
        client,info = g_socket_server.accept()
        thread = Thread(target=message_handle,args=(client,info),daemon=True)
        thread.start()


def message_handle(client,info):
    # client.sendall("connect server successfully!".encode(encoding="utf8"))
    print("產生驗證訊息")
    m = random.randint(0, 9999)
    client.sendall(f"{m}".encode(encoding="utf8"))
    while True:
        try:
            bytes = client.recv(1024)
            msg = bytes.decode(encoding = "utf8")
            jd = json.loads(msg)
            cmd = jd["COMMAND"]
            client_name = jd["client_name"]
            if "CONNECT" == cmd:
                g_conn_pool[client_name] = client
                # print("on client connect: "+client_name,info)
                # client.sendall("ACK!".encode(encoding="utf8"))
                #session_key
                print("session_key")
                E = LWEasym(n, q, bound, scale, A_size, B_size, sk_size)
                # 產生五個隨機數，存入 m array
                m = [0 for _ in range(5)]
                print("Generate a random message.")
                for i in range(5):
                    m[i] = random.randint(0, 9999)
                # 將 m array 加密，存入 c array
                c = [0 for _ in range(5)]
                for i in range(5):
                    c[i] = E.encrypt(m[i], pk_iot)
                print(c)
                c= [c]
                c = json.dumps(c)
                client.sendall(c.encode(encoding="utf8"))
                
                print("on client connect: "+client_name,info)
            elif "SEND_DATA" == cmd:
                get_key(client_name)
                data = jd['data']['data']
                print("接收訊息: ",data)
                if len(data) == 2: #以長度判斷是否為正常驗證訊息
                    print("驗證簽章")
                    c = data[0]
                    p = E_iot.decrypt(c[0], pk_iot)
                    if(p == m):
                        print("驗證成功")
                        print("產生簽章:")
                        c = E_server.encrypt(data[1][0], pk_server, sk_server)
                        print(c)
                        c= [c]
                        c = json.dumps(c)
                        client.sendall(c.encode(encoding="utf8"))
                        
                    else:
                        print("驗證失敗")
                        client.sendall("0".encode(encoding="utf8"))
                # print(jd['data']['data'])
                else:
                    q = 1000
                    # n = len(value)
                    n = 10
                    scale = 10
                    B = 5
                    E = LEWSymmetric(n, q, B, scale)
                    # print(jd['data']['data'])
                    array = list(map(int, input("key: ").split(' ')))
                    s = array[0:10]
                    p = E.decrypt(s,jd['data']['data'])
                    text_p = ""
                    for i in p:
                        if(i != 0):
                            text_p += str(i)
                    print(f"{client_name}:{text_p}")
                    # print(f"{client_name}:{jd['data']['data']}")
                
                
                
        except Exception as e:
            # print(e)
            remove_client(client_name)
            break


def remove_client(client_name):
    client = g_conn_pool[client_name]
    if None != client:
        client.close()
        g_conn_pool.pop(client_name)
        print("client offline: "+client_name)

if __name__ == '__main__':
    init()
    thread = Thread(target=accp_client,daemon=True)
    thread.start()
    while True:
        time.sleep(0.1)

