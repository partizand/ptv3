# -*- coding: utf-8 -*-
import os, sys, time, socket, json
import settings
try:
	import xbmcaddon, xbmc
	addon = xbmcaddon.Addon(id='ptv3')
	serv_dir = os.path.join(addon.getAddonInfo('path'),"serv")
	picon_dir = os.path.join(addon.getAddonInfo('path'),'logo')
	#UserDir = os.path.join(addon.getAddonInfo('path'), "user" )
	set=xbmcaddon.Addon(id='ptv3')
	set.setSetting("ptv",'3')
	UserDir = os.path.join(xbmc.translatePath("special://masterprofile/"),"addon_data","ptv3")
except:
	serv_dir = os.path.join(os.getcwd(), "serv" )
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

#======================Thread==========================
Lthread = []
def update_Lt(d, n=0, url=''):
	global Lthread
	if d == 'reset':	Lthread=[]
	else:				Lthread.append({'L':d, 'n':n, 'url': url})

from threading import Thread
class MyThread(Thread):
	def __init__(self, param):
		Thread.__init__(self)
		self.param = param
	
	def run(self):
		Lu=get_stream(self.param['url'])
		#try:r=test_url(Lu[0])
		#except: r='404'
		#if r!='404': update_Lt(Lu, self.param['n'], self.param['url'])
		#else:		 update_Lt([], self.param['n'], self.param['url'])
		update_Lt(Lu, self.param['n'], self.param['url'])


def create_thread(param):
		my_thread = MyThread(param)
		my_thread.start()
#================================================

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
	return id


def add_BLs(s):
	if s not in BLs and s!='':
		BLs.append(s)
		save_BLs(BLs)

def rem_BLs(s):
	try:BLs.remove(s)
	except: pass
	save_BLs(BLs)

def get_domen(s):
	if '192.168' in s: return ''
	elif '/udp/' in s: return ''
	else: return mfind(s, '//', '/')


def inBL(url):
	for i in BLs:
		if i in url: return True
	return False

import urllib2
def test_url(url):
	if 'udp://' in url:  return '200'
	if 'rtmp://' in url: return '200'
	if '/restream/' in url: return '200'
	
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

def rename_cnl(id, nt):
	if nt!='':
		try:
			DBC[id]['title']=nt
			save_DBC(DBC)
		except:
			print 'ERR ID not in DB'

def unite_cnl(id1, id2):
	if id1 not in DBC.keys(): add_to_base(id1)
	DBC[id2]['names'].extend(DBC[id1]['names'])
	L=[]
	for i in DBC[id2]['names']:
		if i not in L: L.append(i)
	DBC[id2]['names']=L
	#print DBC[id2]
	DBC.pop(id1)
	save_DBC(DBC)

def split_cnl(id, name):
	if name!='':
		nm_list=DBC[id]['names']
		id2=get_ID(name)#CRC32(name)
		DBC[id2]={'group': [], 'names': [name,], 'title': name}
		nm_list.remove(name)
		DBC[id]['names']=nm_list
		save_DBC(DBC)


def update_cnl():
		filtr=[]
		if settings.get("split_1") == 'false':filtr.append('h')
		if settings.get("split_2") == 'false':filtr.append('u')
		if settings.get("split_3") == 'false':filtr.append('p')
		if settings.get("split_4") == 'false':filtr.append('m')
			
		print('update channels ...')
		for i in Lserv:
			try:
				if i[:1] not in filtr:
					serv_id=str(int(i[1:3]))
					if settings.get("serv"+serv_id)!= 'false':
							print('update channels #'+serv_id)
							Ls=upd_canals_db(i)
			except:
				print 'ERR: '+i


def refresh_cnl():
		filtr=[]
		if settings.get("split_1") == 'false':filtr.append('h')
		if settings.get("split_2") == 'false':filtr.append('u')
		if settings.get("split_3") == 'false':filtr.append('p')
		if settings.get("split_4") == 'false':filtr.append('m')
		
		#print('refresh channels ...')
		for i in Lserv:
			try:
				if i[:1] not in filtr:
					serv_id=str(int(i[1:3]))
					if settings.get("serv"+serv_id)!= 'false' and settings.get("upd"+serv_id) == 'true':
						utm = get_cahe_time(serv_id)
						if time.time()-utm > 3600:
							print('update channels #'+serv_id)
							Ls=upd_canals_db(i)
			except:
				print 'ERR: '+i

