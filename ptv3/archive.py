# -*- coding: utf-8 -*-
import os, sys, time, socket, json, urllib
import settings
try:
	import xbmcaddon, xbmc
	addon = xbmcaddon.Addon(id='ptv3')
	serv_dir = os.path.join(addon.getAddonInfo('path'),"arh")
	picon_dir = os.path.join(addon.getAddonInfo('path'),'logo')
	#UserDir = os.path.join(addon.getAddonInfo('path'), "user" )
	set=xbmcaddon.Addon(id='ptv3')
	set.setSetting("ptv",'3')
	UserDir = os.path.join(xbmc.translatePath("special://masterprofile/"),"addon_data","ptv3")
except:
	serv_dir = os.path.join(os.getcwd(), "arh" )
	picon_dir = os.path.join(os.getcwd(),'logo')
	UserDir = os.path.join(os.getcwd(), "user" )

#print serv_dir

UrlCashe={}
BanCashe=[]
Lthread=[]

try: port = settings.get('port')
except: port = 8185
if port=='': port = 8185


sys.path.append(serv_dir)
ld=os.listdir(serv_dir)
#print ld
Lserv=[]
for i in ld:
	if i[-3:]=='.py': Lserv.append(i[:-3])


sys.path.append(UserDir)

def save_d(d):
	try:
		fp=os.path.join(UserDir, 'arh.db')
		fl = open(fp, "w")
		fl.write(repr(d))
		fl.close()
	except:
		pass

def get_d():
	try:
		fp=os.path.join(UserDir, 'arh.db')
		fl = open(fp, "r")
		d=eval(fl.read())
		fl.close()
		return d
	except:
		return {}

link_cnl = get_d()

def save_BLs(BLs):
		fp=os.path.join(UserDir, 'BList.py')
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('BLs=[\n')
		for i in BLs:
			fl.write('"'+i+'",\n')
		fl.write(']\n')
		fl.close()

try: 
	from BList import *
except: 
	BLs=[]
	try: save_BLs(BLs)
	except: pass


def save_DBC(DBC):
		fp=os.path.join(UserDir, 'UserDBcnl.py')
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('DBC={\n')
		for i in DBC.items():
			fl.write("'"+i[0]+"':"+repr(i[1])+',\n')
		fl.write('}\n')
		fl.close()

sys.path.append(UserDir)
try: 
	from UserDBcnl import *
except: 
	from DBcnl import *
	try: save_DBC(DBC)
	except: pass

from DefGR import *


def fs_enc(path):
    sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
    return path.decode('utf-8').encode(sys_enc)

def fs_dec(path):
    sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
    return path.decode(sys_enc).encode('utf-8')

def lower(t):
	try:t=t.decode('utf-8')
	except: pass
	#try:t=t.decode('windows-1251')
	#except: pass
	#try:t=t.decode(sys.getfilesystemencoding())
	#except: pass
	try:t=t.lower().encode('utf-8')
	except: pass
	
	RUS={"А":"а", "Б":"б", "В":"в", "Г":"г", "Д":"д", "Е":"е", "Ё":"ё", "Ж":"ж", "З":"з", "И":"и", "Й":"й", "К":"к", "Л":"л", "М":"м", "Н":"н", "О":"о", "П":"п", "Р":"р", "С":"с", "Т":"т", "У":"у", "Ф":"ф", "Х":"х", "Ц":"ц", "Ч":"ч", "Ш":"ш", "Щ":"щ", "Ъ":"ъ", "Ы":"ы", "Ь":"ь", "Э":"э", "Ю":"ю", "Я":"я"}
	for i in range (65,91):
		t=t.replace(chr(i),chr(i+32))
	for i in RUS.keys():
		t=t.replace(i,RUS[i])
	t=t.lower()
	return t

def utf(t):
	try:t=t.decode('windows-1251')
	except: pass
	try:t=t.decode(sys.getfilesystemencoding())
	except: pass
	try:t=t.encode('utf-8')
	except: pass
	return t

def CRC32(buf):
		import binascii
		buf = (binascii.crc32(buf) & 0xFFFFFFFF)
		return str("%08X" % buf)

def mfind(t,s,e):
	r=t[t.find(s)+len(s):]
	r2=r[:r.find(e)]
	return r2

