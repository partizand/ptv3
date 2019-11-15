# -*- coding: utf-8 -*-
import socket, time, urllib2, os
try:
	import _winreg
	try:
		t = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\AceStream')
	except:
		t = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\TorrentStream')
	port_file = os.path.join(os.path.dirname(_winreg.QueryValueEx(t, 'EnginePath')[0]), r'acestream.port')
	gf = open(port_file, 'r')
	tsport=int(gf.read())
except:
	tsport=62062


sock = None
#tsport=57814
def INIT():
	global sock
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1)
	sock.connect(('127.0.0.1', tsport))


def mfind(t,s,e):
	r=t[t.find(s)+len(s):]
	r2=r[:r.find(e)]
	return r2


def PUSH(command):
			print ('> ' + command)
			try:
				sock.send(command + '\r\n')
				return True
			except:
				return False

def RECV():
			try: return sock.recv(65 * 1024)
			except: return ''

def CONNECT():
	pkey = 'n51LvQoTlJzNGaFxseRK-uvnvX-sD4Vm5Axwmc4UcoD-jruxmKsuJaH0eVgE'
	import hashlib
	sha1 = hashlib.sha1()
	PUSH('HELLOBG version=3')
	r=''
	for i in range(5):
		r = RECV()
		if r != '': break
		time.sleep(1)
	if r == '': return ''
	
	if 'key=' in r: key = mfind(r, 'key=', ' ')
	else: return ''
	
	sha1.update(key + pkey)
	key = sha1.hexdigest()
	pk = pkey.split('-')[0]
	ready_key = 'READY key=%s-%s' % (pk, key)
	PUSH(ready_key)
	
	r=''
	for i in range(20):
		r = RECV()
		if r != '': break
		time.sleep(0.5)
		
	if r == '': return ''
	return r


def STATE():
	print 'GET_STATE'
	PUSH('STATE')
	r=''
	for i in range (3):
		r = RECV()
		if r != '': break
		time.sleep(0.5)
	print r
	print '================'
	return r

def STATUS():
	#state; total_progress; immediate_progress; speed_down; http_speed_down; speed_up; peers; http_peers; downloaded; http_downloaded; uploaded
	#print 'STATUS'
	PUSH('STATE')
	r=''
	for i in range (3):
		r = RECV()
		if r != '': break
	for i in r.splitlines():
		d = {'state':'', 'speed':0, 'load':0, 'upload':0}
		if 'STATUS' in i:
			i=i.replace('STATUS ','')
			p = i.split(';')
			try: d['state']=p[0]
			except: pass
			try: d['speed']=float(p[3])
			except: pass
			try: d['load']=int(p[8])
			except: pass
			try: d['upload']=int(p[10])
			except: pass
			#print d
	print '================'
	return d

def START(PID):
	INIT()
	r=CONNECT()
	print "CONNECT "+r

	if r != '':
		PUSH('START PID '+PID+' 0')
		purl = ''
		for i in range(90):
			time.sleep(0.3)
			st = STATE()
			if st == '': return ''
			if 'START' in st: 
				purl = mfind(st, 'START ', ' ')
				break
		if purl=='': 
			STOP()
			return ''
		PUSH('PLAYBACK '+purl+' stream=1')
		return purl
	else:
		print 'NO KEY'
		STOP()
		return ''

def STOP():
	PUSH('SHUTDOWN')
	sock.shutdown(socket.SHUT_RDWR)
	sock.close()

class P2P():
	def __init__(self, PID):
		self.PID = PID
		url=START(PID)
		if url == '': return 'ERR'
		opener = urllib2.build_opener()
		urllib2.install_opener(opener)
		self.req = urllib2.Request(url)
		self.resp = urllib2.urlopen(self.req, timeout=0.2)
		self.url = url
		self.size_dl = 0
		self.buf = 128#1024#81920
		
	def GET(self):
		try: data=self.resp.read(self.buf)
		except: 
			data=None
		return data

	def get_data(self):
		if self.url == '': return 'ERR'
		data=self.GET()
		if data!=None:
			if len(data)<self.buf: data=None
		if data==None:
			try:    
				self.resp = urllib2.urlopen(self.req, timeout=0.1)
				data=self.GET()
				if len(data)<self.buf: data=None
			except:
				data=None
		return data
	
	def END(self):
		try:
			PUSH('SHUTDOWN')
			sock.shutdown(socket.SHUT_RDWR)
			sock.close()
		except: pass
