import socket
import json
import random
import Adafruit_DHT as DHT
import datetime
from time import sleep
from asym import *
from key import *

DHT_sensor = DHT.DHT11
DHT_pin = 4

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
        print("失敗")
    else:
        p = E_server.decrypt(msg, pk_server)
        if(p == m):
            print("驗證成功")
    send_data(client,"CONNECT")
    

    while True:
        today = datetime.datetime.now().strftime("%Y-%m-%d %X")
        rh, tmp = DHT.read_retry( DHT_sensor, DHT_pin )
        if rh is not None and tmp is not None:
            # print('日期={2} 溫度={0:0.1f}度C 濕度={1:0.1f}%'.format(tmp, rh, today))
            data = '日期={2} 溫度={0:0.1f}度C 濕度={1:0.1f}%'.format(tmp, rh, today)
            print(data)
            send_data(client,"SEND_DATA",data = data)
        else:
            print('讀取失敗，重新讀取。')
        sleep(1)
        
