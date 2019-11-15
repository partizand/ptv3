# coding: utf-8
# Module: server
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
import sys, os, json
import settings as seti
import time
import urllib2
import core
import cookielib

settings = seti.Settings.getInstance()

# try:
# 	import xbmcaddon, xbmc
# 	addon = xbmcaddon.Addon(id='ptv3')
# 	serv_dir = os.path.join(addon.getAddonInfo('path'),"serv")
# 	picon_dir = os.path.join(addon.getAddonInfo('path'),'logo')
# 	set=xbmcaddon.Addon(id='ptv3')
# 	set.setSetting("ptv",'3')
# 	UserDir = os.path.join(xbmc.translatePath("special://masterprofile/"),"addon_data","ptv3")
# except:
# 	serv_dir = os.path.join(os.getcwd(), "serv" )
# 	picon_dir = os.path.join(os.getcwd(),'logo')
# 	UserDir = os.path.join(os.getcwd(), "user" )


sid_file = os.path.join(settings.UserDir, 'vsetv.sid')
cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 
urllib2.install_opener(opener) 


try: port = int(settings.get('port'))
except: 
	port = 8185
	settings.set('port', 8185)
if port=='': 
	port = 8185
	settings.set('port', 8185)


sys.path.append(settings.UserDir)

from UserDBcnl import *

try: 
	from EPGdb import *
	if EPG == "": EPG = {}
except:
	EPG = {}


PlotCashe={}
ImgCashe={}

class Dialog():
	def create (self, s1, s2):
		print s2
	
	def update (self, s1, message=''):
		print(message)
		
	def close(self):
		print ('== OK ==')

pDialog=Dialog()

# =========================== Базовые функции ================================
def save_d(d):
	try:
		fp=os.path.join(settings.UserDir, 'epg.db')
		fl = open(fp, "w")
		fl.write(repr(d))
		fl.close()
	except:
		pass

def get_d():
	try:
		fp=os.path.join(settings.UserDir, 'epg.db')
		fl = open(fp, "r")
		d=eval(fl.read())
		fl.close()
		return d
	except:
		return {}

link_cnl = get_d()

def mfindal(http, ss, es):
	L=[]
	while http.find(es)>0:
		s=http.find(ss)
		#sn=http[s:]
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L

def getURL2(url, dt=3):
		import requests
		try:
			s = requests.session()
			r=s.get(url, timeout=(0.5, dt), verify=False).text#0.00001
		except:
			print 'requests: timeout'
			r=''
		#r=r.encode('windows-1251')
		return r

def getURL(url, Referer = 'http://viks.tv/'):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	req.add_header('Referer', Referer)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def SEND(command):
		ip = settings.get('ip')
		url='http://'+ip+':'+str(port)+'/'+command
		r=getURL(url)
		return r

def get_HTML(url, post = None, ref = None, get_redirect = False):
    import urlparse
    if url.find('http')<0 :url='http:'+url
    request = urllib2.Request(url, post)

    host = urlparse.urlsplit(url).hostname
    if ref==None:
        try:
           ref='http://'+host
        except:
            ref='localhost'

    request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
    request.add_header('Host',   host)
    request.add_header('Accept', 'text/html, application/xhtml+xml, */*')
    request.add_header('Accept-Language', 'ru-RU')
    request.add_header('Referer',             ref)
    request.add_header('Content-Type','application/x-www-form-urlencoded')

    try:
        f = urllib2.urlopen(request)
    except IOError as e:
        if hasattr(e, 'reason'):
           print('We failed to reach a server.')
        elif hasattr(e, 'code'):
           print('The server couldn\'t fulfill the request.')
        return 'We failed to reach a server.'

    if get_redirect == True:
        html = f.geturl()
    else:
        html = f.read()

    return html




def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return x

def rt(x):
	try:
		L=[('&#133;','…'),('&#34;','&'), ('&#39;','’'), ('&#145;','‘'), ('&#146;','’'), ('&#147;','“'), ('&#148;','”'), ('&#149;','•'), ('&#150;','–'), ('&#151;','—'), ('&#152;','?'), ('&#153;','™'), ('&#154;','s'), ('&#155;','›'), ('&#156;','?'), ('&#157;',''), ('&#158;','z'), ('&#159;','Y'), ('&#160;',''), ('&#161;','?'), ('&#162;','?'), ('&#163;','?'), ('&#164;','¤'), ('&#165;','?'), ('&#166;','¦'), ('&#167;','§'), ('&#168;','?'), ('&#169;','©'), ('&#170;','?'), ('&#171;','«'), ('&#172;','¬'), ('&#173;',''), ('&#174;','®'), ('&#175;','?'), ('&#176;','°'), ('&#177;','±'), ('&#178;','?'), ('&#179;','?'), ('&#180;','?'), ('&#181;','µ'), ('&#182;','¶'), ('&#183;','·'), ('&#184;','?'), ('&#185;','?'), ('&#186;','?'), ('&#187;','»'), ('&#188;','?'), ('&#189;','?'), ('&#190;','?'), ('&#191;','?'), ('&#192;','A'), ('&#193;','A'), ('&#194;','A'), ('&#195;','A'), ('&#196;','A'), ('&#197;','A'), ('&#198;','?'), ('&#199;','C'), ('&#200;','E'), ('&#201;','E'), ('&#202;','E'), ('&#203;','E'), ('&#204;','I'), ('&#205;','I'), ('&#206;','I'), ('&#207;','I'), ('&#208;','?'), ('&#209;','N'), ('&#210;','O'), ('&#211;','O'), ('&#212;','O'), ('&#213;','O'), ('&#214;','O'), ('&#215;','?'), ('&#216;','O'), ('&#217;','U'), ('&#218;','U'), ('&#219;','U'), ('&#220;','U'), ('&#221;','Y'), ('&#222;','?'), ('&#223;','?'), ('&#224;','a'), ('&#225;','a'), ('&#226;','a'), ('&#227;','a'), ('&#228;','a'), ('&#229;','a'), ('&#230;','?'), ('&#231;','c'), ('&#232;','e'), ('&#233;','e'), ('&#234;','e'), ('&#235;','e'), ('&#236;','i'), ('&#237;','i'), ('&#238;','i'), ('&#239;','i'), ('&#240;','?'), ('&#241;','n'), ('&#242;','o'), ('&#243;','o'), ('&#244;','o'), ('&#245;','o'), ('&#246;','o'), ('&#247;','?'), ('&#248;','o'), ('&#249;','u'), ('&#250;','u'), ('&#251;','u'), ('&#252;','u'), ('&#253;','y'), ('&#254;','?'), ('&#255;','y'), ('&laquo;','"'), ('&raquo;','"'), ('&nbsp;',' '), ('&amp;quot;','"')]
		for i in L:
			x=x.replace(i[0], i[1])
		return x
	except:
		return x

def showMessage(heading, message, times = 3000):
	print(message)

def fs_enc(path):
	sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
	return path.decode('utf-8').encode(sys_enc)

def fs_dec(path):
	sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
	return path.decode(sys_enc).encode('utf-8')


def lower(t):
	RUS={"А":"а", "Б":"б", "В":"в", "Г":"г", "Д":"д", "Е":"е", "Ё":"ё", "Ж":"ж", "З":"з", "И":"и", "Й":"й", "К":"к", "Л":"л", "М":"м", "Н":"н", "О":"о", "П":"п", "Р":"р", "С":"с", "Т":"т", "У":"у", "Ф":"ф", "Х":"х", "Ц":"ц", "Ч":"ч", "Ш":"ш", "Щ":"щ", "Ъ":"ъ", "Ы":"ы", "Ь":"ь", "Э":"э", "Ю":"ю", "Я":"я"}
	for i in range (65,90):
		t=t.replace(chr(i),chr(i+32))
	for i in RUS.keys():
		t=t.replace(i,RUS[i])
	return t

def upper(t):
	RUS={"А":"а", "Б":"б", "В":"в", "Г":"г", "Д":"д", "Е":"е", "Ё":"ё", "Ж":"ж", "З":"з", "И":"и", "Й":"й", "К":"к", "Л":"л", "М":"м", "Н":"н", "О":"о", "П":"п", "Р":"р", "С":"с", "Т":"т", "У":"у", "Ф":"ф", "Х":"х", "Ц":"ц", "Ч":"ч", "Ш":"ш", "Щ":"щ", "Ъ":"ъ", "Ы":"ы", "Ь":"ь", "Э":"э", "Ю":"ю", "Я":"я"}
	for i in RUS.keys():
		t=t.replace(RUS[i],i)
	for i in range (65,90):
		t=t.replace(chr(i+32),chr(i))
	return t

