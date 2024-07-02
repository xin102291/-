import socket
from threading import Thread
import time
import json
from asym import *
from key import *
from symm import *

q = 999999937
n = 3
scale = 10000
B = 5

E_iot = authentication(n, q, B, scale)
(pk_iot, sk_iot) = asym_key("0123456789", n, q, B)

E_server = authentication(n, q, B, scale)
(pk_server, sk_server) = asym_key("1104427321", n, q, B)
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
            client_type = jd["client_type"]
            if "CONNECT" == cmd:
                g_conn_pool[client_type] = client
                print("on client connect: "+client_type,info)
                # client.sendall("ACK!".encode(encoding="utf8"))
            elif "SEND_DATA" == cmd:
                data = jd['data']['data']
                if len(data) == 3 and len(data[0]) == 3: #以長度判斷是否為正常驗證訊息
                    print("接收訊息:",jd['data']['data'])
                    print("驗證簽章")
                    c = data[0:2]
                    p = E_iot.decrypt(c, pk_iot)
                    if(p == m):
                        print("驗證成功")
                        print("產生簽章:")
                        c = E_server.encrypt(data[2], pk_server, sk_server)
                        print(c)
                        c= list(c)
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
                    print(f"{client_type}:{text_p}")
                    # print(f"{client_type}:{jd['data']['data']}")
                
                
                
        except Exception as e:
            # print(e)
            remove_client(client_type)
            break


def remove_client(client_type):
    client = g_conn_pool[client_type]
    if None != client:
        client.close()
        g_conn_pool.pop(client_type)
        print("client offline: "+client_type)

if __name__ == '__main__':
    init()
    thread = Thread(target=accp_client,daemon=True)
    thread.start()
    while True:
        time.sleep(0.1)