def uni_mark(nm):
	try:nm=lower(nm.strip())
	except:pass
	return nm

names_list = []
for mmm in DBC.items(): 
	#print mmm
	names_list.extend(mmm[1]['names'])

def get_ID(nm):
	id=CRC32(uni_mark(nm))
	if id in link_cnl.keys(): id=link_cnl[id]
	return id

def change_id(cid1, cid2):
	print cid2+' change_id_to '+cid1
	if cid1 == '000000': link_cnl.pop(cid2, '')
	else: link_cnl[cid2]=cid1
	save_d(link_cnl)

import urllib2
def test_url(url):
	if 'udp://' in url:  return '200'
	if 'rtmp://' in url: return '200'
	
	if url in BanCashe: return 404
	
	bld = [
	'/404/index.m3u8',
	'/405/index.m3u8',
	]
	
	for b in bld:
		if b in url: return '404'
	
	opener = urllib2.build_opener()
	urllib2.install_opener(opener)
	
	url=url.replace('ace/getstream?', 'ace/getstream?format=json&')
	print url
	try:
		response = urllib2.urlopen(url, timeout=5)
		if '/ace/' not in url: 
			r=response.getcode()
			#print r
			if r=='404': 
				BanCashe.append(url)
				#set_rating(url, 'bad')
				print 'BAD'
			else:
				#set_rating(url, 'good')
				print 'GOOD'
			return r
		else:
			r = response.read()
			#print r
			if 'X-STREAM' in r:
				print  '404 X-STREAM'
				return '404'
			if 'missing' in r: 
				BanCashe.append(url)
				print  '404 missing'
				return '404'
			else:
				null=None
				j=eval(r)['response']
				#print j
				stat_url = j['stat_url']
				print stat_url
				
				for n in range (8):
					try:
						time.sleep(1)
						response = urllib2.urlopen(stat_url, timeout=15)
						stat = eval(response.read())['response']['status']
						print stat
						if stat=='dl': return '200'
					except:
						pass
				
				return '404'


		#return response.getcode()
	except:
		return '404'


def GET(url):
	import urllib2
	opener = urllib2.build_opener()
	urllib2.install_opener(opener)
	try: response = urllib2.urlopen(url, timeout=15)
	except: response = ''
	return response

cahe_lists={}
def add_cahe_lists(s, t, c):
	cahe_lists[s]={'time': t, 'cahe': c}

def get_cahe_list(s):
		fp=os.path.join(serv_dir, s+'.cl')
		try: tm=os.path.getmtime(fp)
		except: tm=0
		if s in cahe_lists.keys():
			if cahe_lists[s]['time'] == tm:
				return cahe_lists[s]['cahe']
		
		fl = open(fp, "r")
		t=fl.read()
		fl.close()
		L=eval(t[t.find('['):t.rfind(']')+1])
		add_cahe_lists(s, tm, L)
		return L

def get_cahe_time(s):
		fp=os.path.join(serv_dir, s+'.cl')
		try: tm=os.path.getmtime(fp)
		except: tm=0
		if s in cahe_lists.keys():
			if cahe_lists[s]['time'] == tm:
				return tm
		try:
			fl = open(fp, "r")
			t=fl.read()
			fl.close()
			tm=eval(t[t.find('udata=')+6:])
		except:
			tm=0
			print 'ERR: get_cahe_time - '+s
		return tm

def save_channels(n, L):
		#print 'save'
		s=str(int(n))
		print 'save_arh-'+s+"-"+str(len(L))
		fp=os.path.join(serv_dir, s+'.cl')
		fl = open(fp, "w")
		fl.write('[\n')
		for i in L:
			fl.write(repr(i)+',\n')
		fl.write(']\n')
		fl.write('udata='+str(time.time()))
		fl.close()

def find_nm(nm):
		nm = uni_mark(nm)
		nm = nm.replace('-', ' ').replace('канал', '').replace('  ', ' ').strip()
		if nm in names_list: return nm
		
		if '(+' not in nm and '(' in nm: nm=nm[:nm.find('(')].strip()
		if nm in names_list: return nm
		
		return ''

def upd_canals_db(i):
	print 'upd_arh_db '+i
	exec ("import "+i+"; serv="+i+".ARH()")
	L=serv.name2id()
	
	LL=[]
	for k in L:
			id = get_ID(k['title'])
			if id not in DBC.keys():
				nm = find_nm(k['title'])
				if nm != '': k['title'] = nm
			LL.append(k)
	
	save_channels(i[1:3], LL)
	return LL

