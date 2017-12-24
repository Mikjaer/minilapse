#!/usr/bin/python

import subprocess
import datetime
import socket
import thread
import threading
import signal, os,sys, time
import setproctitle
import pprint
import syslog
import errno
from socket import error as socket_error


import time
import sys
import signal
# apt-get install python-setproctitle

running = True

class Exchanger:
	def __init__(self):
		self.port = 1337;
		self.listen = "127.0.0.1";
		self.procname = "timelapsed";
		self.running = True;
		self.appname = "Timelapsed 1.0";
		self.cmds = []
		self.timers = []
		self.conn = "";
		self.first = True
		self.boot = int(time.time()) 

		if len(sys.argv)>1:
			if sys.argv[1] == "--keepalive":
				if self.allready_running():	
					sys.exit()		# If we are allready running, quit silently and do nothing

	
	def log(self,msg):
		syslog.openlog(self.procname)
		syslog.syslog(msg)

	def userExists(self,user):
		try:
			pwd.getpwnam(user)
			return True
		except:
			return False
        
        def execute(self,cmd):
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                out, err = p.communicate()
                self.log("Execute: "+cmd);
                if not out == "": 
                                            self.log("Out:"+out);
                if not err == "":    
                                            self.log("Err:"+err);



	def socket_init(self):
		try:
			ADDR = (self.listen, self.port)
			serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			serversock.bind(ADDR)
			serversock.listen(5)
		except:
			msg = "Could not listen to "+self.listen+":"+str(self.port)
			print msg+"\n";
			self.log(msg)
			sys.exit()

		while self.running:
			try:
				#print "Waiting for connection..."
				clientsock, addr = serversock.accept()
				if self.running:
					self.log('...connected from:'+ str(addr))
					thread.start_new_thread(self.socket_handler, (serversock, clientsock, addr))
				else:
					serversock.close();
			except socket.error as (code, msg):
				if code != errno.EINTR:
					raise
			
			except:
				if str(sys.exc_info()[0]) != "<type 'exceptions.SystemExit'>":	
					self.log("Unexpected error (socket_init):"+ str(sys.exc_info()[0]))
					raise

	def allready_running(self): 
        	try:
        	        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        	        s.connect(( self.listen , self.port )); 
        	        s.send("PING");
        	        ret = s.recv(1024);
        	        ret = ret + s.recv(1024);
        	        if "PONG" in ret:
        	                return True;
        	        self.log("Keepalive: Forbindelsen lykkedes, men svar ikke korrekt.")
        	        print sys.exc_info()[0]
        	        sys.exit()      # Ingen grund til at forsoege en start naa porten er optaget
        	        return False;
      	  	except socket_error as serr:
      	          	self.log("Keepalive: Forbindelsen fejlede.[Socket error "+str(serr.errno)+"]")
        		return False;
		except:
                	self.log("Noget fejlede.:"+sys.exc_info()[0])
			return False;		


	def socket_handler(self,serversock, clientsock,addr):
		while 1:
			try:
			        clientsock.send(">");
				data = clientsock.recv(1024).strip('\r\n')
			except:
				self.log("Connect from "+str(addr)+" with no payload?")
				return False

			if data.upper() == "HELP":
				clientsock.send(self.appname+" help:\n\n");
				clientsock.send("HELP - Shows this text\n");
				for item in self.cmds:
					clientsock.send(item["cmd"].upper()+" - "+item["helptext"]+"\n");
				clientsock.send("QUIT - Disconnects\n");
				clientsock.send("PING - Answers `PONG` (used internally)\n");
				clientsock.send("SHUTDOWN - Exits exchanger (will probably start autostart again\n");
				clientsock.send("           unless you prevent it) \n");
			elif data.upper() == "QUIT":	
				clientsock.close();
				break	
			elif data.upper() == "PING":
				clientsock.send("PONG");
				clientsock.close();
				break;
			elif data.upper() == "SHUTDOWN":
				self.log("Shutdown initiated through socket")
				clientsock.close();
				self.running = False	
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect(( self.listen , self.port ));
				break;
			else:		
				for item in self.cmds:
					if item["cmd"].upper() == data.partition(' ')[0].upper():
						item["method"](clientsock,data)
	def run(self):
		signal.signal(signal.SIGTERM, self.signal_handler) 
		pid = os.fork()
		if pid == 0:
			self.log("Starting "+self.appname)
			setproctitle.setproctitle(self.procname);
			for t in self.timers:
				thread.start_new_thread(self.timer, (t["interval"], t["method"])) 
			self.socket_init()

	def signal_handler ( self, signal, frame ):
		self.log("SIGTERM Received, shutting down exchanger")
		self.running == False
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(( self.listen , self.port ));
		s.send("SHUTDOWN")

	def timer(self,interval,method):
		while (True):
			method(self)
			time.sleep(interval)
			self.first = False

	def addCommand(self,cmd,method,helptext):
		self.cmds.append({
			'cmd':cmd,
			'method':method,
			'helptext':helptext
		});

	def addTimer(self,interval,method):
		self.timers.append({
			'interval':interval,
			'method':method
		});