def upd_canals_by_id(id):
	for i in Lserv:
		serv_id=str(int(i[1:3]))
		if serv_id==id:
			Ls=upd_canals_db(i)

def find_nm(nm):
		nm = uni_mark(nm)
		nm = nm.replace('-', ' ').replace('канал', '').replace('  ', ' ').strip()
		if nm in names_list: return nm
		
		if '(+' not in nm and '(' in nm: nm=nm[:nm.find('(')].strip()
		if nm in names_list: return nm
		
		return ''



def upd_canals_db(i):
	#print 'upd_canals_db '+i
	#try:
		exec ("import "+i+"; serv="+i+".PZL()")
		L=serv.Canals()
		dl_logo = settings.get("dl_logo")
		if True:
			LL=[]
			for k in L:
				id = get_ID(k['title'])
				if id not in DBC.keys():
					nm = find_nm(k['title'])
					if nm != '': 
						#print k['title']+' > '+nm
						k['title'] = nm
				
				if dl_logo == 'true':#Подгрузка логотипов
					try:img = k['img']
					except: img=''
					if img!='': 
						nid= get_ID(k['title'])
						GETimg(img, nid)
				
				LL.append(k)
			L=LL
	#except:
	#	L=[]
	#	print 'error'
	
		save_channels(i[1:3], L)
		if settings.get("addcnl")=='true': aggregate_cnl(L)
		return L

def aggregate_cnl(L):
	nm2id={}
	nml=[]
	for a in DBC.items():
		id=a[0]
		names=a[1]['names']
		for nm in names:
			nm2id[nm]=id
			nml.append(nm)
	
	for i in L:
		name=i['title']
		img=i['img']
		if 'group' in i.keys():group = i['group']
		else: group = ''
		
		if uni_mark(name) in nml:
			id = nm2id[uni_mark(name)]
			if group !="" and group not in DBC[id]['group']:
				DBC[id]['group'].append(group)
		else:
			id = get_ID(name)#CRC32(uni_mark(name))
			print id+" : "+name
			if group !="": lgroup=[group,]
			else:          lgroup=[]
			DBC[id]={'title': i['title'], 'group': lgroup, 'names':[uni_mark(i['title']),]}
		if img!='': GETimg(img, id)#Подгрузка логотипов
		if settings.get("addgr")=='true': appendgroup(group, id)
	save_DBC(DBC)

def GETimg(target, nmi, replace=False):
	try:
			if replace == False:
				if nmi =='': 				return target
				if nmi in picons.keys(): 	return picons[nmi]
				if settings.get("dl_logo")!='true': return target
			
			path = os.path.join(picon_dir, nmi+'.png')
			print 'dl_logo: '+ nmi
			import urllib2
			opener = urllib2.build_opener()
			urllib2.install_opener(opener)
			req = urllib2.Request(url = target, data = None)
			req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
			resp = urllib2.urlopen(req)
			fl = open(path, "wb")
			fl.write(resp.read())
			fl.close()
			#pDialog.close()
			#print path
			picons[nmi]=fs_enc('/logo/'+nmi+'.png')
			return path
	except:
		print "err: "+target
		return target

def appendgroup(group, id):
		if group !='':
			try:L=open_Groups()
			except:L=Ldf
			CL=[]
			for i in L:
				CL.append(i[0])
			
			if group in CL:
				add_to_gr(id, group)
			else:
				add_gr(group)
				add_to_gr(id, group)


def set_num_cn(SG, id, r):
	if SG!='' and SG!='all' and r>=0:
		try:L=open_Groups()
		except:L=[]
		CL=[]
		for i in L:
			if i[0]==SG: CL=i[1]
		CL.remove(id)
		for c in CL:
			if c not in DBC.keys():CL.remove(c)
		
		CL.insert(r, id)
		L2=[]
		for i in L:
				if i[0]==SG:
					if len(i)==2:igr=(SG,CL)
					elif len(i)==3:igr=(SG,CL,i[2])
					L2.append(igr)
				else:
					L2.append(i)
		
		save_Groups(L2)

def group_list(SG):
	if SG!='' and SG!='all':
		try:L=open_Groups()
		except:L=[]
		CL=[]
		for i in L:
			if i[0]==SG: CL=i[1]
		Lr=[]
		for cid in CL:
			try:    Lr.append({'id':cid, 'name':DBC[cid]['title']})
			except: CL.remove(cid)
	
		return Lr
	else:
		return []