def CRC32(buf):
		import binascii
		buf = (binascii.crc32(buf) & 0xFFFFFFFF)
		return str("%08X" % buf)

def mfind_old(t,s,e):
	r=t[t.find(s)+len(s):t.find(e)]
	return r

def mfind(t,s,e):
	r=t[t.find(s)+len(s):]
	r2=r[:r.find(e)]
	return r2
	
def debug(s):
	fl = open(ru(os.path.join( settings.UserDir,"test.txt")), "w")
	fl.write(s)
	fl.close()


# ================================ БД =======================================

def get_inf_db(cid):
	#print n
	if cid in link_cnl.keys(): cid=link_cnl[cid]
	#print n
	try: return EPG[cid]
	except: return {}


# ================================ EPG =======================================

def upepg():
			pDialog.create('EPG', 'Update EPG ...')
			clear_EPG()
			if settings.get('epg_iptvx')=='true':  
				pDialog.update(10, message='Update EPG iptvx')
				try: upd_EPG_xmltv()
				except: pDialog.update(10, message='iptvx: Error')
			if settings.get('epg_tviz')=='true':  
				pDialog.update(20, message='Update EPG Tviz')
				try:tviz()
				except: pDialog.update(30, message='Tviz: Error')
			if settings.get('epg_prtv')=='true':  
				pDialog.update(30, message='Update EPG ProgramTV')
				try:upd_programtv()
				except: pDialog.update(30, message='ProgramTV: Error')
			if settings.get('epg_vsetv_ua')=='true': 
				pDialog.update(40, message='Update EPG VseTV UA')
				try:upd_EPG_vsetv("uabase")
				except: pDialog.update(40, message='VseTV: Error')
			if settings.get('epg_vsetv_by')=='true': 
				pDialog.update(50, message='Update EPG VseTV BY')
				try:upd_EPG_vsetv("bybase")
				except: pDialog.update(50, message='VseTV: Error')
			if settings.get('epg_vsetv_ru')=='true': 
				pDialog.update(70, message='Update EPG VseTV RU')
				try:upd_EPG_vsetv("tricolor")#rubase
				except: pDialog.update(70, message='VseTV: Error')
			if settings.get('epg_yatv')=='true': 
				pDialog.update(80, message='Update EPG Yandex')
				try: yatv()
				except: pDialog.update(80, message='Yandex: Error')
			if settings.get('epg_mail')=='true': 
				pDialog.update(90, message='Update EPG Mail')
				try: mail()
				except: pDialog.update(90, message='Mail: Error')
			save_EPG()
			XMLTV['data']=''
			pDialog.close()

def ADD_EPG(idx, De):
	#print '==== ADD_EPG '+idx
	if idx in EPG.keys():
		#print 'idx in EPG'
		cn=EPG[idx]
		for i in De.keys():
			if i in cn.keys() and i != 'title':
				#print 'i in cn'
				try:
					if De[i]["title"]!='': cn[i]["title"]=De[i]["title"]
				except: pass
				try:
					if De[i]["img"]!='':   cn[i]["img"] = De[i]["img"]
				except: pass
				try:
					if De[i]["plot"]!='':  cn[i]["plot"]= De[i]["plot"]
				except: pass
				try:
					if De[i]["type"]!='':  cn[i]["type"]= De[i]["type"]
				except: pass
			else:
				#print 'i not in cn'
				cn[i] = De[i]
		EPG[idx] = cn
	else:
		#print 'idx not in EPG'
		EPG[idx] = De

serv_cn_list = []
def get_serv_cn_list():
	try: LC=eval(SEND('channels/dict'))
	except: LC=[]
	for itm in LC:
		serv_cn_list.append(itm['id'])
		
	for i in link_cnl.keys():
		serv_cn_list.append(link_cnl[i])
		serv_cn_list.append(i)
	
	return serv_cn_list

def LOW_EPG(idx, De):
	if serv_cn_list==[]: get_serv_cn_list()
	if idx in serv_cn_list:
		#print '==== LOW_EPG '+idx
		cn={}
		for i in De.keys():
			if i != 'title':
				cn[i]={}
				try:
					cn[i]["title"]=De[i]["title"]
				except: pass
				try:
					cn[i]["img"] = De[i]["img"]
				except: pass
				try:
					if len(De[i]["plot"])>210:
						tmp = De[i]["plot"][:200]
						tmp = tmp[:tmp.rfind(' ')]
						cn[i]["plot"]= tmp+' ...'
					else: 
						cn[i]["plot"]= De[i]["plot"]
				except:
					cn[i]["plot"] = ''
				try:
					cn[i]["type"] = ''
				except: pass
				
			else:
				cn[i] = De[i]
			
		EPG[idx] = cn


def get_nm_dict():
	nm_dict={}
	for i in EPG.keys():
		try:nm_dict[EPG[i]['title']]=i
		except:pass
	return nm_dict


def get_id(name):
	nm2id={}
	nm2id_ext={}
	nml=[]
	for a in DBC.items():
		id=a[0]
		names=a[1]['names']
		for nm in names:
			nm2id[nm]=id
			nml.append(nm)
			nm2id_ext[nm.replace('.','').replace('-','').replace(' ','').replace('канал','').replace('channel','')]=id
	
	name_ext=lower(name).replace('.','').replace('-','').replace(' ','').replace('канал','').replace('channel','')
	
	if lower(name) in nml:
		id = nm2id[lower(name)]
	elif name_ext in nm2id_ext.keys():
		id = nm2id_ext[name_ext]
	else:
		Did=get_nm_dict()
		if name in Did.keys(): id=Did[name]
		else: id = CRC32(lower(name.strip()))
	return id

def uni_mark(nm):
	try:nm=lower(nm.strip())
	except:pass
	return nm

def get_id_2(nm):
	id=CRC32(uni_mark(nm))
	return id

#==============================   Старое ======================================

def POST(target, post=None, referer='http://torrentino.net'):
	#print target
	try:
		req = urllib2.Request(url = target, data = post)
		req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
		req.add_header('X-Requested-With', 'XMLHttpRequest')
		req.add_header('Content-Type', 'application/x-www-form-urlencoded')
		resp = urllib2.urlopen(req)
		#print resp.info()
		http = resp.read()
		resp.close()
		return http
	except Exception, e:
		print e
		return ''


def toutf(s):
	s=eval('u"'+s.replace('"',"''")+'"')
	return s.encode('utf-8')
	
	
	
def tviz():
	import time
	post='city_id=1&category_id=0&genre_id=0&my_channels=none&day='+time.strftime('%Y-%m-%d')
	
	for p in range(55):
		post='offset='+str(p*9)+'&city_id=1&category_id=0&genre_id=0'
		#print p*9
		#h = POST('https://www.tviz.tv/index/more/', post)
		h = getURL('https://www.tviz.tv/index/more/?'+post)
		L=mfindal(h, '<div class=\\"schedule-channel\\">', '<\\/a><\\/span><\\/div><\\/div>')
		for c in L:
			try:
				try: name = mfind(c,'data-name=\\"','\\"')
				except: name = 'error'
				#print name
				idx=get_id(name)
				De={}
				
				nday=False
				tms_prev=0
				
				Le = mfindal(c, '<span class=\\"row', '<\\/a><\\/span>')
				for e in Le:
					try:
						e=e.replace(' title-broadcast','').replace(' time-broadcast','')
						start      =    mfind(e,'time\\">','<')
						#print start
						program_id =    mfind(e,'event_id=','\\"')
						ptitle     =    mfind(e,'title\\">','<')
						etitle = ''
						
						try:strptime=time.strptime(time.strftime('%Y-%m-%d ')+start , '%Y-%m-%d %H:%M')
						except:
								time.sleep(1)
								try:strptime=time.strptime(time.strftime('%Y-%m-%d ')+start , '%Y-%m-%d %H:%M:%S')
								except: strptime=0
						
						tms=str(time.mktime(strptime))
						
						tmt=time.mktime(strptime)
						if tms_prev>tmt: nday=True
						tms_prev=tmt
						if nday: tmt+=86400
						tms=str(tmt)
						
						if program_id!='':img='http://127.0.0.1:'+str(port)+"/tviz/"+program_id+'/cid'+idx+'/tms'+tms
						else: img=''
						#print tms
						#print start+' '+ptitle+'. '+etitle
						De[tms]={"title":ptitle, 'img': img, 'plot': etitle, 'type':''}
					except:
						print e
				De['title']=name
				if settings.get('epg_low')=='true': LOW_EPG(idx, De)
				elif settings.get('epg_mix')=='true': ADD_EPG(idx, De)
				else: EPG[idx]=De
			except:
				print 'err'
	
