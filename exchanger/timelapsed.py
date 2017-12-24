#!/usr/bin/python

from maf_exchanger import Exchanger
import sys
import pprint
import os
import signal
import time
import os.path
import pwd
import socket 
from email.mime.text import MIMEText
from subprocess import Popen, PIPE
#import stat_ip
os.environ["LC_ALL"]="C"


def tick(exchanger):
	exchanger.log("Tick")

	restart_apache = False

#	if exchanger.first:
#		startfw(exchanger)

#	if exchanger.first or len(exchanger.getRows("select * from firewall where `update`='true' and `enabled`='true'")) > 0:
#		exchanger.log("Loading firewall")
#		exchanger.execute("/sbin/iptables -F Trusted")

	
def preview(exchang,data):
        exchanger.log("*POUF*");
        exchanger.execute("/usr/bin/raspistill -o /var/www/html/preview.jpg"); 

exchanger = Exchanger();

# Fixing broken apache
exchanger.log("Restarting apache twice to circumvent weird bug");

exchanger.addCommand("PREVIEW", preview, "Takes a preview picture");

#exchanger.addTimer(1,tick)
exchanger.run();