def add_to_gr(id, group=''):
	try:L=open_Groups()
	except:L=Ldf
	Lg=[]
	for i in L:
		Lg.append(i[0])
		
	if Lg!=[]:
		if group=='':
			#sel = xbmcgui.Dialog()
			#r = sel.select("Группа:", Lg)
			r=-1
			print '!!! dopishi select.dialog !!!'
		else:
			r=Lg.index(group)
		if r!=-1:
			if id not in L[r][1]:
					L[r][1].append(id)
					save_Groups(L)

def rem_from_gr(id, SG=''):
	#try:	SG=__settings__.getSetting("Sel_gr")
	#except: SG=''
	
	try:L=open_Groups()
	except:L=Ldf
	L2=[]
	for i in L:
		if SG=='' or SG=='Все каналы':
				ng=i[1]
				if id in ng: i[1].remove(id)
				L2.append(i)
		else:
			if SG == i[0]:
				ng=i[1]
				if id in ng: i[1].remove(id)
			L2.append(i)
	save_Groups(L2)

def add_gr(name=''):
	#name=utf(name)
	if name == '': return #print '!!! input !!!'#name=inputbox('')
	try:L=open_Groups()
	except:L=Ldf
	st=(name,[])
	if st not in L: L.append(st)
	save_Groups(L)

def rem_gr(name=''):
	try:L=open_Groups()
	except:L=Ldf
	Lg=[]
	for i in L:
		Lg.append(i[0])
	
	if name=="":
		return
		'''
		if Lg!=[]:
			sel = xbmcgui.Dialog()
			r = sel.select("Группа:", Lg)
		if r>=0:
			name=Lg[r]
		'''
	if name!="":
		L2=[]
		for i in L:
			if i[0]!=name: L2.append(i)
		save_Groups(L2)

def rename_gr(id, name):
	if name!="":
		try:L=open_Groups()
		except:L=Ldf
		Lg=[]
		gi=None
		n=0
		for i in L:
			if n==id: i=(name,i[1])
			Lg.append(i)
			n+=1
		save_Groups(Lg)

def get_blacklist_cn(cgr=''):
		BL=[]
		try:L=open_Groups()
		except:L=[]
		for i in L:
			if len(i)==3:
				if i[2]!='false' and i[0]!=cgr: BL.extend(i[1])
		return BL

def get_blacklist_gr():
		BL=[]
		try:L=open_Groups()
		except:L=[]
		for i in L:
			if len(i)==3:
				if i[2]!='false': BL.append(i[0])
		return BL

def lock_gr(id, lock='false'):
		try:L=open_Groups()
		except:L=Ldf
		Lg=[]
		gi=None
		n=0
		for i in L:
			if n==id: i=(i[0],i[1], lock)
			Lg.append(i)
			n+=1
		save_Groups(Lg)

def move_gr(id, new_id):
	L=open_Groups()
	itm = L.pop(id)
	L.insert(new_id, itm)
	save_Groups(L)

def unite_gr(id1, id2):
	L=open_Groups()
	g1 = L[id1][1]
	g2 = L[id2][1]
	g2.extend(g1)
	itm2 = (L[id2][0], g2)
	L[id2] = itm2
	L.pop(id1)
	save_Groups(L)

def save_channels(n, L):
		s=str(int(n))
		print 'save_channels-'+s+"-"+str(len(L))
		fp=os.path.join(serv_dir, s+'.cl')
		fl = open(fp, "w")
		fl.write('[\n')
		for i in L:
			fl.write(repr(i)+',\n')
		fl.write(']\n')
		fl.write('udata='+str(time.time()))#strftime('%Y%m%d')
		fl.close()

def get_all_channeles():
	#print '==get_all_channeles start=='
	L=[]
	filtr=[]
	if settings.get("split_1") == 'false':filtr.append('h')
	if settings.get("split_2") == 'false':filtr.append('u')
	if settings.get("split_3") == 'false':filtr.append('p')
	if settings.get("split_4") == 'false':filtr.append('m')
	
	# приоритет источников
	Ltmp=[]
	for s in Lserv:
		sid=str(int(s[1:3]))
		pr = settings.get('pr'+sid)
		if pr=='':sort = 'я'
		else: sort = pr
		Ltmp.append([sort, s])
	
	Ltmp.sort()
	Lout = []
	for t in Ltmp:
		Lout.append(t[1])
	
	for i in Lout:
		if i[:1] not in filtr:
			serv_id=str(int(i[1:3]))
			if settings.get("serv"+serv_id)!= 'false':
				print serv_id
				try: 
					Ls=get_cahe_list(serv_id)
				except:Ls=[]
				if Ls==[]:
					utm = get_cahe_time(serv_id)
					if time.time()-utm > 600:
						try: Ls=upd_canals_db(i)
						except: Ls=[]
			else: Ls=[]
			
			L.extend(Ls)
	#print '==get_all_channeles end=='
	return L

