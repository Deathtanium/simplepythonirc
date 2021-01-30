#!/usr/bin/env python3

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
        main_thread = threading.Thread(target=self.msgsend_loop)
        receive_thread = threading.Thread(target=self.receive)

        #starting the threads
        main_thread.start()
        receive_thread.start()
    
    #main messaging loop
    def msgsend_loop(self):
        while True:
            message = input()
            self.sock.send(message.encode('utf-8'))
    
    #loop for updating message history
    def receive(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except ConnectionAbortedError:
                print("ConnectionAbortedError, do CTRL-C to exit")
                exit(0)
                break
            except:
                print("Generic Error, do CTRL-C to exit")
                exit(0)
                break

#driver code
client = Client(HOST, PORT)


















