# -*- coding: utf-8 -*-
"""
Created on Tue May 10 20:08:28 2022

@author: annam
"""

import socket
import threading                                               

host = '127.0.0.1'                                                      
port = 55555                                                          

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#binding host and port to socket        
server.bind((host, port))                                               
server.listen()

clients = []
nicknames = []

#broadcast function declaration
def broadcast(message):                                                 
    for client in clients:
        client.send(message)

def handle(client):                                         
    while True:
        try:                                                            
            msg = message = client.recv(1024)
            if msg.decode('ascii').startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':
                    kickName = msg.decode('ascii')[5:]
                    print("see whether the name is crctly extracted ")
                    print(kickName)
                    kickUser(kickName)
                else:
                    client.send('Command was refused!'.encode('ascii'))
            else:
                broadcast(message)


        except:
            #removing clients
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast('{} left!'.format(nickname).encode('ascii'))
                nicknames.remove(nickname)
                break

def receive(): 
    #accepting multiple clients                                                         
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')
        #print("Connected with {}".format(str(address)))
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        #check if client is admin
        if nickname == 'admin':
            client.send('PASS'.encode('ascii'))
            pwd = client.recv(1024).decode('ascii')

            #check if pwd is crct or not
            #if not close the client thread and inform it as a wrng pwd
            if pwd != 'admin':
                client.send('REFUSE '.encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)
        print(f'Nickname is {nickname}')
        broadcast(f'{nickname} joined!'.encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kickUser(kickName):
    if kickName in nicknames:
        ind = nicknames.index(kickName)
        clientToKick = clients[ind]
        clients.remove(clientToKick)
        clientToKick.send('YOU HAVE BEEN KICKED BY ADMIN'.encode('ascii'))
        clientToKick.close()
        nicknames.remove(kickName)
        #telling clients in server that "kickName" has been removed
        broadcast(f'{kickName} was kicked by admin.')

print('server is listening...')
receive()