def get_all_picons(id):
	print '==get_all_picons=='
	L=[]
	LL=[]
	for i in Lserv:
				serv_id=str(int(i[1:3]))
				print serv_id
				try:Ls=get_cahe_list(serv_id)
				except:Ls=[]
				if Ls==[]:
					utm = get_cahe_time(serv_id)
					if time.time()-utm > 600:
						try: Ls=upd_canals_db(i)
						except: Ls=[]
				L.extend(Ls)
	for i in L:
		if get_ID(i['title']) == id and i['img']!='': LL.append(i['img'])
	return LL

def get_all_serv(id):
	L=[]
	filtr=[]
	if settings.get("split_1") == 'false':filtr.append('h')
	if settings.get("split_2") == 'false':filtr.append('u')
	if settings.get("split_3") == 'false':filtr.append('p')
	if settings.get("split_4") == 'false':filtr.append('m')
	
	cl_names = DBC[id]['names']
	LL=[]
	for i in Lserv:
			serv_id=str(int(i[1:3]))
			serv_nm=i[4:]
			pr = settings.get('pr'+serv_id)
			
			enable_serv = True
			if i[:1] in filtr: enable_serv = False
			if settings.get("serv"+serv_id)== 'false': enable_serv = False
			
			try:    Ls=get_cahe_list(serv_id)
			except: Ls=[]
			
			if Ls==[]:
				utm = get_cahe_time(serv_id)
				if time.time()-utm > 600:
					try: Ls=upd_canals_db(i)
					except: Ls=[]
			
			for n in Ls:
				name = uni_mark(n['title'])
				if name in cl_names :
					url=n['url']
					if url in BLs: lock = True
					else:          lock = False
					LL.append({'serv': serv_nm, 'url': url, 'id':serv_id, 'lock':lock, 'serv_on': enable_serv, 'priority': pr})
			
	return LL



def get_serv_dict():
	filtr=[]
	if settings.get("split_1") == 'false':filtr.append('h')
	if settings.get("split_2") == 'false':filtr.append('u')
	if settings.get("split_3") == 'false':filtr.append('p')
	if settings.get("split_4") == 'false':filtr.append('m')

	D={}
	for i in Lserv:
			serv_id=str(int(i[1:3]))
			if i[:1] in filtr:	serv_nm='<font color="red">'+i[4:]+'</font>'
			elif settings.get("serv"+serv_id)== 'false': serv_nm='<font color="red">'+i[4:]+'</font>'
			else:				serv_nm=i[4:]
			try: Ls=get_cahe_list(serv_id)
			except:Ls=[]
			D[serv_nm]=Ls
	return D


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
		L2=eval(t[t.find('['):t.rfind(']')+1])
		L=[]
		for i in L2:
			if inBL(i['url']) == False: L.append(i)
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


def get_SG():
	SG=settings.get("Sel_gr")
	if SG=='':
		SG='Все каналы'
		settings.set("Sel_gr",SG)
	return SG

def save_Groups(L):
		fp=os.path.join(UserDir, 'UserGR.py')
		fl = open(fp, "w")
		fl.write('[\n')
		for i in L:
			fl.write(repr(i)+',\n')
		fl.write(']\n')
		fl.close()

def open_Groups():
		fp=os.path.join(UserDir, 'UserGR.py')
		
		try:sz=os.path.getsize(fp)
		except:sz=0
		if sz==0:
			save_Groups(Ldf)
			return Ldf
		
		fl = open(fp, "r")
		ls=fl.read().replace('\n','')
		fl.close()
		return eval(ls)

def get_dict_groups():
	D={}
	for i in open_Groups():
		group=i[0]
		for id in i[1]:
			try:    l_gr=D[id]
			except: l_gr = []
			if group not in l_gr: 
				l_gr.append(group)
				D[id]=l_gr
	return D

def get_cn_groups(cid):
	D=get_dict_groups()
	if cid in D.keys(): return D[cid]
	else: return []

def sort_abc(L):
	L2=[]
	for id in L:
		try: L2.append((DBC[id]['title'],id))
		except: pass
	L2.sort()
	L=[]
	for i in L2:
		L.append(i[1])
	return L

