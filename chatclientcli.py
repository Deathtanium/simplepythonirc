#!/usr/bin/env python3

import sys
import socket
import threading

HOST = '84.117.187.56'
PORT = 9090

class Client:
    def __init__(self, host, port):
        
        #set nickname
        self.nickname = input("Please enter your nickname: ")
        
        #connect to server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port)) #host = domain name/WAN IP of the server

        #setting the two parralel threads
        self.main_thread = threading.Thread(target=self.msgsend_loop)
        self.main_thread.daemon = True

        #starting the threads
        self.main_thread.start()
        self.receive()
    
    #main messaging loop
    def msgsend_loop(self):
        while True:
            try:
                message = input()
                if len(message)>1:
                    self.sock.send(message.encode('utf-8'))
            except KeyboardInterrupt:
                print("\nClient stopping1")
                exit()
    
    #loop for updating message history
    def receive(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                #why is is sending blank data when closed?
                elif message=='1':
                    print("\nServer shutdown")
                    self.sock.close()
                    break
                elif message=='':
                    continue
                else:
                    print(message)
            except KeyboardInterrupt:
                print("\nKeyboard halt signal")
                break
        exit()
#driver code
try:
    client = Client(HOST, PORT)
except ConnectionRefusedError:
    print("\nServer is unreachable")
except:
    print("\nClient stopped")
