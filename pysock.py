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

#Classes

class urlMngr(object):
	arg_url = None;
	uri = None;
	proto = None;
	request_page = None;

	def __init__(self, url):
		self.arg_url = url;
		uri_splitlist = self.arg_url.split("/");

		if ( uri_splitlist[0][:-1] in [ "http", "https" ] ):
			self.proto = uri_splitlist[0][:-1];

		self.uri = uri_splitlist[2];
		self.request_page = "";
		for i in range(3, len(uri_splitlist)):
                	tmp_string = "/" + uri_splitlist[i];
                	self.request_page += tmp_string;
		
		if ( dbg ):
			print "\nUrlMNGR INIT:";
			print "Argument:\t" + str(self.arg_url);
			print "Protocol:\t" + str(self.proto);
			print "Uri:\t\t" + str(self.uri);
			print "Page:\t\t" + str(self.request_page);

	def getAll(self):
		return self.uri, self.proto, self.request_page;
	
	def getDomain(self):
		return self.uri;

	def getProto(self):
		return self.proto;

	def getWebPage(self):
		return self.request_page;
	

class socketMngr(object):
	socket = None;
	remote_ip = None;			# the IP mapped on domain by DNS
	requested_ip = None;			# the IP to which the request will be redirected
	source_ip = None;			# the spoofed SRC IP
	my_url_manager = None;
	

	def __init__(self,urlMngr,request_ip,spoof_ip):
		self.remote_ip = "";
		self.requested_ip = "";
		self.source_ip = "";
		self.socket = "";
		self.SSLsocket = "";
		self.my_url_manager = urlMngr;
		
		try:
			self.remote_ip = socket.gethostbyname( self.my_url_manager.getDomain() );
		except socket.gaierror:
			print 'Hostname could not be resolved. Exiting'
	                sys.exit()

		if ( request_ip != ""): 
			self.requested_ip = request_ip;
		else:
			self.requested_ip = self.remote_ip;

		if ( spoof_ip != ""): self.source_ip = spoof_ip;

		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
			self.setSocket();
       		except socket.error:
                	print "Failed to create socket";
        	
		if ( dbg ):
			print "\nsocketMNGR INIT:";
			print "remote_ip = " + str(self.remote_ip);
			print "requested_ip = " + str(self.requested_ip);
			print "source_ip = " + str(self.source_ip);
			print "urlManager.uri = " + str(self.my_url_manager.getDomain());
			print "urlManager.page = " + str(self.my_url_manager.getWebPage());
			print "urlManager.proto= " + str(self.my_url_manager.getProto());

	def setSocket(self):
		self.socket.settimeout(20);
        	if ( self.my_url_manager.getProto() == "https" ):
                	self.SSLsocket = ssl.wrap_socket(self.socket, ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ALL", server_side=0, cert_reqs=ssl.CERT_NONE);
                	self.SSLsocket.connect((self.requested_ip, 443));
        	elif ( self.my_url_manager.getProto() == "http" ):
                	self.socket.connect((self.requested_ip, 80));

	def mySend(self,message):
		if ( self.my_url_manager.getProto() == 'http'):
			try:
                		self.socket.sendall(message)
        		except socket.error:
                		print 'Send failed'
                		sys.exit()

        		
			part = None;
        		reply = "";
        		while ( part != ""):
                		part = self.socket.recv(5575)
                		reply += part;

        		self.socket.close();
		if ( self.my_url_manager.getProto() == 'https'):
                        try:
                                self.SSLsocket.sendall(message)
                        except socket.error:
                                print 'Send failed'
                                sys.exit()

                        
                        part = None;
                        reply = "";
                        while ( part != ""):
                                part = self.SSLsocket.recv(5575)
                                reply += part;

                        self.SSLsocket.close();
		return reply;

		

		
class webMngr(object):
	http_methods = ["GET", "HEAD", "CHECKOUT", "PUT", "DELETE", "POST", "LINK", "UNLINK", "CHECKIN", "TEXTSEARCH", "SPACEJUMP", "SEARCH",  "TRACE", "OPTIONS", "08HJAE98134"];
	http_options = {'version':"HTTP/1.1",'ua':"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1"};
	socketMngr = None;

	def __init__(self,socketManager):
		self.socketMngr = socketManager;
		print "\nwebMNGR INIT:";
		print "socketMngr.uri = " + str(self.socketMngr.my_url_manager.getDomain());
		print "socketMngr.proto = " + str(self.socketMngr.my_url_manager.getProto());

	def callPage(self,method):
		message = method  + " " + str(self.socketMngr.my_url_manager.getWebPage()) + " " + self.http_options['version'] + "\r\nConnection: Keep-Alive\r\n" + self.http_options['ua'] + "\r\nHost: " + str(self.socketMngr.my_url_manager.getDomain()) + "\r\n\r\n"; 

		return self.socketMngr.mySend(message);

# settings
dbg = 1;
methodloop_flag = 0;
stdout_body_flag = 0;
stdout_headers_flag = 0;
stdout_flag = 0;

	
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

arg_requested_url="";
arg_ip ="";
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


url = urlMngr(arg_requested_url);
s = socketMngr(url, arg_ip, "");
lynx = webMngr(s);
print lynx.callPage("GET");


'''

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
'''

####   END ###################################
