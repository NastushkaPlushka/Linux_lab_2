#!/usr/bin/python
# -*- coding: utf-8 -*-
print("-Start client.py")
import socket

# Создаем сокет
sock = socket.socket()

# Даем выбор между ручным вводом порта и автоматическим
if raw_input("Do you want to connect automatically?\nEnter 't' or 'n' ") == "t":
    host = 'localhost'
    port = 9090
elif "n":
    host = raw_input("enter hostname\n")
    port = int(raw_input("enter port number\n"))
else:
    print("you should have entered 't' or 'n' ")

# Осуществляем подключение по конкретному порту с выбранным ip
sock.connect((host, port))
print("-server connection established")

#data = sock.recv(1024)
#print("server: " + data)

# Отсылаем и принимаем на сервер сообщения, 
# пока не будет введена команда "exit"
s = "0"
while s != "exit":
    s = raw_input("please write your message\n")
    sock.send(s)
    print("-sending data to server")

    print("-dreceiving data from the server")
    data = sock.recv(1024)
    print("server: " + data)

    if not data:
        print("-server disconnection process")
        break

print("-disconnecting from the server")

# Закрываем соединение
sock.close()
