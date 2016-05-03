#!/usr/bin/python
#
# Sorry for potato quality
#

import socket
import sys
import random
import ssl 
from urlparse import urlparse
#https://en.wikipedia.org/wiki/List_of_HTTP_header_fields

# settings
dbg = 1;
protocol = None;
domain = None;
request_page = None;
http_methods = ["GET", "HEAD", "CHECKOUT", "PUT", "DELETE", "POST", "LINK", "UNLINK", "CHECKIN", "TEXTSEARCH", "SPACEJUMP", "SEARCH",  "TRACE", "OPTIONS", "08HJAE98134"];
http_options = {'version':"HTTP/1.1",'ua':"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1"};
# global variables
arg_requested_url = None;
arg_ip = None;

# flags
methodloop_flag = 0;
stdout_body_flag = 0;
stdout_headers_flag = 0;
stdout_flag = 0;

# functions
def split_url(full_uri):
	uri_splitlist = full_uri.split("/");
	protocol = uri_splitlist[0][:-1];
	domain = uri_splitlist[2];
	request_page = "";

	for i in range(3, len(uri_splitlist)):
		tmp_string = "/" + uri_splitlist[i];
		request_page += tmp_string; 

	if ( protocol not in ["http", "https"] ):
		print "Wrong protocol " + protocol;
		sys.exit();
	return protocol,domain,request_page;

def getAddr(domain):
	try:
        	remote_ip = socket.gethostbyname( domain );
	except socket.gaierror:
        	print 'Hostname could not be resolved. Exiting'
        	sys.exit()

	return remote_ip;	

def createSocket(protocol, ip):
	if ( protocol == "https" ):

		try:
        		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
 	       	except socket.error:
        		print "Failed to create socket";
		
		wrappedSocket = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ALL", server_side=0, cert_reqs=ssl.CERT_NONE);
		wrappedSocket.connect((ip, 443));
		return wrappedSocket;

	elif ( protocol == "http" ):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
		except socket.error:
			print "Failed to create socket";

		s.connect((ip, 80));
		return s;


def CallWebPage(domain, page, ip, method):

	s = createSocket(protocol, ip);

	message = method  + " /" + page + " " + http_options['version'] + "\r\nConnection: Keep-Alive\r\n" + http_options['ua'] + "\r\nHost: " + domain + "\r\n\r\n"; 

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

	s.close();

	headers = "";
	body = "";
	headers_ended = 0;


	for line in reply.splitlines():
		if ( headers_ended == 0 ):
			if ( line == '' ):
				headers_ended = 1;
				continue;
			line_forprint=line +"\r\n";
			headers += line_forprint;
		else:
			if ( line == ''): continue;
			else:
				line_forprint = line + "\r\n";
				body += line_forprint;
	return headers,body;


def antibodi(body, headers):
	id = str(random.randint(00000000,99999999));
        bname = domain+"-"+id+".out";
        hname = domain+"-headers-"+id+".out";

        print "";
        if ( stdout_body_flag or stdout_headers_flag ):
                print "Domain:\t\t" + domain;
                print "Page:\t\t" + request_page;
                print "Real Ip:\t" + remote_ip;
                print "Request Ip:\t" + ip;

                if ( stdout_headers_flag ):
                        print "Headers:\n";
                        print headers;
                if ( stdout_body_flag ):
                        print "\nBody:\n";
                        print body;
        else:
                out_file=open(bname, "w");
                out_file.write(body);
                out_file.close();
                out_file=open(hname, "w");
                out_file.write(headers);
                out_file.close();

	

####### MAIN ##########################

# get args
if ( len(sys.argv) > 1 ):
	for ( i, sysarg) in enumerate(sys.argv):
        	if ( sysarg in ["--url", "-u"] ):
                	arg_requested_url=sys.argv[i+1];
        	if ( sysarg in ["--host", "-h"] ):
                	arg_ip=sys.argv[i+1];
		if ( sysarg in ["--loopmethods", "-lp"] ):
			methodloop_flag = 1;
		if ( sysarg in ["--stdout-body", "-sob"] ):
			stdout_body_flag = 1;
		if ( sysarg in ["--stdout-headers", "-soh"] ):
			stdout_headers_flag = 1;

if ( arg_requested_url != None ):
	protocol, domain, request_page = split_url(arg_requested_url);	

ip = None;

if ( methodloop_flag != 1 ):
	remote_ip = getAddr(domain);
	if ( arg_ip != None ): ip = arg_ip;
	else: ip = remote_ip;

	headers,body = CallWebPage(domain, request_page, ip, http_methods[0]);

	antibodi(body,headers);
else:
	for method in http_methods:
		print method;
		remote_ip = getAddr(domain);
		if ( arg_ip != None ): ip = arg_ip;
		else: ip = remote_ip;
	        headers,body = CallWebPage(domain, request_page, ip, method);
		antibodi(body, headers);

####   END ###################################