def mail():
	import json, time
	target='https://tv.mail.ru/ajax/index/'
	
	prev='region_id=70&channel_type=all'
	ext='&appearance=list&period=all'
	dtm='&date='+time.strftime('%Y-%m-%d')
	
	Lc=[[],
	[850,1271,1395,1389,1139,2060,1112,1158,751,1051,2068,1383,986,963,968,1671,1259,1049,717,1162,2097,2338,1670,1193],
	[1973,24,843,732,2360,2391,1959,2373,743,1173,2273,933,1334,1799,736,1362,800,868,975,1008,1092,2186,2025,1340],
	[1462,1519,1612,888,994,1063,1064,1229,1309,1968,1042,1433,2007,1727,1956,2355,2266,2396,1835,713,1234,1607,864,1405],
	[1810,1066,1143,2120,2122,2123,2384,742,905,980,1300,1721,1782,2301,2368,2294,2399,2263,2351,1851,775,1219,1894,2274],
	[1243,889,1944,919,924,1195,1244,1282,1296,1307,1353,1356,1396,1477,1567,1628,1122,2136,729,761,763,792,801,911],
	[1002,1003,1019,1094,896,2137,1050,2048,2167,2281,1266,1333,1343,1707,1993,2350,2324,2356,2425,2035,2195,2285,2363,2375],
	[2413,2173,2216,2153,2243,1027,1800,1566,1718,1926,2154,796,1144,773,787,833,1269,1651,769,1085,1097,1103,1134,1159],
	[1201,1241,808,1249,814,1258,838,1503,907,1669,929,1780,945,1991,1004,2090,1007,2277,1083,2135,2193,2268,2111,2166],
	[2276,974,921,1010,1262,1342,1367,1397,2246,2404,1653,2300,2269,2194,2306,2353,2209,2214,2215,2235,2288,2291,2295,2303],
	[2305,2259,2205,2210,2400,2401,2423,2161,2202,2237,2296,2339,2341,2398,1794,2192,2211,2258,2407,2411,2199,2200,2191,2234],
	[1641,1658,2044,2198,2249,2252,1126,1197,1352,1380,1499,1610,1622,835,900,944,1075,1115,1525,1827,781,996,1136,1141],
	[1204,1384,1623,1684,726,739,1420,2290,2420,1834,2386,1813,2010,1747,2311,1576,1603,745,766,806,1252,1324,1326,1354],
	[1381,1516,2006,2424,1825,2197,2224,2416,2426,2212,2155,2042,1970,1971,1972,715,1038,1716,1739,1185,1346,810,1449,822],
	[1570,834,853,901,942,953,1057,1104,1111,1127,1129,1182,2317,2367,1660,2304,2293,2325,1831,2026,2280,2264,2405,2415],
	[2217,2024,1787,782,946,1128,1302,1378,1759,2326,1778,1652,2262,2298,2320,2206,1666,1687,904,1579,981,1590,1070,1617],
	[1116,1618,1250,1619,1257,1657,1360,1683,1401,2124,1404,2204,1408,2227,1422,1521,1542,786,1557,832,1559,873,1832,1479],
	[1524,1598,2174,1470,1783,1818,2113,2116,2115,1700,2180,1781,1784,1817,1741,1786,1806,2160,2244,2309,2310,2321,2348,2349],
	[2383,1798,2168,1702,1830,2179,1744,1511,2207,2260,2261,2427,1836,1884,1821,2011,2175,1871,1854,2226,2229,2230,1723,2232],
	[2369,1385,1263,1366,1801,1561,1574,943,1382,1507,1528,714,744,1014,1023,1096,1174,1714,950,1255,1429,1624,927,1179]]
	cl=''
	for p in Lc:
		for j in p:
			cl+='&ex='+str(j)
		post=prev+cl+dtm+ext
		#print cl
		L=json.loads(POST(target, post))['schedule']
		for i in L:
			try:
				c = eval(repr(i['channel']).replace("u'","'"))
				try: name = toutf(c['name'])
				except: name = 'error'
				#print name
				idx=get_id(name)
				De={}
				
				nday=False
				tms_prev=0
				
				Le = eval(repr(i['event']).replace("u'","'"))
				for e in Le:
					try:
						start      =    e['start']
						#print start
						program_id =    str(e['id'])
						ptitle     =    toutf(e['name'])
						try: etitle   = toutf(e['episode_title'])
						except: etitle = ''
						
						try:strptime=time.strptime(time.strftime('%Y-%m-%d ')+start , '%Y-%m-%d %H:%M')
						except:
								time.sleep(1)
								try:strptime=time.strptime(time.strftime('%Y-%m-%d ')+start , '%Y-%m-%d %H:%M:%S')
								except: strptime=0
						
						tms=str(time.mktime(strptime))
						
						tmt=time.mktime(strptime)
						if tms_prev>tmt: nday=True
						tms_prev=tmt
						if nday: tmt+=86400
						tms=str(tmt)
						
						
						if program_id!='':img='http://127.0.0.1:'+str(port)+"/cid"+idx+'/tms'+tms+'/program/tv.mail.ru/ajax/event/?id='+program_id+"&region_id=70"
						else: img=''
						#print tms
						#print start+' '+ptitle+'. '+etitle
						De[tms]={"title":ptitle, 'img': img, 'plot': etitle, 'type':''}
					except:
						print e
				De['title']=name
				if settings.get('epg_low')=='true': LOW_EPG(idx, De)
				elif settings.get('epg_mix')=='true': ADD_EPG(idx, De)
				else: EPG[idx]=De
			except:
				print 'err'

