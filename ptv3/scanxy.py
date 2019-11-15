#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import sys
import socket

def scan_port(ip, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(0.5)
	try:
		connect = sock.connect((ip,port))
		print ip+':'+str(port)
		IPlist.append(ip)
		connect.close()
	except:
		pass


from threading import Thread
class MyThread(Thread):
	def __init__(self, param):
		Thread.__init__(self)
		self.ip = param['ip']
		self.port = param['port']
	
	def run(self):
		scan_port(self.ip, self.port)
		CT.append(self.ip)

def create_thread(param):
		my_thread = MyThread(param)
		my_thread.start()

def scaner(provider, pref, port):
		try:
			import settings
			limit = int(settings.get('scan_limit'))
		except:
			limit = 15
		print '-- SCAN - '+provider+' '+pref+'.x.x LIMIT '+str(limit)+' --'
		global IPlist
		IPlist = []
		global CT
		CT = []
		TT = 0
		for n3 in range(255):
			print n3
			for n4 in range(255):
				ip = pref+'.'+str(n3)+'.'+str(n4)
				if limit == 1:
					scan_port(ip, port)
				else:
					if TT-len(CT) < limit:
						create_thread({'ip':ip, 'port':port})
						TT+=1
						time.sleep(0.01)
					else:
						time.sleep(1)
		print '-- SCAN - END --'
		return IPlist
