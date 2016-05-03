#!/usr/bin/python
import socket
import sys
from urlparse import urlparse
#https://en.wikipedia.org/wiki/List_of_HTTP_header_fields


sysarg="";
arg_url="";
arg_ip="";
port=80;

for ( i, sysarg) in enumerate(sys.argv):
	if ( sysarg in ["--url", "-u"] ):
		arg_url=sys.argv[i+1];
        if ( sysarg in ["--host","-h"] ):
                arg_ip = sys.argv[i+1];
try:
	domain, page = arg_url.split("/");
except ValueError:
	domain = arg_url;
	page = "";

if ( arg_url == "" ):
	print "Usage:";
        print "./pysock.py --url www.desired.url --host des.ire.dho.st";
        print "./pysock.py -u www.desired.url -h des.ire.dho.st";
        print "./pysock.py -u www.desired.url";

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
except socket.error:
	print 'Failed to create socket';
	sys.exit();


	
try:
	remote_ip = socket.gethostbyname( domain );
except socket.gaierror:
	print 'Hostname could not be resolved. Exiting'
	sys.exit()


if ( arg_ip != "" ):
	print " Changing " + str(remote_ip)  + " in " + (arg_ip) + " for " + domain + " \n ";
	remote_ip = arg_ip;


http_command="GET";
#http_command="UAT";
http_version="HTTP/1.1";
http_ua="Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1";

message = http_command + " /" + page + " " + http_version + "\r\nConnection: Keep-Alive\r\n" + http_ua + "\r\nHost: " + domain + "\r\n\r\n"; 
print message;

s.connect((remote_ip, int(port)));

try:
	s.sendall(message)
except socket.error:
	print 'Send failed'
	sys.exit()

part = None;
reply = "";
while ( part != ""):
	part = s.recv(5575)
	reply += part;

out_file=open("out.html", "w");
out_file.write("");
out_file.close();
out_file=open("out.html", "a");


print reply;

out_file.close();