def get_all_archive():
	#print '==get_all_arh start=='
	D={}
	
	for i in Lserv:
			serv_id=str(int(i[1:3]))
			if settings.get("arh"+serv_id)!= 'false':
				#print serv_id
				try:   Ls=get_cahe_list(serv_id)
				except:Ls=[]
				if Ls==[]:
					utm = get_cahe_time(serv_id)
					#print utm
					if time.time()-utm > 600:
						try: Ls=upd_canals_db(i)
						except: Ls=[]
			else: Ls=[]
			
			D[i]=Ls
	#print '==get_all_arh end=='
	return D

def save_cache(name, cache, sd=0):
	try:
		sd=str(sd)
		DT={}
		if sd=="":sd='0'
		DT['time']=time.time()
		DT['cache']=cache
		fp=os.path.join(os.getcwd(), 'cache', get_ID(name+'_'+sd))
		fl = open(fp, "w")
		fl.write(repr(DT))
		fl.close()
	except: pass

def get_cache(name, sd=0):
	try:
		sd=str(sd)
		if sd=="":sd='0'
		fp=os.path.join(os.getcwd(), 'cache', get_ID(name+'_'+sd))
		fl = open(fp, "r")
		DT = eval(fl.read())
		fl.close()
		if time.time()-DT['time']<600: return DT['cache']
		elif time.time()-DT['time']<3600 and sd!='0': return DT['cache']
		else: return {}
	except:
		return {}


def archive(name, day=0):
	sname=name
	ssec=int(day)*24*60*60
	t=time.localtime(time.time() - ssec)
	#add_item ('[COLOR FF10FF10][B]'+time.strftime('%d.%m.%Y',t)+" - "+unmark(name)+"[/B][/COLOR]", "select_date", 'url', '0' )
	cash=get_cache(name, day)
	if cash!={}:
		print 'cache'
		da=cash
	else:
		print 'no cache'
		da={}
		Lm=[]
		Da=get_all_archive()
		for serv_id in Da.keys():
			cnl = Da[serv_id]
			exec ("import "+serv_id+"; arh="+serv_id+".ARH()")
			
			for cn in cnl:
				if uni_mark(cn['title'])==uni_mark(name):
					aid=cn['id']
					try:L=arh.Archive(aid, t)
					except: 
						print 'except: arh.Archive(aid, t)'
						L=[]
					for i in L:
						st=i['time']
						try: 
							i2=da[st]
							urls=i2['url']
							url=i['url']
							urls.append(url)
							i2['url']=urls
							da[st]=i2
						except: 
							url=i['url']
							i['url']=[url,]
							da[st]=i
		save_cache(name, da, day)
	return da

def archive_by_cid(CID, day=0):
	ssec=int(day)*24*60*60
	t=time.localtime(time.time() - ssec)
	cash=get_cache(CID, day)
	if cash!={}:
		print 'cache'
		da=cash
	else:
		print 'no cache'
		da={}
		Lm=[]
		Da=get_all_archive()
		for serv_id in Da.keys():
			if settings.get("arh"+serv_id)!= 'false':
				cnl = Da[serv_id]
				exec ("import "+serv_id+"; arh="+serv_id+".ARH()")
				
				for cn in cnl:
					#print CID
					if get_ID(cn['title'])==CID:
						#print CID
						#print 'ok'
						aid=cn['id']
						try: L=arh.Archive(aid, t)
						except: L=[]
						for i in L:
							st=i['time']
							#rec_id = get_ID(st+i['title'])+'|'+aid+'|'+str(day)
							rec_id = st.replace(':','-')+'_'+CID+'_'+str(day)
							try: 
								i2=da[st]
								urls=i2['url']
								url=i['url']
								urls.append(url)
								i2['url']=urls
								i2['id']=rec_id
								da[st]=i2
							except: 
								url=i['url']
								i['url']=[url,]
								i['id']=rec_id
								da[st]=i
						break
		save_cache(CID, da, day)
	return da

