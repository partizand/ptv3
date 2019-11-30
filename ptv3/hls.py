# -*- coding: utf-8 -*-
import urllib2, time, cookielib, os
sid_file = os.path.join(os.getcwd(), 'hls.sid')

cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 
urllib2.install_opener(opener) 

def mfind(t,s,e):
	r=t[t.find(s)+len(s):]
	r2=r[:r.find(e)]
	return r2

def get_UA(url):
	L=[['peers.tv','DuneHD/1.0.3'],]
	for i in L:
		if i[0] in url: return i[1]
	return 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60'

def CRC32(buf):
		import binascii
		buf = (binascii.crc32(buf) & 0xFFFFFFFF)
		return str("%08X" % buf)

def save_cache(url, cache):
	try:
		fp=os.path.join(os.getcwd(), 'cache2', CRC32(url))
		fl = open(fp, "wb")
		fl.write(cache)
		fl.close()
	except: pass

def get_cache(url):
	try:
		fp=os.path.join(os.getcwd(), 'cache2', CRC32(url))
		fl = open(fp, "r")
		DT = fl.read()
		fl.close()
		return DT
	except:
		return None

class HLS():
	def __init__(self, hls_url, header='', list_index = -1):
		self.header = header
		if list_index != -1:
			self.reconnect = True
		else:
			self.reconnect = False
		self.hls_head = ''
		self.hls_url = hls_url
		self.hls_list = []
		self.list_index = list_index
		self.hls_complit = []
		self.hls_n = 0
		self.buf = None
		self.br_n = 0

	def GET(self, url, Referer = 'http://ya.ru/'):
		#cache=get_cache(url)
		#if cache!=None: return cache
		try:
			urllib2.install_opener(urllib2.build_opener()) 
			req = urllib2.Request(url)
			UA = get_UA(url)
			req.add_header('User-Agent', UA)
			#req.add_header('User-Agent', 'SmartSDK')
			#|User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:35.0) Gecko/20100101 Firefox/35.0
			req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
			req.add_header('Accept-Language', 'ru,en;q=0.9')
			response = urllib2.urlopen(req, timeout=3)
			data=response.read()
			response.close()
			#save_cache(url, data)
			return data
		except:
			return None

	def get_sublist(self, resp):
		print 'X-STREAM'
		if resp == None: return ''
		if 'X-STREAM' not in resp: return ''
		list=resp.splitlines()
		link = ''
		for i in list:
			if '#' not in i:
				if len (i)>5:
					link = i
					if 'zabava' in link: return link
		return link

	def get_list(self, url):
		
		#print 'get_list'
		resp=self.GET(url)
		if resp==None: return []
		if 'X-MEDIA-SEQUENCE' in resp:
			try:index = int(mfind(resp, 'MEDIA-SEQUENCE:', '\n'))
			except: index = -1
			if index-self.list_index < 2 and index >2 : return []
			if index==self.list_index and self.reconnect == False: return []
			else: self.list_index=index
			print index
		
		if 'X-STREAM' in resp: 
			h = self.get_head(url)
			url = self.get_sublist(resp)
			if 'http' not in url: url=h+url
			#print url
			self.hls_url = url
			resp=self.GET(url)
		
		if resp == None: return []
		if '#EXTINF' not in resp: return []
		list=resp.splitlines()
		
		L=[]
		h = self.get_head(url)
		for i in list:
			if '#' not in i :#and len (i)>5
					#if len(L)<5: print i
					if i[:4]=='http': L.append(i)
					else:             L.append(h+i)
					
		#if self.reconnect:
		#	for i in L:
		#		self.hls_complit.append(i)
		#	self.reconnect = False
		#	return []
		#L.sort()
		return L

	def get_head(self, url=''):
		if url=='': url=self.hls_url
		if 'peers.tv' in url or '178.162' in url:#/var
			t1 = url[:url.find('://')+3]
			t2 = mfind(url, '://', '/')
			return t1+t2
		else:
			return url[:url.rfind('/')+1]
		
	def get_data2(self):
		#print '============= get_data ==============='
		if self.hls_n+1>=len(self.hls_list): 
			self.hls_list = []
			self.hls_n = 0
		
		if self.hls_list == []: 
			#print self.hls_url
			list = self.get_list(self.hls_url)
			if list == []: return None#'error '+str(self.list_index)
			else: self.hls_list = list
		
		L=self.hls_list
		if self.hls_head == '':
			head = self.get_head()
			self.hls_head = head
		else:
			head = self.hls_head
		
		#print head
		if L[self.hls_n][:4]!='http': data_url = head+L[self.hls_n]
		else:						  data_url = L[self.hls_n]
		
		print data_url#[-20:]
		if data_url not in self.hls_complit:
			
			data = self.GET(data_url, head)
			if data != None:
				self.hls_n+=1
				self.hls_complit.append(data_url)
			else:
				print 'ERR'
		else:
			print '- complit'
			self.hls_n+=1
			time.sleep(0.3)
			data = None
		
		return data
	
	def get_data(self):
		block_sz = 8192
		if self.buf == None:
			self.buf = self.get_data2()
			if self.buf == None: return None
		elif len(self.buf)< block_sz:
			dt = self.get_data2()
			if dt!=None:
				self.buf = self.buf+dt
			else: return None
		
		data = self.buf[:block_sz]
		self.buf=self.buf[block_sz:]
		return data

#sHLS = HLS('https://strm.yandex.ru/kal/fashiontv/fashiontv0_169_1080p.json/index-v1-a1.m3u8?partner_id=270171&target_ref=https%3A%2F%2Fyastatic.net&uuid=42ee5f579c38ea04a6d92ccefdbeed99&vsid=ojhxcxb2wxf48pv&redundant=5')
#sHLS.get_data()
#sHLS.get_data()
#sHLS.get_data()
#get_data('https://strm.yandex.ru/kal/fashiontv/fashiontv0_169_1080p.json/index-v1-a1.m3u8?partner_id=270171&target_ref=https%3A%2F%2Fyastatic.net&uuid=42ee5f579c38ea04a6d92ccefdbeed99&vsid=ojhxcxb2wxf48pv&redundant=5')