def get_gr(SG='', blacklist=True):
	if SG=='':SG=get_SG()
	if SG=='Все каналы':
		CLf=[]
		DBK=DBC.keys()
		LG=open_Groups()
		for g in LG:
			for cid in g[1]:
				if cid in DBK and cid not in CLf: CLf.append(cid)
		for cid in DBK:
			if cid not in CLf: CLf.append(cid)
	else:
		try:L=open_Groups()
		except:L=[]
		CLf=[]
		for i in L:
			if i[0]==SG: CLf=i[1]
	
	if blacklist: BL=get_blacklist_cn(SG)
	else: BL=[]
	if BL==[]: CL=CLf
	else:
		CL=[]
		for c in CLf:
			if c not in BL: CL.append(c)
	
	#if settings.get("abc")=='true' or SG=='Все каналы': CL=sort_abc(CL)
	return CL

def get_picon_dict():
	try:
		fp=os.path.join(picon_dir, 'picon_list.txt')
		fl = open(fp, "r")
		t=fl.read()
		fl.close()
		L=t.splitlines()
		D={}
		for i in L:
			D[i[:-4]]='http://td-soft.narod.ru/logo/picon/'+i
		
		L=os.listdir(picon_dir)
		ip = settings.get('ip')
		for i in L:
			D[i[:-4]]=fs_enc('http://'+ip+':'+str(port)+'/logo/'+i)
		
		return D
	except:
		return {}

picons = get_picon_dict()

def get_allurls(id, L):
	cl_names = DBC[id]['names']
	L3=[]
	for j in L:
		name = uni_mark(j['title'])
		if name in cl_names :
			url = j['url']
			if url not in BLs: L3.append(url)
	return L3

def get_stream(url):
	filtr=[]
	if settings.get("split_1") == 'false':filtr.append('h')
	if settings.get("split_2") == 'false':filtr.append('u')
	if settings.get("split_3") == 'false':filtr.append('p')
	if settings.get("split_4") == 'false':filtr.append('m')
	
	buf=CRC32(url)
	if buf in UrlCashe.keys():
		Cashe=UrlCashe[buf]
		if time.time()-Cashe['time'] < 300:
			print '==== Cashe ===='
			return Cashe['urls']
	
	print '==== new_steams ===='
	for i in Lserv:
		
		if i[:1] not in filtr:
			ids=i[4:]
			ids2 = ids.replace('_','-')
			#print ids
			if ids in url or ids2 in url:
				print ids
				print url
				try:
					exec ("import "+i+"; serv="+i+".PZL()")
					Lcurl = serv.Streams(url)
					Lpurl = []
					try:
						for curl in Lcurl: 
							if 'zabava' in curl or 'vrzh-htlive' in curl or 'yandex' in curl or 'ucom.am' in curl or '/udp/' in curl or 'peers.tv' in curl or '193.124.177.175' in curl:
								import base64
								ip = settings.get('ip')
								curl= 'http://'+ip+':'+str(port)+'/restream/'+base64.b64encode(curl)
							
							if 'acestream://' in curl:
								CID=curl[12:]
								prx = settings.get("p2p_proxy")
								ip = settings.get('ip')
								srv=settings.get("p2p_serv")
								if srv=='': srv = '127.0.0.1'
								if prx == 'RESTREAMER' or prx == 'REDIRECT':
									curl = 'http://'+ip+':'+str(port)+'/acestream/'+CID
								elif prx == 'AS_PROXY':
									curl = 'http://'+srv+':8000/infohash/'+CID+'/stream.mp4'
								else:
									curl = 'http://'+srv+':6878/ace/getstream?id='+CID+"&.mp4"
							
							Lpurl.append(curl)
							
						#print Lpurl
						Lcurl=Lpurl
					except:pass
					UrlCashe[CRC32(url)]={'urls':Lcurl, 'time': time.time()}
					#print UrlCashe
					return Lcurl
				except:
					print 'error'
					UrlCashe[CRC32(url)]={'urls':[], 'time': time.time()}
	return []