def yatv():
	ncrd=str(long(time.time())*1000+1080)
	dtm=time.strftime('%Y-%m-%d')
	
	Lcnl=[1867,1861,1856,1853,1852,1845,1844,1843,1842,1841,1838,1834,1828,1827,1821,1820,1817,1816,1815,1814,1810,1809,1808,1807,1806,161,1804,1803,1802,1799,1798,1794,1793,1790,1785,1784,1783,1782,1781,1780,1778,1767,1773,1772,1766,1765,1764,1763,1762,1761,1760,1759,1757,1755,1754,1753,690,1744,1743,1746,1738,1737,1734,1736,1732,1731,1727,1728,1730,1729,1726,1725,1721,1723,1722,1720,1716,1714,1702,1719,1713,1703,1698,1700,1699,932,1666,363,248,180,509,730,1396,576,141,37,6,783,275,618,1425,217,638,349,431,933,626,442,756,1672,1670,1663,1657,1681,1588,1586,423,1038,741,138,1377,1395,389,1612,1011,1012,331,1043,1042,1034,1031,984,1035,1372,1013,983,987,807,124,1033,382,934,464,1030,560,990,930,415,121,801,631,312,1676,920,663,1329,1026,925,165,412,777,1322,1679,1662,1660,1397,425,776,1571,173,505,919,661,617,779,346,595,547,21,113,931,153,614,637,705,376,434,132,82,393,257,491,156,680,25,662,1021,151,681,927,258,591,642,533,319,715,575,59,589,1331,315,355,461,247,23,495,463,313,921,214,384,831,278,502,743,828,1578,1332,66,810,494,31,917,601,555,929,308,410,567,1669,1668,1667,1376,664,1039,454,850,737,288,455,563,481,328,406,250,1585,669,1562,1365,685,769,223,757,765,1436,1330,1394,521,277,325,365,102,409,912,613,996,35,273,1036,928,322,367,333,774,723,648,520,794,675,55,924,1680,1620,1674,799,1584,834,798,608,644,12,1570,352,516,686,659,821,518,485,53,311,309,918,1037,1371,935,615,994,401,477,125,145,566,542,22,462,123,267,127,1046,1335,100,323,898,1649,1598,150,897,633,726,405,1003,279,304,79,447,689,529,1000,740,1683,187,427,162,1593,597,146,1171]
	
	channelIds=''#'channelIds%22%3A%22'
	for i in Lcnl:
		channelIds+=str(i)+'%2C'
	channelIds=channelIds[:-3]#+'%22'
	
	for n in range(0,36):
		url='https://m.tv.yandex.ru/ajax/i-tv-region/get?params=%7B"channelLimit"%3A10%2C"channelOffset"%3A'+str(n*10)+'%2C"fields"%3A"channel%2Ctitle%2Cchannel%2Cid%2Ctitle%2Clogo%2Csizes%2Cwidth%2Cheight%2Csrc%2Ccopyright%2Cschedules%2Cchannels%2Cchannel%2Cid%2Ctitle%2CavailableProgramTypes%2Celement%2Cid%2Cname%2Cevents%2Cid%2CchannelId%2Cepisode%2Cdescription%2CseasonName%2CseasonNumber%2Cid%2CprogramId%2Ctitle%2Cstart%2Cfinish%2Cprogram%2Cid%2Ctype%2Cid%2Cname%2Ctitle"%2C"channelIds"%3A"'+channelIds+'"%2C"start"%3A"'+dtm+'T03%3A00%3A00%2B03%3A00"%2C"duration"%3A96400%2C"channelProgramsLimit"%3A500%2C"lang"%3A"ru"%7D&userRegion=193&resource=schedule&ncrd='+ncrd
		#print url
		#1469175651563
		try:E=getURL(url)
		except:
			try:E=getURL(url)
			except:
				print 'yatv unavailable'
				return False
		e=E.replace('\\/','/').replace('false','False').replace('true','True').replace('\\"',"'")
		#debug (e)
		try:
			D=eval(e)
			L=D['schedules']
		except:
			L=[]
		#DCnl={}
		
		for i in L:
			try:
				title=i['channel']['title']
				#print title
				channel_id=str(i['channel']['id'])
				idx=get_id(title)
				
				Le=[]
				De={}
				L2=i['events']
				for j in L2:
					start      =    j['start']
					program_id =str(j['program']['id'])
					ptitle     =    j['program']['title']
					try: etitle   = j['episode']['title']
					except: etitle = ''
					try:plot   =    j['program']['description']
					except: plot = ''
					try: type=j['program']['type']['name']
					except: type=''
					if etitle == ptitle: etitle = ''
					if etitle != '': ptitle=ptitle+' '+etitle
					
					cdata = time.strftime('%Y%m%d')
					pdata = start[:10].replace('-','')
					if True:#pdata==cdata:
						start_at=start.replace('+03:00','').replace('T',' ')#2016-07-22T04:20:00+03:00
						#print "-==-=-=-=-=-=-=-=-=-=-"
						try:strptime=time.strptime(start_at , '%Y-%m-%d %H:%M:%S')
						except:
							time.sleep(1)
							try:strptime=time.strptime(start_at , '%Y-%m-%d %H:%M:%S')
							except: strptime=0
						if strptime!=0:
							tms=str(time.mktime(strptime))
							#img='http://127.0.0.1:'+str(port)+'/977/program/'+program_id#+"/cid"+idx+'/tms'+tms
							img='http://127.0.0.1:'+str(port)+'/y_img/'+program_id
							#print tms
							#Le.append({"title":rt(ptitle), "start_at":start_at, 'img': img})
							#plot=plot[:301]
							De[tms]={"title":rt(ptitle), 'img': img, 'plot': plot, 'type':type}
				#E2=repr(Le)
				#Ed=repr(De)
				De['title']=title
				#pDialog.update(int(n*100/31), message=title)
				if idx!="":
					if settings.get('epg_low')=='true': LOW_EPG(idx, De)
					elif settings.get('epg_mix')=='true': ADD_EPG(idx, De)
					else: EPG[idx]=De
			except:
				pass


def upd_programtv():
	url='http://programtv.ru/xmltv.xml.gz'
	xml=dload_epg_xml(url)
	if xml=="": xml=dload_epg_xml(url)
	if xml!="":
		d=pars_xmltv2(xml)

