#!/usr/bin/python
import socket
import sys
import random
from urlparse import urlparse
#https://en.wikipedia.org/wiki/List_of_HTTP_header_fields

# settings
dbg = 1;
protocol = None;
domain = None;
request_page = None;
http_methods = ["GET", "HEAD", "CHECKOUT", "PUT", "DELETE", "POST", "LINK", "UNLINK", "CHECKIN", "TEXTSEARCH", "SPACEJUMP", "SEARCH",  "TRACE", "OPTIONS", "08HJAE98134", "                                                                            " ]
http_options = ["HTTP/1.1","Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1"];
# global variables
arg_requested_url = None;
arg_ip = None;

# flags
methodloop_flag = 0;

# functions
def split_url(full_uri):
	uri_splitlist = full_uri.split("/");
	protocol = uri_splitlist[0][:-1];
	domain = uri_splitlist[2];
	request_page = "";

	for i in range(3, len(uri_splitlist)):
		tmp_string = "/" + uri_splitlist[i];
		request_page += tmp_string; 

	return protocol,domain,request_page;

def getAddr(domain):
	try:
        	remote_ip = socket.gethostbyname( domain );
	except socket.gaierror:
        	print 'Hostname could not be resolved. Exiting'
        	sys.exit()

	return remote_ip;	

def createSocket(protocol):
	if ( protocol == "https" ): print "suca";
	if ( protocol == "http" ):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
		except socket.error:
			print "Failed to create socket";
		return s;


def CallWebPage(domain, page, ip, method):

	s = createSocket(protocol);

	message = method  + " /" + page + " " + http_options[0] + "\r\nConnection: Keep-Alive\r\n" + http_options[1] + "\r\nHost: " + domain + "\r\n\r\n"; 
	s.connect((ip, 80));

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
			print methodloop_flag;

if ( arg_requested_url != None ):
	protocol, domain, request_page = split_url(arg_requested_url);	

if ( methodloop_flag != 1 ):
	remote_ip = getAddr(domain);

	headers,body = CallWebPage(domain, request_page, remote_ip, http_methods[0]);

	id = str(random.randint(00000000,99999999));
	bname = domain+"-"+id+".out";
	hname = domain+"-headers-"+id+".out";
	
	out_file=open(bname, "w");
	out_file.write(body);
	out_file.close();
	
	out_file=open(hname, "w");
	out_file.write(headers);
	out_file.close();
else:
	for method in http_methods:
		print method;
		remote_ip = getAddr(domain);
	        headers,body = CallWebPage(domain, request_page, remote_ip, method);

        	id = str(random.randint(00000000,99999999));
        	bname = domain+"-"+id+"-"+method+".out";
        	hname = domain+"-headers-"+id+"-"+method+".out";

		print "";
		print headers;
        	out_file=open(bname, "w");
        	out_file.write(body);
        	out_file.close();

        	out_file=open(hname, "w");
        	out_file.write(headers);
        	out_file.close();


####   END ###################################
