#!/usr/bin/env python3

import sys
import socket
import threading

HOST = '192.168.0.122' #84.117.187.56 for 
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

logFile = open('log.txt', 'w')

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message.encode('utf-8'))

def handle(client):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            message = f"{nicknames[clients.index(client)]}: {msg}"
            if len(msg) > 1:
                #logging
                stdout_backup = sys.stdout
                sys.stdout = logFile
                print(message)
                sys.stdout = stdout_backup
                print(message)
                
                #send the message to everyone
                broadcast(f"{message}")
        except:
            #this should be triggered if the client becomes unreachable
            index = clients.index(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            
            clients.remove(client)
            client.close()
            
            print(f"{nickname} disconnected.")
            break
        
def receive():              
    while True:
        client, address = server.accept()

        client.send("NICK".encode('utf-8'))  #requesting nickname from client
        nickname = client.recv(1024).decode('utf-8')         #taking their response
        
        nicknames.append(nickname)
        clients.append(client)

        #logging
        msg = f"{nickname} connected to the server from {str(address)}"
        stdout_backup = sys.stdout
        sys.stdout = logFile
        print(msg)
        sys.stdout = stdout_backup
        print(msg)
        
        broadcast(f"{nickname} connected to the server")

        thread = threading.Thread(target=handle, args=(client,))
        
        thread.start()

print ("Server running")
receive()
