import socket
import json
import random
import Adafruit_DHT as DHT
import datetime
from time import sleep
from asym import *
from symm import *
from key import *
import os

DHT_sensor = DHT.DHT11
DHT_pin = 4

q = 999999937
n = 3
scale = 10000
bound = 5
A_size = 8
B_size = 32
sk_size = 12

session_key = ""
E_iot = authentication(n, q, bound, scale, A_size, B_size, sk_size)
pk_iot = ""
sk_iot = ""
E_server = authentication(n, q, bound, scale, A_size, B_size, sk_size)
pk_server = ""

ADDRESS = ("192.168.50.173",88)

client_name = 'linxinfa'

def send_data(client,cmd,**kv):
    global client_name
    jd = {}
    jd['COMMAND'] = cmd
    jd['client_name'] = client_name
    jd['data'] = kv

    jsonstr = json.dumps(jd)
    # print("send: "+jsonstr)
    client.sendall(jsonstr.encode('utf8'))

def input_client_name():
    return input("name: ")

def get_key(iot_id):
    global pk_server,sk_iot,pk_iot
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
        if item["id"] == iot_id:
            pk_iot = item["pk"]
            sk_iot = item["sk"]

if __name__ == "__main__":
    client_name = input_client_name()
    get_key(client_name)
    client = socket.socket()
    client.connect(ADDRESS)
    print("產生簽章:")
    msg = json.loads(client.recv(1024).decode(encoding='utf8'))
    c = E_iot.encrypt(msg, pk_iot, sk_iot)
    print(c)
    print("產生驗證訊息:")
    m = random.randint(0, 9999)
    print(m)
    c= [[c]]
    c.append(m)
    send_data(client,"SEND_DATA",data = c)
    msg = json.loads(client.recv(1024).decode(encoding='utf8'))
    if msg == 0:
        print("失敗")
    else:
        p = E_server.decrypt(msg, pk_server)
        if(p == m):
            print("驗證成功")
    send_data(client,"CONNECT")
    msg = json.loads(client.recv(1024).decode(encoding='utf8'))
    # print(msg)
    E = LWEasym(n, q, bound, scale, A_size, B_size, sk_size)
    p = [0 for i in range(5)]
    for i in range(5):
        p[i] = E.decrypt(msg[i], sk_iot)
    # 生成 session key
    session_key = [0 for _ in range(10)]
    count=0
    for i in range(5):
        # 將每個 p array 中的數再拆成兩組
        session_key[count] = p[i]//100
        count += 1
        session_key[count] = p[i] % 100
        count += 1
    

    while True:
        q = 100003
        n = 10
        scale = 1000
        bound = 5
        today = datetime.datetime.now().strftime("%Y-%m-%d %X")
        rh, tmp = DHT.read_retry( DHT_sensor, DHT_pin )
        if rh is not None and tmp is not None:
            # print('日期={2} 溫度={0:0.1f}度C 濕度={1:0.1f}%'.format(tmp, rh, today))
            data = '{2},{0:0.1f},{1:0.1f}'.format(tmp, rh, today)
            print(data)
            m = [0 for _ in range(n)]
            for i in range(0, len(data)):
                m[10 - len(data) + i] = ord(data[i])
            E = LEWSymmetric(n, q, bound, scale)
            c = E.encrypt(session_key, m)
            send_data(client,"SEND_DATA",data = c)
        else:
            print('讀取失敗，重新讀取。')
        sleep(1)
        
