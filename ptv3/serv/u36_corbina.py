#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, urllib2
import settings
import time
#-----------------------------------------
prov = 'corbina'
serv_id = '36'
provider = 'CRB_MSC'
port = 4022#1234

udpxylist = []

try:
	import xbmcaddon
	addon = xbmcaddon.Addon(id='ptv3')
	root_dir = addon.getAddonInfo('path')
except:
	root_dir = os.getcwd()


from threading import Thread
class MyThread(Thread):
	def __init__(self, param={}):
		Thread.__init__(self)
	
	def run(self):
		upd_xy()

def update():
		my_thread = MyThread()
		my_thread.start()


def test(url):
	urllib2.install_opener(urllib2.build_opener())
	try:
		response = urllib2.urlopen(url, timeout=1)
		r=response.getcode()
		data=response.read(128)
		if '404' in repr(data): r='404'
		if 'html' in repr(data): r='404'
		if r=='404': print 'BAD'
		else: print 'GOOD'
		return r
	except:
		print 'BAD'
		return '404'


def get_channels(n):
	try:
		sys.path.append(root_dir)
		import uxydb
		D = uxydb.get_info(n)
		return D
	except:
		return {'data': [], 'time':0}

def save_channels(n, L):
	try:
		sys.path.append(root_dir)
		import uxydb
		D={'data': L, 'time':time.time()}
		uxydb.add(n, D)
	except:
		print 'ERR ADD uxydb'

def get_ux_ip():
			global udpxylist
			import random
			if udpxylist == []: udpxylist = get_all_xy()#get_channels(provider)['data']
			uip = random.choice(udpxylist)
			return uip+':'+str(port)

def get_all_xy():
	LL=[]
	Lip = get_channels(provider+'/ip')
	for i in Lip:
		try:
			L=get_channels(provider+'/'+i)['data']
			LL.extend(L)
		except:
			pass
	return LL

def upd_xy_old():
	import random
	import scanxy
	Lip = get_channels(provider+'/ip')
	for i in range (3):
		pref = random.choice(Lip)
		print pref
		tm = get_channels(provider+'/'+pref)['time']
		if time.time()-tm > 360000:
			L=scanxy.scaner(provider, pref, port)
			save_channels(provider+'/'+pref, L)
			return L

def upd_xy():
	import random
	import scanxy
	Lip = get_channels(provider+'/ip')
	Lcn = get_channels(provider+'/cl')
	for i in range (3):
		pref = random.choice(Lip)
		print pref
		tm = get_channels(provider+'/'+pref)['time']
		if time.time()-tm > 360000:
			L=scanxy.scaner(provider, pref, port)
			Lr = []
			for uip in L:
				mcast = random.choice(Lcn)['url'].replace(prov+':','')
				udpxy = uip+':'+str(port)
				stream = 'http://%s/udp/%s\n' % (udpxy, mcast)
				print stream
				if test(stream) != '404':
					Lr.append(uip)
			save_channels(provider+'/'+pref, Lr)
			return L


class PZL:
	def Streams(self, url):
			print url
			mcast = url.replace(prov+':','')
			udpxy = settings.get(prov)
			stream = 'http://%s/udp/%s\n' % (udpxy, mcast)
			if test(stream) != '404': 
				return [stream,]
			else:
				for i in range(8): # проверкa альтернативных вариантов
						udpxy = get_ux_ip()
						stream = 'http://%s/udp/%s\n' % (udpxy, mcast)
						print stream
						if test(stream) != '404': 
							settings.set(prov, udpxy)
							return [stream,]
			return []
	
	def Canals(self):
			L = get_channels(provider+'/cl')
			update()
			return L