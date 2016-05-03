#!/usr/bin/python
import socket
import sys
from urlparse import urlparse

# get $Url from $Ip what DNS says about it.


def Caller(url, ip):
	port = 80;
	url, page = url.split('/');
	
	try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        except socket.error:
                print 'Failed to create socket';
                sys.exit();

        try:
                remote_ip = socket.gethostbyname( url );
        except socket.gaierror:
                # print 'Hostname could not be resolved. Exiting'
                sys.exit()

	print url;
	print page;
	if ( ip != '' ):
                remote_ip = ip;

        s.connect((remote_ip, int(port)))
        message="GET /" + page + " HTTP/1.1\r\nConnection: Keep-Aliver\nUser-Agent: Mozilla/5.0 (compatible; Konqueror/3.2; Linux) (KHTML, like Gecko)\r\nHost:  "  + url + "\r\n\r\n";
	
	print "*****************";
	print message;
	print "*****************";

	try:
                s.sendall(message)
        except socket.error:
                print 'Send failed'
                sys.exit()

        reply = s.recv(5575)
        l = reply.split('\r\n');
        line_number = 0;

	print l;	

##############################################

arg_length=len(sys.argv);
print arg_length;
if ( arg_length < 5 ): 
	print "	Usage:"
	print "	pysock.py --url $url --ip $ip";

sysarg="";
_url="";
_ip="";
for (i, sysarg) in enumerate(sys.argv):
	if ( sysarg in ["--url","-u"] ):
		_url = sys.argv[i+1];
	if ( sysarg in ["--host","-h"] ):
		_ip = sys.argv[i+1];
if ( _url == "" ):
	print "Usage:"
	print "./pysock.py --url www.desired.url --host des.ire.dho.st";
	print "./pysock.py -u www.desired.url -h des.ire.dho.st";
	print "./pysock.py -u www.desired.url";
else:
	Caller(_url,_ip);

##############################################





'''
def callit(url, ip):
	hostname=url;
	port=80

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	except socket.error:
		print 'Failed to create socket';
		sys.exit();
	
	try:
		remote_ip = socket.gethostbyname( hostname );
	except socket.gaierror:
		# print 'Hostname could not be resolved. Exiting'
		sys.exit()
	
	if ( ip != '' ):
		remote_ip = ip;

	s.connect((remote_ip, int(port)))
	message="GET / HTTP/1.1\r\nConnection: Keep-Aliver\nUser-Agent: Mozilla/5.0 (compatible; Konqueror/3.2; Linux) (KHTML, like Gecko)\r\nHost:  "  + hostname + "\r\n\r\n";


	try:
		s.sendall(message)
	except socket.error:
		print 'Send failed'
		sys.exit()

	reply = s.recv(5575)
	l = reply.split('\r\n');
	line_number = 0;

	print "Got Reply!"

	for line in l:
		if "Location" in line:
			new_url=urlparse(line.split(' ')[1]);
			print "***************** Searching " + new_url[1] + "*****************\n";
			callit (new_url[1], "");

	if not "Location" in reply:
		print reply;	

'''