def upd_stv_off():
	opener = urllib2.build_opener()
	opener.addheaders.append(('Cookie', 'favorites=1TV%3BRTR%3BNTV%3BMIR%3BTVC%3BKUL%3BMatchTV%3BTNT%3BDOMASHNIY%3BRenTV%3BSTS%3BPiter5_RUS%3BZVEZDA%3BChe%3BKarusel%3B2X2%3BDisney%3BU%3BTV3%3BOTR%3BFriday%3BVesti%3BSuper%3BTNT_4%3BMOSCOW-24%3BDOVERIE%3BProdvige%3BFAMILY%3BAmedia1%3BAMEDIA%3Bntv%2B41%3BAmediaHit%3BBollywood%3BDetektive%3BEurochanne%3BFilmBoxArh%3BFOX%20CRIME%3BFOX%20LIFE%3BPARAMAUNT%3BParaComedy%3BSET_RUSSIA%3BAXNSciFi%3BSonyTurbo%3BSpike%3BTV1000%3BTV1000_Act%3BTV1000_RK%3BTV21%3BZee-TV%3BDomKino%3BDomKinoP%3BDorama%3BEuroKINO%3BILLUSION%2B%3BIndia%3BKaleidosco%3BKinoUHD%3BKinoTV%3BKomedia%3Bntv%2B34%3BKinipokaz%3BKinop_HD-1%3BKinop_HD-2%3BKinoPrHD%3Bntv%2B10%3Bntv%2B4%3BHDKino%3BmnogoTV%3Bntv%2B40%3BClassKino%3BKomedia1%3BMir_serial%3BMenKino%3BNSTV%3Bnashdetekt%3Bnashkinor%3BNasheLubim%3Bntv%2B7%3BNTVserial%3BNTVHit%3BOstroHD%3Bntv%2B3%3BRTVi-LK%3BRTVi-NK%3BRus-Bestst%3BRuDetektiv%3BRU_ILLusio%3BRusRoman%3BSerialUHD%3BStrahnoeHD%3BSTSLove%3BTelenovell%3BFeniks%3Bntv%2B13%3BEuro-2%3BEurospGold%3BEurospNews%3Bntv%2B23%3BFightBox%3BM-1GLOBAL%3BRu_ExtUHD%3BViasatGolf%3BViaGolfHD%3BVia_Sport%3BBoxingTV%3BMatchKmir%3BMatcharena%3Bboets%3BMatchigra%3BMatchsport%3Bntv%2B11%3Bntv%2B44%3BSporthit%3BNautical%3Bntv%2B1%3BRU_Extrem%3BStart%3Bntv%2B9%3BKHL_HD%3BFootBallTV%3BArirang%3Bntv%2B25%3BBBC_Entert%3BBBC-World%3Bntv%2B33%3BCCTVNews%3BCNBC%3Bntv%2B30%3BCNN_ENG%3BDW%3BDW_DEU%3Bntv%2B19%3BFrance24%3BFrance_FR%3BJSTV%3BNewsOne%3BNHK_World%3BRus_Today%3BRTArabic%3BRT_Doc%3BRTEspanol%3BRTDrus%3BBelarus-TV%3BRAIN%3BIzvestiy%3BKommers_TV%3BLDPR%3BMir24%3BRBK%3B4P.INFO%3BEhoFilm%3B365_day%3Bntv%2B17%3BDa%20Vinci%3Bntv%2B16%3BDiscov_VE%3Bntv%2B28%3BHistor2%3BHHD2%3BHistor%20%3BHistoryENG%3Bntv%2B18%3BOCEAN-TV%3BExplorer%3BHistory%3BViaHistHD%3BNature_CEE%3BZooTV%3BZoopark%3BVopr-Otvet%3BDoctor%3BEGE%3BGivPlaneta%3BJivPriroda%3BJivPriHD%3BIstoria%3BWho_is_who%3BMosObrazov%3BMy_Planet%3BNANO_TV%3BNauka_2.0%3B1Obrazovat%3BProsvejeni%3BSinergiaTV%3BTop_secret%3BGalaxy_TV%3B1HD%3B360TuneBox%3BBridgeHD%3BBridge-TV%3BTOPSONG_T%3BDangeTV%3BRusong_TV%3BC_Music_TV%3BClubbingTV%3BEuropaPlus%3BFestival4K%3BFreshtv%3BHardLifeTV%3BHitv%3BJuCeTV%3BMCMTOP%3Bntv%2B26%3BMTVDI%3BMTVHI%3BMTVRI%3BMTVRus%3BMTV_AM%3BMusicBox-T%3BRAP%3BRU-TV%3BMusicBox-R%3BiConcerts%3BTMBRU%3BVH1_Class%3BVH1_EURO%3BLa-minor%3BMUZ_TVnew%3BMuZ-One%3BMultmuzika%3BO2TV%3BA-ONE%3BSHANSON%3BTV7%3BC4K360%3BReality%3BCCTV4%3BCCTV%3BPark_Razvl%3BDTXEMEA%3BGame_Show%3BEnglishClu%3BFash_One%3BFashion_4K%3BFashion_TV%3BFLN%3BFoodNet%3BFoodmanClu%3BFuel_TV_HD%3BGlobalStar%3BHome4K%3BInsiUlHD%3BLuxe_TV%3BMotors_TV%3BMuseum_HD%3Bntv%2B20%3BNoise_%3BOutdoor%3Bprodengi%3BRTGInt%3BRusHualiTV%3BRTG_TV%3BStyle%26moda%3BShoppingLi%3BSlow%3BTDK%3BTLC%3BTop%20Shop%20T%3BTrChenel%3BTravel%2BAdv%3BTrick%3BTVclub%3BTV_SALE%3Bntv%2B32%3BTVMChannel%3BTvRus%3BWBC%3BW_Fashion%3Bautoplus%3BAvto24%3BAnekdotTV%3BBalansTV%3BBober%3BBolshAziy%3BBUMTV%3BSovetFeder%3BVremya%3BDaivingTV%3BdialogiRib%3BDikayOhHD%3BDikayRybHD%3BDikiy%3BD_Jivotnie%3BDomMagazin%3BDrive_MTU%3BEDA%3BBulvar%3BJiVi%3BZagorod_zh%3Bzagorodny%3BZagorodInt%3BZdorov_MTU%3BTONUS-TV%3BKVNTV%3BKuhna%3BMirUvlech%3BMuzhskoj%3BNadegda%3BNeizPlanet%3BNostalgi%3BNTVpravo%3BNTVstil%3BWeapons%3BHa%26Fi_MTU%3BOhot%26Ribal%3BOhotRibInt%3BPervVegeta%3BPesiKo%3BPoehali%3BPsihology%3BRaz-TV%3BRetro_MTU%3Bsarafan-tv%3BSojuz%3BSPAS%3BTvoiDom%3BTvTur%3BTeatr%3BTeledom%3BTelekafe%3BTeletravel%3BTehno24%3B3Angela%3BUsadba_MTU%3BUspeh%3BCentralTV%3BEgoist-TV%3BUvelir%3BHUMOUR-TV%3BAni%3BBaby_TV%3BBoomerang%3Bntv%2B29%3BGingerHD%3BGulli%3BJIMJAM%3BNick_Jr%3Bntv%2B15%3BNickelodHD%3BTiJi%3BVgostskaz%3BDetskiy%3Bntv%2B39%2B8%3BDetskoeRad%3BLubimoetv%3BMalysh%3BMother%26Chi%3BMult%3BMyltikHD%3BMultimania%3BO%3BPingLolo%3BRadost_moj%3BRigiy%3BTlumHD%3B360dHD%3BAmediaPRHD%3BAnimalPlHD%3BArteHD%3BDocuBoxHD%3BEuroSporHD%3BEurospGHD%3BFashBoxHD%3BFashiOneHD%3BFashion_HD%3BFaFuBoxHD%3BFilmBoxHD%3BFoodNetHD%3BFOXLIFE_HD%3BHD-Life%3BHD_Media%3BHD_Media3D%3BLuxe_TV_HD%3BMezzoLive%3BMGM_HD%3BMTV_LiveHD%3BNatGeoW_HD%3BNat_Geo_HD%3BOutdoor%20HD%3BParamounHD%3BRTDrushd%3BRussiaMBHD%3BSETHD%3BSET_HD%3BTr_Chan_HD%3BTravAdHD%3BTV1000Come%3BTV1000Mega%3BTV1000Prem%3BAnFamilHD%3BRAIN_HD%3BDomKinoPHD%3BEDA_HD%3BKinoTVHD%3BMatchareHD%3BMirHD%3BOhotRybHD%3B1TVHD%3BIQHD%3BTeleTravHD%3BRTRHD%3BRRomanHD%3BTNTHD%3BEurekaHD%3BBabesTV%3BBarely%3BBlueHust24%3BBlueHust%3BCandy3D%3BCandy%3BDaring!TV%3BErox%3BHustle3DHD%3BHustler%3BPlayboy_TV%3BIskushenie%3BNightClub%3BRusnight%3BShalun%3BShalunHD%3B360d%3B8_KANAL%3BShantPrem%3BTRO%3BVesnaFM%3BKBSrus%3BKrasLin%3BLiderTV%3BMarusyFM%3BNasheTV%3BNovoeradio%3BNewworld%3BOpenworld%3B1_Meteo%3BRatnik%3BRGD%3BTBN%3BTNV%3BTNV_PL%3BTnomer%3BTochkaOtr%3BToshkaTV'))

	urllib2.install_opener(opener)
	url = 'http://new.s-tv.ru/tv/-/'+time.strftime('%Y-%m-%d')+'/'
	http = getURL(url)
	ss='<td class="channel">'
	es='<table class="item_table">'
	L=mfindal(http,ss,es)
	epg={}
	n=0
	tt=len(L)
	for i in L:
		n+=1
		#try:
		if i!="":
			ss='width="45px" title="'
			es='" />'
			cnl_nm=mfindal(i,ss,es)[0][len(ss):]
			idx=get_id(cnl_nm)
			if idx!="":
				ss='<div class="prg_item">'
				es='</div>'
				L2=mfindal(i,ss,es)
				Le=[]
				De={}
				nday=False
				tms_prev=0
				for j in L2:
					
					#print j
					type=''
					if 'class="live"' in j:  type='live'
					if 'class="info"' in j:  type='info'
					if 'class="new"' in j:   type='new'
					if 'class="movie"' in j: type='movie'
					if 'сезон.' in j:        type='tvshow'
					if 'Футбол.' in j:       type='sport'
					if 'Хоккей.' in j:       type='sport'
					if 'Ралли.' in j:       type='sport'
					if 'спорт.' in j:       type='sport'
						
					j=j.replace('span', 'span\n')
					Ls=j.splitlines()
					title=''
					st=''
					img_id=''
					for t in Ls:
						if 'prg_item_no' in t: title=mfind(t,'item_no">','</span')
						if 'item_time'  in t: st=mfind(t, 'time">','</span')
						if 'href'  in t: 
							img_id=mfind(t, 'href="#ab','">')
							title=mfind(t,'">','</a>')
					
					title=title.replace('<spa','')
					#print cnl_nm+" "+st+" "+title+" "+img_id
			
					start_at=time.strftime('%Y-%m-%d')+" "+st#+":00"
					strptime=time.strptime(start_at , '%Y-%m-%d %H.%M')
					tmt=time.mktime(strptime)
					
					if tms_prev>tmt: nday=True
					tms_prev=tmt
					if nday: tmt+=86400
					tms=str(tmt)
					
					if img_id!='':img='http://127.0.0.1:'+str(port)+"/cid"+idx+'/tms'+tms+'/program/new.s-tv.ru/tv/ajaxinfo/'+img_id+"/0"
					else: img=''
					De[tms]={"title":rt(title), 'img': img, 'plot': '', 'type':type}
					
				De['title']=cnl_nm
				#EPG[idx]=De
				#ADD_EPG(idx, De)
				if settings.get('epg_mix')=='true': ADD_EPG(idx, De)
				else: EPG[idx]=De

				#pDialog.update(int(n*100/tt), message=cnl_nm)