def channels(SG=''):
		#refresh_cnl() # обновление каналов
		BL = get_blacklist_cn()
		
		Lret=[]
		if SG=='all':SG='Все каналы'
		if SG=='':SG=get_SG()
		Lnm=[]
		Ls=get_all_channeles()
		
		CL=get_gr(SG)
		nml=[]
		bl=[]
		dn={}
		
		A=[]
		for id in CL:
			try:
				i = DBC[id]
				names = i['names']
				name  = i['title']
				A.extend(names)
				for b in names:
					dn[b]=name
			except: pass
		
		B=[]
		for a in Ls:
			B.append(uni_mark(a['title']))
		
		Bset = frozenset(B)
		C = [item for item in A if item in Bset] 
		
		for nm in C:
			nml.append(dn[nm])
		#print 'root C: '+ str(time.time()-tm)
		
		for id in CL:
				try:
					name  = DBC[id]['title']
					if name in nml:
						if id in picons.keys(): cover = picons[id]
						else: 
							cover = picons['0000']
							#print 'NO PICON: '+id+' '+name
						if id not in BL:
							Lret.append({'title':name, 'id': id, 'picon': cover})
				except:
					pass
		
		return Lret

def get_DBC():
	L=[]
	for id in DBC.keys():
		i = DBC[id]
		try: gr=i['group'][0]
		except: gr=''
		L.append({'00':uni_mark(i['title']),'title':i['title'], 'id':id, 'group': gr})
		L.sort()
	return L

#base_cache={}

def get_base(mode = 'none'):
	if mode == 'none': mode = settings.get('editor_mode')
	
	BL = get_blacklist_cn()
	BG = get_blacklist_gr()
	
	#global base_cache
	editor_sort=settings.get("editor_sort")
	filtr=[]
	if settings.get("split_1") == 'false':filtr.append('h')
	if settings.get("split_2") == 'false':filtr.append('u')
	if settings.get("split_3") == 'false':filtr.append('p')
	if settings.get("split_4") == 'false':filtr.append('m')
	
	enb_list = []
	for j in channels('all'): 
		enb_list.append(j['id'])
	
	CL=DBC.keys()
	L=[]
	Lt=[]
	lid=[]
	
	
	
	for id in CL:
		lid.append(id)
		Lnm=DBC[id]['names']
		if len(Lnm)>1: spl=True
		else: spl=False
		for n in Lnm:
			id2 = get_ID(n)#CRC32(n)
			lid.append(id2)
				
		if id not in BL:
			
			if mode!='false':
				groups = get_cn_groups(id)#DBC[id]['group']
				name = DBC[id]['title']
				if id in enb_list:
					if editor_sort == 'group': sort = groups
					else:                      sort = uni_mark(name)
						
					if id in picons.keys(): cover = picons[id]
					else:                   cover = '\\webui.files\space.jpg'#picons['0000']
					
					if sort=='' or sort==[]: sort='яяяяяяяяяяя'
					L.append({'00':sort,'title':name,'id':id,'group':groups, 'enable':True, 'split':spl, 'picon':cover})
	
	if mode!='true':
		for i in Lserv:
			if i[:1] not in filtr:
				serv_id=str(int(i[1:3]))
				if settings.get("serv"+serv_id)!= 'false':
					try: Ls=get_cahe_list(serv_id)
					except:Ls=[]
					for c in Ls:
						name = c['title']
						id = get_ID(name)#CRC32(uni_mark(name))
						if id not in lid:
							if id not in CL and id not in BL:
								#picon = c['img']
								try:group = c['group']
								except:group =''
								if group not in BG:
									lid.append(id)
									#Lt.append(name)
									if editor_sort == 'group': sort = [group,]
									else:                      sort = uni_mark(name)
									
									if id in picons.keys(): cover = picons[id]
									else:                   cover = '\\webui.files\space.jpg'#picons['0000']
									
									if sort=='' or sort==['',]: sort='яяяяяяяяяяя'
									L.append({'00':sort,'title':name,'id':id,'group':[group,], 'enable':False, 'split':False, 'picon':cover})
	L.sort()
	return L
	

def rem_from_base(CID=''):
	if CID!='':
		DBC.pop(CID)
		save_DBC(DBC)


def add_to_base(CID):
	CL=DBC.keys()
	L=[]
	Lt=[]
	lid=[]
	for i in Lserv:
			serv_id=str(int(i[1:3]))
			try: Ls=get_cahe_list(serv_id)
			except:Ls=[]
			for c in Ls:
				name = c['title']
				#picon = c['img']
				try:group = c['group']
				except:group =''
				id = get_ID(name)#CRC32(uni_mark(name))
				if id not in CL:
					if id == CID:
						DBC[id]={'group': [group,], 'names': [uni_mark(c['title'])], 'title': c['title']}
						try: save_DBC(DBC)
						except: pass
						set_group_cnl(id, group, False)
						return True
	return False

