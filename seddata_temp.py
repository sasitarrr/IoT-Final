import socket
import network
import time
from machine import Pin
import dht

#####################
serverip = 'xxx.xx.xx.x'
port = 9000
#####################

def send_data(data):
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server.connect((serverip,port))
    server.send(data.encode('utf-8'))
    data_server = server.recv(1024).decode('utf-8')
    print('Server:' , data_server)
    server.close()

###WIFI###
wifi = "Sasitarrr’s iPhone"
password = "12345678"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
time.sleep(3) #delay 3 sec
wlan.connect(wifi, password)
time.sleep(3) #delay 3 sec
print(wlan.isconnected())
###########

print("> Temperature checking...")
d = dht.DHT22(Pin(23))
time.sleep(1)

while True:
    d.measure()
    time.sleep(1)
    temp = d.temperature()
    humid = d.humidity()
    print(temp)
    print(humid)
    #text = "TEMP-HUMID:{} and {}".format(temp,humid)
    text = "TEMP:{}".format(temp)
    send_data(text)
    time.sleep(3)
    print("----------")
    