def upd_EPG_vsetv(pack):
	#url = 'http://www.vsetv.com/schedule_package_'+pack+'_day.html'
	#post='submit.x=109&submit.y=16&dset11=2&dset12=1&dset21=2&dset22=1'
	#ht = get_HTML(url, post)
	
	url1='http://www.vsetv.com/rewrite_url.php'
	url2 = 'http://www.vsetv.com/schedule_printversion_withdesc.html'
	post='timezone=14&selected_channel=package_'+pack+'&submit.x=109&submit.y=16&dset11=2&dset12=1&dset21=2&dset22=1'
	ht = get_HTML(url1, post, url2)
	ht = get_HTML(url2)
	
	main=mfind(ht, '<td class="main">', 'class="bottomline">')
	if main!='':
		#print "main"
		#print main
		L=mfindal(main, 'class="chname"', 'class="clearshed"')
		for i in L:
			try:
				i=i.decode('windows-1251')
				i=i.encode('utf-8')
				i=i.replace('class="past','class="').replace('class="onair"','class="time"').replace('<div class="time">','\n<div class="time">')
				#i=i.replace('<a class=f0></a>','0').replace('<a class=d9></a>','0').replace('<a class=z0></a>','0')
			except: pass

			#print i
			name=mfind(i,'class="channeltitle">','</td>')
			
			Lrepl=[' (русский)', ' (Русский)', ' (Россия)', ' Россия', ' (Europe)']
			for j in Lrepl:
				name=name.replace(j,'')
			
			idx=get_id(name)
			#print "-==-=-=-=-"+name+'=-=-=-=-=-'
			L2=i.splitlines()
			nday=False
			tms_prev=0
			De={}
			for sl in L2:
				if 'class="time"' in sl:
					
					#print sl
					st=mfind(sl,'class="time">','</div><div')
					
					
					ptitle=mfind(sl,'prname2">','</div>')
					if 'absmiddle">&nbsp;' in ptitle: ptitle=mfind(ptitle,'absmiddle">&nbsp;','</div>')
					
					ptitle=ptitle.replace('<b>','').replace('</b>','').replace('</b','')
					
					#if '<img src' in sl: img='http://www.vsetv.com'+mfind(sl,'<img src="','" border=0 hspace=5')
					#else: img=""
					#print img
					if 'class="desc">' in sl and '<br><br>' in sl: 
						if '...' in sl: se='...'
						else: se='<div'
						plot=mfind(sl,'<br><br>',se)+"..."
					else: plot=''
					
					if len(ptitle)>80 and '", ' in ptitle:
						plot2=ptitle[ptitle.find('", ')+3:]
						ptitle=ptitle[:ptitle.find('", ')]
						plot=plot2+'\n'+plot
					elif len(ptitle)>80 and '. ' in ptitle:
						plot2=ptitle[ptitle.find('. ')+2:]
						ptitle=ptitle[:ptitle.find('. ')]
						plot=plot2+'\n'+plot
					elif len(ptitle)>80 and ': ' in ptitle:
						plot2=ptitle[ptitle.find(': ')+2:]
						ptitle=ptitle[:ptitle.find(': ')]
						plot=plot2+'\n'+plot
					
					#print '...............................'
					#print st
					#print ptitle
					#print plot
					
					
					HM=time.strptime(st, '%H:%M')
					H=HM[3]
					M=HM[4]
					ctime=time.gmtime(time.time()+3*60*60)
					ntime=(ctime[0],ctime[1],ctime[2],H,M,0,ctime[6],ctime[7],ctime[8])
					tmt=time.mktime(ntime)
					#print tmt
					'''
					start_at=time.strftime('%Y-%m-%d')+" "+st#+":00"
					strptime=time.strptime(start_at , '%Y-%m-%d %H:%M')
					tmt=time.mktime(strptime)
					print ' '
					print tmt
					'''
					if tms_prev>tmt: nday=True
					tms_prev=tmt
					if nday: tmt+=86400
					tms=str(tmt)
					#print time.ctime(tmt)
					De[tms]={"title":rt(ptitle), 'img': '', 'plot': plot}
					
			De['title']=name
			#EPG[idx]=De
			if settings.get('epg_low')=='true': LOW_EPG(idx, De)
			elif settings.get('epg_mix')=='true': ADD_EPG(idx, De)
			else: EPG[idx]=De


def upd_EPG_xmltv():
	xml=dload_epg_xml()
	if xml=="": xml=dload_epg_xml()
	if xml!="":
		d=pars_xmltv3(xml)

def dload_epg_xml(target=''):
	try:
			#target='http://programtv.ru/xmltv.xml.gz'
			if target=='': target='https://iptvx.one/epg/epg.xml.gz'#'http://api.torrent-tv.ru/ttv.xmltv.xml.gz'
			#print "-==-=-=-=-=-=-=- download =-=-=-=-=-=-=-=-=-=-"
			fp = os.path.join(settings.UserDir, 'tmp.zip')
			
			req = urllib2.Request(url = target, data = None)
			req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
			resp = urllib2.urlopen(req)
			fl = open(fp, "wb")
			fl.write(resp.read())
			fl.close()
			
			time.sleep(1)
			#print "-==-=-=-=-=-=-=- unpak =-=-=-=-=-=-=-=-=-=-"
			xml=ungz(fp)
			#print "-==-=-=-=-=-=-=- unpak ok =-=-=-=-=-=-=-=-=-=-"
			#os.remove(fp)
			return xml
	except Exception, e:
			print 'HTTP ERROR ' + str(e)
			return ''


def ungz(filename):
	import gzip
	with gzip.open(filename, 'rb') as f:
		file_content = f.read()
		f.close()
		return file_content


def get_ttv_epg_id():
	E=getURL('http://torrent-tv.ru/news.php')
	L=mfindal(E,'<li ','</li>')
	D={}
	for i in L:
		if 'data-epg-id' in i:
			epg_id=i[i.find('epg-id="')+8:i.find('">')]
			ttv_id='ttv'+i[i.find('translation=')+12:i.rfind('">')]
			print epg_id+" > "+ttv_id
			D[ttv_id]=epg_id
	return D

def pars_xmltv(xml):
	xml=xml.replace(chr(10),"").replace(chr(13),"").replace("<programme ", "\n<programme ").replace("<channel ", "\n<channel ")
	L=xml.splitlines()
	cdata = time.strftime('%Y%m%d')
	epg={}
	channel={}
	#epg_id=get_ttv_epg_id()
	n=0
	for i in L:
		if "<channel " in i:
			channel_id=i[i.find('id="')+4:i.find('"><display')]
			name=i[i.find('"ru">')+5:i.find('</display-name>')]
			cid=get_id(name)
			#if cid not in EPG.keys(): EPG
			channel[channel_id]={'id':cid, 'name':name}
		if "<programme " in i:
			n+=1
			title=i[i.find('<title lang="ru">')+17:i.find('</title>')]
			if 'desc' in i: desc=i[i.find('<desc lang="ru">')+16:i.find('</desc>')]
			else: desc=''
			if '<category' in i: cat=i[i.find('<category lang="ru">')+20:i.find('</category>')]
			else: cat=''

			start_at=i[i.find('start="')+7:i.find(' +0300')]
			ttv_id=i[i.find('channel="')+9:i.find('">')]
			cid=channel[ttv_id]['id']
			cnm=channel[ttv_id]['name']
			
			strptime=time.strptime(start_at , '%Y%m%d%H%M%S')
			tms=str(time.mktime(strptime))
			
			img=''
			
			if cid not in EPG.keys(): EPG[cid] = {'title':cnm}
			EPG[cid][tms]={"title":rt(title), 'img': img, 'plot': desc, 'type': cat}
			

