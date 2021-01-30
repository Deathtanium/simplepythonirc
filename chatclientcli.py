#!/usr/bin/env python3

import sys
import socket
import threading
import hashlib

HOST = '84.117.187.56'
PORT = 9090

class Client:
    def __init__(self, host, port):
        
        self.username = input("Username: ")
        self.password = input("Password: ")
        self.passhash = hashlib.sha256(self.password.encode('utf-8')).hexdigest()
            
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
                print ("\033[A                             \033[A")
                if len(message)>1 and len(message)<128:
                    self.sock.send(message.encode('utf-8'))
            except KeyboardInterrupt:
                print("\nClient stopping1")
                exit()
    
    #loop for updating message history
    def receive(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'LOGIN':
                    self.sock.send(f"{self.username}#{self.passhash}".encode('utf-8'))
                    message = self.sock.recv(1024).decode('utf-8')
                    if message == 'OK':
                        pass #login successful
                    elif message == 'BADUSERNAME':
                        print("This username doesn't exist.\nContact the owner of this server if you know him in order to register an account on this server.")
                        break
                    elif message == 'BADPASSWORD':
                        print("Incorrect password.")
                        break
                    elif message == 'ALREADYLOGGED':
                        print("You are already logged in from another device.")
                        break
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
