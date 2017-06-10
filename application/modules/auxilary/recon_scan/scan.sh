# Gilbert Lynch
# last update 11/04/17
# Most usefull nmap and others
# Alpha version 0.000001 ;-)
argument=$1

if [ $# = 0 ]; then
	echo 1-[ip] ip - range
	echo 2-[ports][ftp][netbios][enum4linux][snmp][snmpwalk][dns][host][traceroute][enum][vuln][http][allhttp][whois][smb][discovery][smbbrute][brute][exploit][auth][safe][external][all][OS][name][nbtstat][malware][rdp][mail][firewall][telnet][httpserver][mysql][mssql][dirb][hash][hydra][ncrack][msrpc][nikto][niktoforce][apache][gobuster][myvpn][ssl][smtp][vnc][details][smbshare]
	echo 3-[force] - force brute - slow
	exit
fi
clear
printf "____________________________________________________\n\nScan %s\n" "$1"
if [ $# = 3 ]; then
	if [ $3 = 'force' ]; then
		if [ $2 = 'vuln' ]; then
			argument+=" --script-args=unsafe=1"
		else
			argument+=" -p- -sV --version-intensity 5 -T4 -Pn"
		fi
	fi
fi
case "$2" in
	"DNS")
		printf "Check DNS"
#		nmap --script=dns-service-discovery -p 5353 $argument ;;
# 		./dnsdb_query -p csv -i $argument | head
#		nmap --dns-servers 8.8.8.8,8.8.4.4 -sL $argument
#		nmap -sn -Pn $argument --script dns-check-zone --script-args='dns-check-zone.domain=google.com'
#	nmap -R $argument
#	nmap -system-dns $argument ;;
	arping -c 1 $argument ;;
	"ports")
		nmap -p- $1 ;;
	"httpserver")
		printf "Check http https server..."
		nmap -p80,443 $argument -oG - ;;
#		nmap -p80,443 $argument -oG - | nikto.pl -h - ;;
	"dns")
		printf "Check dns brute..."
		nmap $argument --script=dns-brute.nse ;;
	"mysql")
		printf "Check all mysql..."
		nmap $argument --script=mysql* ;;
	"mssql")
		printf "Check all mssql..."
		nmap $argument --script=ms-sql* ;;
	"host")
		printf "Check hosts..."
		nmap $argument --script=hostmap-bfk.nse  ;;
	"traceroute")
		nmap $argument --script=traceroute-geolocation.nse  ;;
	"enum")
		printf "Check http enum..."
		nmap $argument --script=http-enum  ;;
	"vuln")
		printf "check ALL vulnerability" 
		nmap $argument --script vuln ;;
	"http")
		printf "Check http..."
		curl -i -L $argument
		curl -i http://$argument/cgi-bin/admin.cgi
		url -i http://$argument/cgi-bin/admin.cgi -s | html2text
		nmap $argument --script=http-title | grep "|"
		nmap $argument --script=http-headers | grep "|"
		nmap $argument --script=http-enum  ;;
	"allhttp")
		printf "Check all http...slow"
		nmap $argument --script=http*  ;;
	"ftp")
#		nmap $argument --script=ftp-anon.nse
		printf "check ftp" 
		nmap $argument --script=ftp* ;;
#	"whois")
#		printf "Check whois..."
#		nmap $argument --script=asn-query,whois,ip-geolocation-maxmind ;;
	"smb")
		printf "check smb" 
		nmap $argument --script=smb-enum*
		nmap $argument --script=smb-os-discovery ;;
	"smbshare")
		printf "check smb shares" 
		nmap --script smb-enum-shares.nse -p445 $argument
		nmap -sU -sS --script smb-enum-shares.nse -p U:137,T:139 $argument ;;
	"discovery")
		printf "Check smb discovery..."
		nmap $argument 445 --script=smb-os-discovery  ;;
	"smbbrute")
		nmap $argument 445 --script=smb-brute  ;;
	"netbios")
		printf "Check netbios..."
		nmap -sU --script nbstat.nse -p 137 $argument
		nbtscan -r $argument ;;
	"enum4linux")
		enum4linux -a $argument ;;
	"exploit")
		printf "check ALL exploit" 
		nmap $argument --script exploit ;;
	"brute")
		printf "Check BRUTE attempts... passwords..." 
		nmap $argument --script brute ;;
	"auth")
		printf "Check auth" 
		nmap $argument --script auth ;;
	"safe")
		printf "Check not intrusive scripts..." 
		nmap $argument --script safe ;;
	"malware")
		printf "Check find open backdoor and malware..." 
		nmap $argument --script malware ;;
	"all")
		printf "Check ALL SCRIPTS!! slow results..." 
		nmap -sV $argument --script all ;;
	"default")
		printf "Check default scripts..." 
		nmap $argument --script default ;;
	"external")
		printf "Check external sources..." 
		nmap $argument --script external ;;
	"update")
		printf "update scripts..." 
		nmap --script-updatedb ;;
	"name")
		printf "Check names..."
		nmblookup -A $argument
		nmap --script smb-os-discovery -p 445 $argument
		nmap -sP $argument
		nbtscan -r $argument ;;
	"nbtstat")
		nmap --script nbstat.nse $argument ;;
	"OS")
		printf "Check Operating system..."
		nmap -O $argument ;;
	"rdp")
		printf "Check rdp" 
		nmap $argument --script rdp* ;;
	"ssh")
		printf "Check ssh" 