def pars_xmltv3(xml):
	xml=xml.replace(chr(10),"").replace(chr(13),"").replace("<programme ", "\n<programme ").replace("<channel ", "\n<channel ")
	L=xml.splitlines()
	cdata = time.strftime('%Y%m%d')
	epg={}
	channel={}
	#epg_id=get_ttv_epg_id()
	n=0
	for i in L:
		if "<channel " in i:
			channel_id=i[i.find('id="')+4:i.find('"><display')]
			name=i[i.find('<display-name>')+14:i.find('</display-name>')]
			cid=get_id(name)
			#if cid not in EPG.keys(): EPG
			channel[channel_id]={'id':cid, 'name':name}
		if "<programme " in i:
			n+=1
			title=i[i.find('<title lang="ru">')+17:i.find('</title>')]
			if 'desc3' in i: desc=i[i.find('<desc lang="ru">')+16:i.find('</desc>')]
			else: desc=''
			if '<category' in i: cat=i[i.find('<category lang="ru">')+20:i.find('</category>')]
			else: cat=''
			
			start_at=i[i.find('start="')+7:i.find(' +0300')]
			ttv_id=i[i.find('channel="')+9:i.find('">')]
			cid=channel[ttv_id]['id']
			cnm=channel[ttv_id]['name']
			
			strptime=time.strptime(start_at , '%Y%m%d%H%M%S')
			tms=str(time.mktime(strptime))
			
			img=''
			
			if cid not in EPG.keys(): EPG[cid] = {'title':cnm}
			EPG[cid][tms]={"title":rt(title), 'img': img, 'plot': desc, 'type': cat}

def pars_xmltv2(xml):
	xml=xml.replace(chr(10),"").replace(chr(13),"").replace("<programme ", "\n<programme ").replace("<channel ", "\n<channel ").replace("&quot;", '"')
	L=xml.splitlines()
	cdata = time.strftime('%Y%m%d')
	epg={}
	channel={}
	n=0
	for i in L:
		if "<channel " in i:
			channel_id=i[i.find('id="')+4:i.find('">')]
			name=i[i.find('<display-name>')+14:i.find('</display-name>')]
			cid=get_id(name)
			#if cid not in EPG.keys(): EPG
			channel[channel_id]={'id':cid, 'name':name}
		if "<programme " in i:
			n+=1
			title=i[i.find('<title>')+7:i.find('</title>')]
			if '<category' in i: cat=i[i.find('<category>')+10:i.find('</category>')]
			else: cat=''
			if 'desc' in i: desc=i[i.find('<desc>')+6:i.find('</desc>')]
			else: desc=cat

			start_at=i[i.find('start="')+7:i.find(' +0300')]
			ttv_id=i[i.find('channel="')+9:i.find('">')]
			cid=channel[ttv_id]['id']
			cnm=channel[ttv_id]['name']
			
			strptime=time.strptime(start_at , '%Y%m%d%H%M%S')
			tms=str(time.mktime(strptime))
			
			img=''
			
			if cid not in EPG.keys(): EPG[cid] = {'title':cnm}
			EPG[cid][tms]={"title":rt(title), 'img': img, 'plot': desc, 'type': cat}


# --------------------------------------------------

XMLTV={'data':''}
def xmltv2():
	if XMLTV['data']!='': return XMLTV['data']
	print '== xmltv =='
	req = '<?xml version="1.0" encoding="utf-8" ?><!DOCTYPE tv SYSTEM "http://www.teleguide.info/download/xmltv.dtd"><tv generator-info-name="TVH_W/0.751l" generator-info-url="http://www.teleguide.info/">\n'
	nm_dict=get_nm_dict()
	lid = []
	for nm in nm_dict.keys():
		id=nm_dict[nm]
		lid.append(id)
		cnl = '<channel id="'+id+'"><display-name lang="ru">'+nm+'</display-name></channel>\n'
		req+=cnl
		
	for cid in lid:
		info=get_inf_db(cid)
		L=info.keys()
		try:L.remove('title')
		except: pass
		L.sort()
		for i in L:
			n1=L.index(i)
			n0=n1-1
			if n0>=0: 
				title=info[L[n0]]['title']
				ts=eval(L[n0])-3*60*60
				te=eval(L[n1])-3*60*60
			
				start=time.strftime('%Y%m%d%H%M%S', time.gmtime(ts))#20190503014000
				stop =time.strftime('%Y%m%d%H%M%S', time.gmtime(te))#20190503023000
				
				prg = '<programme start="'+start+' +0300" stop="'+stop+' +0300" channel="'+cid+'"><title lang="ru">'+title+'</title></programme>\n'
				req+=prg
	req+='</tv>'
	XMLTV['data']=req
	return req

class xmltv():
	def __init__(self):
		self.ct = time.time()
		self.epg_low = settings.get('epg_low')
		if settings.get('autoshift')!='false':
			self.dts=time.timezone
		else:
			self.dts=(int(settings.get('shift')))*3600
		print self.dts
		self.rev_link={}
		for i in link_cnl.keys():
			self.rev_link[link_cnl[i]]=i
	
	def cnl_part(self, L=[]):
		print '== xmltv =='
		req = '<?xml version="1.0" encoding="utf-8" ?><!DOCTYPE tv SYSTEM "http://www.teleguide.info/download/xmltv.dtd"><tv generator-info-name="TVH_W/0.751l" generator-info-url="http://www.teleguide.info/">\n'
		nm_dict=get_nm_dict()
		lid = []
		for nm in nm_dict.keys():
			id=nm_dict[nm]
			if id in L or L==[]:
				try:    nms = core.DBC[self.rev_link[id]]['title']
				except: nms = nm.replace('<','[').replace('>',']').replace('&','&amp;')
				lid.append(id)
				cnl = '<channel id="'+id+'"><display-name lang="ru">'+nms+'</display-name></channel>\n'
				req+=cnl
		return [req, lid]
		
	def prg_part(self, cid):
		#for cid in lid:
			req=''
			info=get_inf_db(cid)
			#if cid in self.rev_link.keys(): cid=self.rev_link[cid]
			#if cid in link_cnl.keys(): cid=link_cnl[cid]
			L=info.keys()
			try:L.remove('title')
			except: pass
			L.sort()
			for i in L:
				n1=L.index(i)
				n0=n1-1
				if n0>=0: 
					p_inf=info[L[n0]]
					title= p_inf['title'].replace('<','[').replace('>',']').replace('&','&amp;')
					plot = p_inf['plot'].replace(chr(10),'').replace(chr(13),'').replace('</div>','').replace('</','').replace('<','[').replace('>',']').replace('&','&amp;').strip()
					img  = p_inf['img']
					ts=eval(L[n0])#-3*60*60-self.dts
					te=eval(L[n1])#-3*60*60-self.dts
					#print time.localtime(ts)
					#print time.gmtime(ts)
					'''
					z=int(self.dts/60/-60)
					if z<0:
						if z<-9:sz=' '+str(z)+'00'
						else:   sz=' -0'+str(z)[1:]+'00'
					elif z>0:
						if z>9: sz=' +'+str(z)+'00'
						else:   sz=' +0'+str(z)+'00'
					else: sz=''
					'''
					if te >= self.ct:
						start=time.strftime('%Y%m%d%H%M%S', time.gmtime(ts))#+sz#20190503014000
						stop =time.strftime('%Y%m%d%H%M%S', time.gmtime(te))#+sz#20190503023000
						#print start+' '+stop+' '+title
						
						#prg = '<programme start="'+start+' +0300" stop="'+stop+' +0300" channel="'+cid+'">\n'
						prg = '<programme start="'+start+'" stop="'+stop+'" channel="'+cid+'">\n'
						prg +='<title lang="ru">'+title+'</title>\n'
						prg +='<desc lang="ru">'+plot+'</desc>\n'
						if self.epg_low!='true': prg +='<icon src="'+img+'"/>\n'
						prg +='</programme>\n'
						req+=prg
			return req
		
	def end_part(self):
		req='</tv>'
		#XMLTV['data']=req
		return req


def clear_EPG():
	print 'clear_EPG'
	for cid in EPG.keys():
		cnl=EPG[cid]
		try:CL=cnl.keys()
		except:CL=[]
		for tm in CL:
			if tm!='title':
				if time.time()-eval(tm) > 4*60*60:
					#print cid+' '+tm
					EPG[cid].pop(tm, '')

def debug_epg(cid):
	if cid in link_cnl.keys(): cid=link_cnl[cid]
	info=get_inf_db(cid)
	L=info.keys()
	print "debug_epg " + info['title']
	try:L.remove('title')
	except: pass
	L.sort()
	s=''
	for tm in L:
		t=time.ctime(eval(tm))
		ttl=info[tm]['title']
		si=t+" "+ttl
		print si
		s=s+si+'\n'
	return s


def change_id(cid1, cid2):
	print cid1+' change_id_to '+cid2
	if cid2 == '000000': link_cnl.pop(cid1, '')
	else: link_cnl[cid1]=cid2
	save_d(link_cnl)
	#info=get_inf_db(cid1)
	#EPG.pop(cid1, '')
	#EPG[cid2]=info
	#save_EPG()


