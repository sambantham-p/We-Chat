# -*- coding: utf-8 -*-
"""
Created on Tue May 10 20:08:27 2022

@author: annam
"""

import socket
import threading
nickname = input("Choose your Nickname: ")

#if nickname is admin .. pwd should be entered
if nickname == 'admin':
    pwd = input('Enter password for admin : ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 #connecting client to server   
client.connect((socket.gethostname(), 55555))                            

#boolean global variable
stop_thread = False
def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                nxt_msg = client.recv(1024).decode('ascii')
                if nxt_msg == 'PASS':
                    client.send(pwd.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Wrong password !! Connection is refused to establish.")
                        stop_thread = True
                        #admin connection is stopped
            else:
                print(message)
        except:                                                
            print("An error occured!")
            client.close()
            break
def write():
    while True:
        if stop_thread:
            break
        message = f'{nickname}: {input("")}'
        # nickname: /command
        if message[len(nickname)+2:].startswith('/'):
            #Only admin has rights to kick any client
            #check whether the client is admin or not
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))

            else:
                print("Only admins are allowed to use commands!!")
        else:
            client.send(message.encode('ascii'))


#receiving multiple messages
receive_thread = threading.Thread(target=receive)               
receive_thread.start()
write_thread = threading.Thread(target=write)                   
write_thread.start()
