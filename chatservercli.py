#!/usr/bin/env python3

import os
import sys
import socket
import threading
import hashlib
import datetime

HOST = '192.168.0.122'
PORT = 9090

accFileName = 'accounts.txt'
accFilePath = ''

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))

server.listen()

clients = []
usernames = []
passhashes = []

accFile = open(f"{accFilePath}{accFileName}",'r+')
accText = accFile.readlines()
accFile.close()

for line in accText:
    clients.append(0)
    lin = line.split('#')
    usernames.append(lin[0])
    passhashes.append(lin[1].strip())

def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except AttributeError:
            pass

def handle(client):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            message = '[{:%d-%m-%Y %H:%M}]'.format(datetime.datetime.now()) + f"<{usernames[clients.index(client)]}> {msg}"
            if len(msg) > 1:
                #logging
                logFile = open('msg.log', 'a')
                logFile.write(f"{message}\n")
                logFile.close()
                print(message)
                
                #send the message to everyone
                broadcast(message)
            if msg == '':
                #this should be triggered if the client becomes unreachable
                username=usernames[clients.index(client)]
                
                client.close()
                clients[clients.index(client)] = 0
                
                #logging
                message = '[{:%d-%m-%Y %H:%M}]'.format(datetime.datetime.now()) + f"{username} disconnected.\n"
                logFile = open('connect.log', 'a')
                logFile2= open('msg.log', 'a')
                logFile2.write(message)
                logFile.write(message)
                logFile.close()
                logFile.close()
                
                broadcast(message.replace('\n',''))
                
                print(f"{username} disconnected.")
                break
        except KeyboardInterrupt:
            pass
        
def receive():              
    while True:
        client, address = server.accept()

        client.send("LOGIN".encode('utf-8'))                 #requesting username from client
        logindata = client.recv(1024).decode('utf-8').split('#')         #taking their response
        username = logindata[0]
        passhash = logindata[1]
        
        try:
            usernames.index(username)
        except ValueError:
            client.send("BADUSERNAME".encode('utf-8'))
            client.close()
            continue
        
        if clients[usernames.index(username)] != 0: 
            client.send("ALREADYLOGGED".encode('utf-8'))
            client.close()
            continue
        
        try:
            passhashes.index(passhash)
        except ValueError:
            client.send("BADPASSWORD".encode('utf-8'))
            client.close()
            continue
        
        if usernames.index(username) == passhashes.index(passhash):
            client.send("OK".encode('utf-8'))
            
            clients[usernames.index(username)] = client
            try:
                logFile = open('msg.log', 'r')
                client.send(logFile.read().encode('utf-8'))
                logFile.close()
            except:
                pass
            
            address = address[0]
            
            msg1 = '[{:%d-%m-%Y %H:%M}]'.format(datetime.datetime.now()) + f"{username} connected to the server\n"
            msg2 = '[{:%d-%m-%Y %H:%M}]'.format(datetime.datetime.now()) + f"{username} connected to the server from {str(address)}\n"
            
            #logging
            logFile = open('msg.log', 'a')
            logFile2= open('connect.log','a')
            logFile.write(msg1)
            logFile2.write(msg2)
            logFile.close()
            logFile2.close()
            print(msg2)
            
            broadcast(msg1.replace('\n',''))

            thread = threading.Thread(target=handle, args=(client,))
            thread.daemon = True
            thread.start()
            
        elif usernames.index(username) != passhashes.index(passhash):
            client.send("BADPASSWORD".encode('utf-8'))
            client.close()


print ("Server running")
try:
    logFile = open('log.txt', 'r')
    print(logFile.read())
    logFile.close()
except:
    pass

try:
    receive()
except KeyboardInterrupt:
    broadcast('1')
    for client in clients:
        try:
            client.close()
        except AttributeError:
            pass
    server.close()
    print("\nServer is stopping")
    exit()
except BrokenPipeError or UnicodeDecodeError:
    for client in clients:
        try:
            client.close()
        except AttributeError:
            pass
    server.close()
    clients = []
    nicknames = []
    os.execv(sys.argv[0], sys.argv)