def set_group_cnl(id, gs, add=True):
	rem_from_gr(id)
	Lg = gs.split('|')
	GROUPS = groups()
	for g in Lg:
		group = g.strip()
		if group in GROUPS:
			add_to_gr(id, group)
		else:
			if add:
				add_gr(group)
				add_to_gr(id, group)

def groups():
	L=open_Groups()
	Lg=['Все каналы',]
	for i in L:
		Lg.append(i[0])
		#if len(i)==2:Lg.append(i[0])
		#elif len(i)==3: Lg.append(i[0]+'[lock]')
	return Lg

def playlist(type='stream'):
		#try:ip = socket.gethostbyname_ex(socket.gethostname())[2][0]
		#except: ip = '127.0.0.1'
		ip = settings.get('ip')
		Dgr={}
		try:Lgr=open_Groups()
		except:Lgr=[]
		for i in Lgr:
			for idc in i[1]:
				Dgr[idc]=i[0]

		list='#EXTM3U\n'
		L=channels('all')# pztv.root('Все каналы')
		for i in L:
			name  = i['title']
			id    = i['id']
			cover = i['picon']
			if id in Dgr.keys(): gr=Dgr[id]
			else: gr='ДРУГИЕ'
			EXTINF='#EXTINF:-1 group-title="'+gr+'" tvg-name="'+name+'" tvg-id="'+id+'" tvg-logo="'+cover+'",'+name
			PREF='http://'+ip+':'+str(port)+'/'+type+'/'
			list+=EXTINF+'\n'
			list+=PREF+id+'\n'
		return list

def tvhlist(type='stream'):
		ip = settings.get('ip')
		Dgr={}
		try:Lgr=open_Groups()
		except:Lgr=[]
		for i in Lgr:
			for idc in i[1]:
				Dgr[idc]=i[0]
		
		list='#EXTM3U\n'
		L=channels('all')
		for i in L:
			name  = i['title']
			id    = i['id']
			cover = i['picon']
			if id in Dgr.keys(): gr=Dgr[id]
			else: gr='ДРУГИЕ'
			EXTINF='#EXTINF:-1 group-title="'+gr+'" tvg-name="'+name+'" tvg-id="'+id+'" tvg-logo="'+cover+'",'+name
			EXTGRP='#EXTGRP:'+gr
			URL='http://'+ip+':'+str(port)+'/'+type+'/'+id
			ITM = 'pipe://ffmpeg -v quiet -i '+URL+' -c copy -map 0 -f mpegts pipe:1'
			list+=EXTINF+'\n'
			list+=EXTGRP+'\n'
			list+=ITM+'\n'
		return list

def stream(id):
	if id=='': return ''
	L = get_all_channeles()
	urls=get_allurls(id, L)
	'''
	if settings.get('p2p_start') == 'true': 
		for url in urls:
			print url
			try: L2=get_stream(url)
			except:L2=[]
			for s in L2:
				#print s
				if '/ace/' in s:
					t=test_url(s)
					#print t
					if  s!='' and t!='404': return s 
	'''
	
	for url in urls:
		try: L2=get_stream(url)
		except:L2=[]
		for s in L2:
			t=test_url(s)
			#print t
			if  s!='' and t!='404': return s 
	return ''

def streams_old(id):
	if id=='': return []
	L = get_all_channeles()
	urls=get_allurls(id, L)
	LL=[]
	for url in urls:
		try: L2=get_stream(url)
		except:L2=[]
		LL.extend(L2)
		#if len(L2)>0: return L2[0]
	return LL

def streams(id):
	if id=='': return []
	L = get_all_channeles()
	urls=get_allurls(id, L)
	LL=[]
	Lt=[]
	if settings.get("multi")=='true' and len(urls)>1:
		fplay = settings.get("fplay")
		update_Lt('reset')
		sn=0
		for url in urls:
			sn+=1
			create_thread({'url':url, 'n':sn})
		
		for t in range(6):
			if len(Lthread) == len(urls): break
			#if len(Lthread) > 1 and fplay =='true': break
			time.sleep(0.5)
		
		for rst in Lthread:
			Lst=rst['L']
			n = rst['n']
			for st in Lst:
				Lt.append([n,st])
		
		Lt.sort()
		for r in Lt:
			if r[1] not in LL: LL.append(r[1])
	
	else:
		for url in urls:
			try: L2=get_stream(url)
			except:L2=[]
			LL.extend(L2)
			
	return LL