def archive_by_id(aid, day=0):
	ssec=int(day)*24*60*60
	t=time.localtime(time.time() - ssec)
	cash=get_cache(aid)
	if cash!={}:
		print 'cache'
		da=cash
	else:
		print 'no cache'
		da={}
		Lm=[]
		Da=get_all_archive()
		for serv_id in Da.keys():
			if settings.get("arh"+serv_id)!= 'false':
					exec ("import "+serv_id+"; arh="+serv_id+".ARH()")
					try:L=arh.Archive(aid, t)
					except: 
						print 'except: arh.Archive(aid, t)'
						L=[]
					#print aid
					for i in L:
						st=i['time']
						#rec_id = get_ID(st+i['title'])+'|'+aid+'|'+str(day)
						L2=Da[serv_id]
						CID = '00000000'
						for j in L2:
							if j['id'] == aid: 
								CID = get_ID(j['title'])
								break
						
						rec_id = st.replace(':','-')+'_'+CID+'_'+str(day)
						url= i['url']
						try: 
							i2=da[st]
							urls=i2['url']
							urls.append(url)
							i2['url']=urls
							i2['id']=rec_id
							da[st]=i2
						except: 
							i['url']=[url,]
							i['id']=rec_id
							da[st]=i
		save_cache(aid, da)
	return da

def get_archive(url):
	for i in Lserv:
		ids=i[4:]#.replace('_','-')
		if ids in url:
			try:
				exec ("import "+i+"; serv="+i+".ARH()")
				return serv.Streams(url)
			except: pass
	return []

def stream(url):
	try:   Lpurl=get_archive(url)
	except:Lpurl=[]
	
	if Lpurl==[]: return ""
	else:         return Lpurl[0]

def stream_by_id(uid):
	ip = settings.get('ip')
	Lid = uid.split('_')
	rid=Lid[0].replace('-',':')
	CID=Lid[1]
	day=Lid[2]
	L=archive_by_cid(CID, day)[rid]['url']
	Lpurl = []
	for url in L:
				try:   Lcurl=get_archive(url)
				except:Lcurl=[]
				for curl in Lcurl:
					if 'HLS:' in curl:
						import base64
						url = curl[4:]
						curl= 'http://'+ip+':'+str(port)+'/restream/'+base64.b64encode(url)
					return rec
	return ''

def streams(urls):
	Lpurl=[]
	for url in urls:
		try:   Lcurl=get_archive(url)
		except:Lcurl=[]
		try:   Lpurl.extend(Lcurl)
		except:pass
	
	return Lpurl

def streams_by_id_old(uid):
	ip = settings.get('ip')
	Lid = uid.split('_')
	#print Lid
	rid=Lid[0]
	aid=Lid[1]
	day=Lid[2]
	D=archive_by_id(aid, day)
	Lpurl = []
	for k in D.keys():
		itm=D[k]
		if itm['id'].split('_')[0]==rid:
			Lrec=itm['url']
			for url in Lrec:
				try:   Lcurl=get_archive(url)
				except:Lcurl=[]
				for curl in Lcurl:
					if 'HLS:' in curl:
						import base64
						url = curl[4:]
						curl= 'http://'+ip+':'+str(port)+'/restream/'+base64.b64encode(url)
					Lpurl.append(curl)
	return Lpurl

def streams_by_id(uid):
	ip = settings.get('ip')
	Lid = uid.split('_')
	rid=Lid[0].replace('-',':')
	CID=Lid[1]
	day=Lid[2]
	L=archive_by_cid(CID, day)[rid]['url']
	Lpurl = []
	for url in L:
				try:   Lcurl=get_archive(url)
				except:Lcurl=[]
				for curl in Lcurl:
					if 'HLS:' in curl:
						import base64
						url = curl[4:]
						curl= 'http://'+ip+':'+str(port)+'/restream/'+base64.b64encode(url)
					Lpurl.append(curl)
	return Lpurl


def channels():
	L=[]
	Lt=[]
	D=get_all_archive()
	for s in D.keys():
		lst=D[s]
		for i in lst:
			ut=uni_mark(i['title'])
			if ut not in Lt:
				Lt.append(ut)
				cid = get_ID(ut)
				L.append({'name':ut, 'id':i['id'],'cid':cid})
	return L

#for i in get_all_archive().keys():
#	print i
#time.sleep(5)

#print archive('Карусель', 0)
#time.sleep(5)