#		nc -nv $argument 22
		nmap $argument -p 22 -sV --script=ssh-hostkey
		nmap $argument --script ssh* ;;
	"mail")
		printf "Check mail" 
		nmap $argument --script pop3*
		nmap $argument --script smtp* ;;
	"firewall")
		printf "Check firewall" 
		nmap -sA $argument ;;
	"telnet")
		printf "Check telnet" 
		nmap $argument --script telnet* ;;
	"rpc")
		printf "Check rpc" 
		nmap $argument --script rpc* ;;
	"ssl")
		printf "Check ssl" 
		nmap $argument --script ssl* ;;
	"snmp")
		printf "Check snmp" 
		nmap $argument --script snmp* ;;
	"ncrack")
		printf "Check passwords"
		ncrack -vv -U username.txt -P password.txt $argument:$3 ;;
	"hydra")
		printf "Check passwords"
#		hydra -v -L username.txt -P password.txt -t ssh://$argument ;;
		hydra -v -L username.txt -P password.txt $argument ssh ;;

	"hash-sha")
		printf "Check hash"
		john --format=Raw-SHA1 $argument ;;
	"hash-md5")
		printf "Check hash"
		john --format=Raw-MD5 $argument ;;
	"hash")
		printf "Check hash"
		john $argument ;;
	"dirb")
		printf "Check http directory"
		dirb http://$argument big.txt ;;
	"gobuster")
		printf "Check http directory"
		gobuster -u http://$argument/ -w /usr/share/seclists/Discovery/Web_Content/cgis.txt -s '200,204,301,302,307,403,500' -e
		gobuster -u http://$argument/ -w /usr/share/seclists/Discovery/Web_Content/common.txt -s '200,204,301,302,307,403,500' -e ;;
	"apache")
		printf "Check Apache"
		nmap $argument --script http-apache* ;;
	"nikto")
		printf "Nikto check"
		nikto -host $argument ;;
	"niktoforce")
		printf "Nikto check all"
		nikto -C all -host $argument ;;
	"myvpn")
		printf "Check my vpn tunnel"
		ip addr show dev tap0 ;;
	"msrpc")
		printf "Check msrpc"
		nmap $argument --script msrpc-enum ;;
	"rpcbind")
		printf "Check rpc bind"
		nmap -sV $argument
		nmap $argument --script rpc-grind ;;
	"vnc")
		printf "Check vnc"
		nmap --script vnc-brute -p 5900 $argument ;;
	"details")
		printf "Check ports details"
		nmap -sV -sC $argument ;;
	"wordpress")
		printf "Check wordpress"
		nmap -sV --script http-wordpress-enum --script-args limit=25 $argument ;;
	"wpscan")
		printf "Scan wordpress"
		wpscan $argument ;;
	"wppass")
		printf "Pass check wordpress"
		wpscan -u $argument --wordlist /root/password.txt --username admin ;;

#	"snmpwalk")
#		snmpwalk -c public -v1 $argument
#		snmpwalk -c public -v1 $argument 1.3.6.1.2.1.25.6.3.1.2 ;;
	*)
		nmap $argument
esac
printf "____________________________________________________\n\nScan %s done\n" "$1"
#		printf "check SMB vulnerability" 
#		nmap $argument --script=smb-vuln*
#		printf "\ncheck RDP vulnerability" 
#		nmap $argument --script=rdp-vuln* 
#		printf "\ncheck MYSQL vulnerability " 
#		nmap $argument --script=mysql-vuln* 
#		printf "\ncheck SMTP vulnerability " 
#		nmap $argument --script=smtp-vuln* 
#		printf "\ncheck HTTP vulnerability" 
#		nmap $argument --script=http-vuln*
#		printf "\ncheck WORDPRESS vulnerability" 
#		nmap $argument --script=http-wordpress*
#		printf "\ncheck IRC vulnerability" 
#		nmap $argument --script=irc*
#		printf "\ncheck FTP vulnerability" 
#		nmap $argument --script=ftp*
#		printf "\ncheck SSL vulnerability" 
#		nmap $argument --script=ssl*
#		printf "\ncheck OSX vulnerability" 
#		nmap $argument --script=afp-path-vuln
#		printf "\ncheck FIREWALL vulnerability" 
#		nmap $argument --script=firewall-bypass 
#		printf "\ncheck SAMBA vulnerability" 
#		nmap $argument --script=samba-vuln* 

