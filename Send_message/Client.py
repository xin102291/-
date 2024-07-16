import socket
from asym import *
import numpy as np
from key import *
import json
import random
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

client_type = 'linxinfa'

def send_data(client,cmd,**kv):
    global client_type
    jd = {}
    jd['COMMAND'] = cmd
    jd['client_type'] = client_type
    jd['data'] = kv

    jsonstr = json.dumps(jd)
    # print("send: "+jsonstr)
    client.sendall(jsonstr.encode('utf8'))

def input_client_type():
    return input("name: ")

if __name__ == "__main__":
    client_type = input_client_type()
    client = socket.socket()
    client.connect(ADDRESS)
    print("產生簽章:")
    msg = json.loads(client.recv(1024).decode(encoding='utf8'))
    c = E_iot.encrypt(msg, pk_iot, sk_iot)
    print(c)
    print("產生驗證訊息:")
    m = random.randint(0, 9999)
    print(m)
    c= list(c)
    c.append(m)
    send_data(client,"SEND_DATA",data = c)
    msg = json.loads(client.recv(1024).decode(encoding='utf8'))
    if msg == 0:
        print("不成功")
    else:
        print("成功")
        p = E_server.decrypt(msg, pk_server)
        if(p == m):
            print("驗證成功")
    send_data(client,"CONNECT")
    

    while True:
        q = 1000
        # n = len(value)
        n = 10
        scale = 10
        B = 5

        data = input("請輸入訊息: ")
        if data == "exit":
            break
        m = [0 for _ in range(n)]
        for i in range(0, len(data)):
            m[10 - len(data) + i] = ord(data[i])-48
        E = LEWSymmetric(n, q, B, scale)
        array = list(map(int, input("key: ").split(' ')))
        s = array[0:10]
        c = E.encrypt(s, m)
        send_data(client,"SEND_DATA",data = c)
        
        