def get_channels_info(cid):
	info=get_inf_db(cid)
	
	try:L=info.keys()
	except:
		print 'info err:'
		print info
		return []
		
	try:L.remove('title')
	except: pass
	L.sort()
	if settings.get('autoshift')!='false':
		dts=time.timezone
	else:
		dts=(int(settings.get('shift')))*3600
	#print dts
	ct=time.time()
	m_ct=ct+dts
	#print ct
	for i in L:
		#print i
		try:ei=eval(i)-3*60*60
		except:
			print '!except eval(i)!'
			ei=0
		if ei > m_ct:
			#print 'ok'
			n1=L.index(i)
			n0=n1-1
			n2=n1+1
			e1=info[L[n1]]
			e1['time']=str(eval(L[n1])-3*60*60-dts)
			if n0>=0: 
				e0=info[L[n0]]
				e0['time']=str(eval(L[n0])-3*60*60-dts)
			else:e0={}
			if n2<len(L): 
				e2=info[L[n2]]
				e2['time']=str(eval(L[n2])-3*60*60-dts)
			else:e2={}
			Lr=[e0,e1,e2]
			#print Lr
			return Lr
	
	#if 'title' in info.keys():title=info['title']
	#else:title='Неизвестный канал'
	#print "NoEPG " +cid+' '+title
	return []

#get_channels_info('F79F4A92')
#print 'debug'
#debug_epg('7944E7D0')
#upepg()

def get_current_epg(ps='0'):
	#print ps
	try:p=int(ps)
	except: p=0
	print 'run get_current_epg()'
	D={}
	n=0
	for cid in get_channels_list():
		if n>=(p-1)*100: 
			#print cid
			if cid!='udata':
				nfo=get_channels_info(cid)
				if cid in link_cnl.keys(): cid=link_cnl[cid]
				D[cid]=nfo
			if n > 0 and n >= 100*p: return D
		n+=1
	
	if D=={}:
		for cid in link_cnl.keys():
			id=link_cnl[cid]
			D[cid]=get_channels_info(id)

	return D

def get_all_current_epg():
	D={}
	for cid in get_channels_list():
			if cid!='udata': D[cid]=get_channels_info(cid)
				
	for cid in link_cnl.keys():
			id=link_cnl[cid]
			D[cid]=get_channels_info(id)
	return D


def get_channels_list():
	try:
		L=[]
		for cid in EPG.keys():
			if cid in link_cnl.keys(): cid=link_cnl[cid]
			L.append(cid)
		return L
	except: 
		print 'except: get_channels_list()'
		return []

def save_EPG():
		EPG['udata']=time.strftime('%Y%m%d')
		fp=os.path.join(settings.UserDir, 'EPGdb.py')
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('EPG={\n')
		for i in EPG.items():
			fl.write("'"+i[0]+"':"+repr(i[1])+',\n')
		fl.write('}\n')
		fl.close()

#print get_current_epg()

import os
import socket
import time
import sys

def load_img(target):
	try:
			req = urllib2.Request(url = target, data = None)
			req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
			resp = urllib2.urlopen(req)
			return resp.read()
	except:
			print "err:  "+target
			return None

def get_img(addres):
	#try:
		if 's-tv.ru' in addres:
			#print 'stv img'
			if 'cid' in addres:
				cid=addres[addres.find('/cid')+4:addres.find('/tms')]
				tms=addres[addres.find('/tms')+4:addres.find('/program')]
				addres=addres[addres.find('/program'):]
			else:
				cid=''
			#print 'cid:'+cid
			url=addres.replace('/program/','http://')
			#print url
			http=getURL(url)
			if http=='': return ''
			img=mfind(http,'<img src="','" style=')
			#print img
			if cid!='':
				#print 'DESC'
				try:
					if '<h4>' in http: tmp1=mfind(http,'<h4>','</h4>')
					else:  tmp1=''
				except:
					print 'err tmp1'
					tmp1=''
				try:
					if 'ajax-info-desc' in http: tmp2=mfind(mfind(http,'ajax-info-desc','<script type'),'<p>','</p>')
					else: tmp2=''
				except:
					print 'err tmp2'
					tmp2=''
				
				if tmp1!='': desc=tmp1+"\n"+tmp2
				else: desc=tmp2
				#print xt(desc)
				if desc!="":
					EPG[cid][tms]['plot']=desc
		elif "/tviz/" in addres:
			id=addres[addres.find('/tviz/')+6:addres.find('/cid')]
			cid=addres[addres.find('/cid')+4:addres.find('/tms')]
			tms=addres[addres.find('/tms')+4:]
			url='https://www.tviz.tv/card/?event_id='+id
			http=getURL(url)
			if http=='': return ''
			img='https://www.tviz.tv'+mfind(http,'<img id="picture" src="','"')
			if cid!='':
				desc=rt(mfind(http,'<div class="description">','<'))
				if desc!="":
					EPG[cid][tms]['plot']=desc
			
		elif 'tv.mail.ru' in addres:
			#print 'stv img'
			if 'cid' in addres:
				cid=addres[addres.find('/cid')+4:addres.find('/tms')]
				tms=addres[addres.find('/tms')+4:addres.find('/program')]
				addres=addres[addres.find('/program'):]
			else:
				cid=''
			#print 'cid:'+cid
			url=addres.replace('/program/','http://')
			#print url
			http=getURL(url)
			if http=='': return ''
			import json
			j=json.loads(http)['tv_event']
			img=j['sm_image_url']
			#print img
			if cid!='':
				try:    desc=toutf(j['descr'])
				except: desc=''
				#print xt(desc)
				if desc!="":
					EPG[cid][tms]['plot']=desc
		
		else:
			url='https://m.tv.yandex.ru'+addres.replace('/y_img/', '/146/program/')
			print url
			http=getURL(url)
			if http=='': return ''
			if 'yandex.net/get-tv-shows' in http:
				img='https://avatars.mds.yandex.net/get-tv-shows'+mfind(http,'//avatars.mds.yandex.net/get-tv-shows','"')
				img=img.replace('/small','/normal').replace('/large','/normal')
			elif 'yandex.net/get-kino-vod' in http:
				img='https://avatars.mds.yandex.net/get-kino-vod-films-gallery'+mfind(http,'//avatars.mds.yandex.net/get-kino-vod-films-gallery','"')
			else:
				img=''
		return img
	#except:
	#	return ''


#--------------------------------------------

def get_on(addres):
		print addres
		data=''
		if 'current' in addres:
			if '/p=' in addres: 
				p=addres[addres.find('/p=')+3:]
				data=repr(get_current_epg(p))
			else: 
				data=repr(get_all_current_epg())
			
		if  'debug' in addres:
			cid=addres[addres.rfind('/')+1:]
			data=debug_epg(cid)

		if  'update' in addres:
			data="update"
			upepg()
		
		if  'change/id' in addres:
			cid1=addres[addres.find('/id=')+4:addres.find('/to=')]
			cid2=addres[addres.find('/to=')+4:]
			data="change id"
			change_id(cid1, cid2)

		if  'channels' in addres:
			try:
				cid=addres[addres.rfind('/')+1:]
				#print cid
				if   cid == 'all':	data=repr(get_channels_list())
				elif cid =='dict':	data=repr(get_nm_dict())
				elif len(cid)>4:	data=repr(get_channels_info(cid))
				else: 				data="id:"+'None'
			except:
				print "ERR EPG "+addres
				data="ERR 404"
		
		if  'channel/full/id' in addres:
			cid=addres[addres.find('/id=')+4:]
			data=repr(get_inf_db(cid))
		
		if  'channel/json/dict' in addres:
			data=json.dumps(get_nm_dict())

		if  'channel/json/id' in addres:
			cid=addres[addres.find('/id=')+4:]
			if   cid == 'all':	data=json.dumps(EPG)
			else : 				data=json.dumps(get_inf_db(cid))
			
		if  'program' in addres:
			redir=get_img(addres)
			if redir=='': redir='http://kolomiets.by/wp-content/uploads/2016/03/error-768x432.jpg'
			if redir=='': data="ERR 404"
			else:         data=redir
		return data

#upepg()
#XMLTV=xmltv()