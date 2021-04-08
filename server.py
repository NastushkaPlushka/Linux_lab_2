#!/usr/bin/python
# -*- coding: utf-8 -*-
# server test

import socket
import logging
import random
import hashlib

# Стандартный порт
DEFAULT_PORT = 9090
# Настройки логирования
logging.basicConfig(filename="logs.log", format='%(asctime)s-%(levelname)s- %(message)s', level=logging.INFO)

def code_pass(password):
    return hashlib.sha224(password.encode("utf-8")).hexdigest()

def is_port_free(port):
    try:
        sock = socket.socket()
        sock.bind( ("", port) )
        sock.close()
        logging.info("port %i is free", port)
        return True
    except:
        logging.warning("port %i is busy", port)
        return False

def check_ip(ip):
    f = open('usernames.txt')
    try:
        ip_list = { line.split(':')[0] :  line.split(':')[1] for line in f }
        f.close()
        for x in ip_list.items():
            if ip == x[0]:
                return x[1][:-1]
        return ""
    except:
        return ""

def is_true_pass(ip, password):
    f = open('usernames.txt')
    ip_list = { line.split(':')[0] :  line.split(':')[2] for line in f }
    f.close()
    for x in ip_list.items():
        if ip == x[0]:
            if x[1][:-1] == code_pass(password):
                return True

    return False

def add_ip(ip, name, password):
    f = open('usernames.txt', 'a')
    f.write(ip + ":" + name + ":" + code_pass(password) + "\n")
    f.close()




print("Server is running")
logging.info("server is running")


sock = socket.socket()

if is_port_free(DEFAULT_PORT):
    sock.bind( ("", 9090) )


    sock.listen(1)
    print("-port %d is listening"%DEFAULT_PORT)
    logging.info("port %i is listening", DEFAULT_PORT)
else:
    flag = False
    while flag == False:

        port = round( random.random() * 63000 + 1024 )
        print("-port %d is checking"%port)
        logging.info("port %i is checking", port)
        if is_port_free(port):
            flag = True
    print("-port %d is listening"%port)
    logging.info("port %i is listening", port)

try:
    while True:
        conn, addr = sock.accept()
        print("-client was connected")
        logging.info("client was connected")
        print("addr: " + addr[0])
        name = check_ip(addr[0])
        print("name: <" + name +">")
        if name == "":
            d = conn.recv(1024)
            conn.send("Hi, what is your name? ")
            name = conn.recv(1024)
            print("name: " + name)
            conn.send("enter your password pls ")
            password = conn.recv(1024)
            print("password: " + password)
            add_ip(addr[0], name, password)
            conn.send("password add")
            print("password add")
        name = conn.recv(1024)
        conn.send("Hellow, Mr " + name + "\n")
        
        conn.send("enter your password pls ")
        psw = conn.recv(1024)

        if is_true_pass(addr[0], psw) == False:
            print("Incorrect password")
            conn.send("Incorrect password, bye ")
            #conn.close()
            raise ValueError
        #print("Congratulations!!")
        conn.send("Congratulations!!")

        while True:

            data = conn.recv(1024)
            print("-process of receiving data from the client")
            logging.info("process of receiving data from the client")

            print("data: " + data)


            if not data:
                print("-client disconnection process")
                logging.info("client disconnection process")

                break
            conn.send(data)
            print("-data has been sent to the client")
            logging.info("data has been sent to the client")
except:
    print("Something went wrong")
    logging.warning("exception")
finally:  

    print("-server is stopping")
    logging.info("server is stopping")
    sock.close()