def streams_ds(id):
	if id=='': return []
	L = get_all_channeles()
	urls=get_allurls(id, L)
	LL=[]
	Lt=[]
	if settings.get("multi")=='true' and len(urls)>1:
		fplay = settings.get("fplay")
		update_Lt('reset')
		sn=0
		for url in urls:
			sn+=1
			create_thread({'url':url, 'n':sn})
		
		for t in range(60):
			if len(Lthread) == len(urls): break
			#if len(Lthread) > 1 and fplay =='true': break
			time.sleep(0.1)
		
		for rst in Lthread:
			Lst=rst['L']
			n = rst['n']
			ur= rst['url']
			Lt.append([n,Lst,ur])
		
		Lt.sort()
		for r in Lt:
			if len(r[1])>0: LL.append({'cache':r[2], 'streams': r[1]})
	
	else:
		for url in urls:
			try: L2=get_stream(url)
			except:L2=[]
			if len(L2)>0: LL.append({'cache':url, 'streams': L2})
	return LL


def sublist_old(id):
		#try:ip = socket.gethostbyname_ex(socket.gethostname())[2][0]
		#except: ip = '127.0.0.1'
		ip = settings.get('ip')
		list='#EXTM3U\n'
		L=streams(id)
		for i in L:
			name  = mfind(i, '://', '/')
			EXTINF='#EXTINF:-1 ,'+name
			list+=EXTINF+'\n'
			list+=i+'\n'
		return list

def sublist(id):
		list='#EXTM3U\n#EXT-X-VERSION:3\n'
		L=streams(id)
		for i in L:
			list+='#EXT-X-STREAM-INF:PROGRAM-ID=1\n'
			list+=i+'\n'
		return list

def sublist2(stream):
		list='#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-STREAM-INF:PROGRAM-ID=1\n'+stream
		return list


def jsonlist():
		#try:ip = socket.gethostbyname_ex(socket.gethostname())[2][0]
		#except: ip = '127.0.0.1'
		ip = settings.get('ip')
		Dgr={}
		Dgrn={}
		Dnum={}
		Djson={}
		try:Lgr=open_Groups()
		except:Lgr=[]
		nc = 0
		for i in Lgr:
			ncg = 0
			for cid in i[1]:
				ncg+=1
				if cid in Dgr.keys():
					Dgr[cid].append(i[0])
					Dgrn[cid].append({'name':i[0], 'num':ncg})
				else:
					nc+=1
					Dgr[cid]=[i[0]]
					Dgrn[cid]=[{'name':i[0], 'num':ncg}]
					Dnum[cid]=nc

		L=channels('all')#root_list()
		Lc=[]
		nc2 = 0
		for i in L:
			name  = i['title']
			id    = i['id']
			cover = i['picon']
			if id in Dgr.keys(): 
				gr=Dgr[id]
				grn=Dgrn[id]
				num = Dnum[id]
			else: 
				nc+=1
				nc2+=1
				num = nc
				grn=[{'name':'ДРУГИЕ', 'num':nc2}]
				gr=['ДРУГИЕ']
			PREF='http://'+ip+':'+str(port)+'/streams/json/'
			curl=PREF+id
			Lc.append({"id":id, "name":name, "icon":cover, "group":gr, "group_num":grn, "url":curl, "num":num})
		Djson["channels"]=Lc
		#return repr(json).replace("'", '"').replace('u"','"')
		return json.dumps(Djson)

def json_streams(id):
	if id=='': return '[]'
	L = get_all_channeles()
	urls=get_allurls(id, L)
	Lstr=[]
	for url in urls:
		try: L2=get_stream(url)
		except:L2=[]
		for st in L2:
			Lstr.append(st)
	#return repr(Lstr).replace("'", '"').replace('u"','"')
	return json.dumps(Lstr)

def get_rating(url):
	buf = url
	#print buf
	id = CRC32(buf)
	import bldb
	inf=bldb.get_info(id)
	#print inf
	return inf

def set_rating(url, ratung=''):
	buf = url
	id = CRC32(buf)
	import bldb
	info=bldb.get_info(id)
	try:    good = info['good']
	except: good=0
	try:    bad = info['bad']
	except: bad=0
	if ratung=='good':good+=1
	if ratung=='bad' :bad+=1
	n_info={'good':good, 'bad':bad}
	bldb.add(id, n_info)

#get_cahe_list('5')

#L=channels('\xd0\x9c\xd0\xa3\xd0\x97\xd0\xab\xd0\x9a\xd0\x90')
#for i in L:
#	print i['id']
