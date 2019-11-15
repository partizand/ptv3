# coding: utf-8
# Module: server
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import threading, SocketServer, BaseHTTPServer
quit_event = threading.Event()


import sys, os, json
import time
import urllib, urllib2, socket
import base64

import settings
import core
#import epg
import hls


buf = []
trd = [0]
twr = [0]
for b in range (100):
	buf.append(None)


try:
	import xbmcaddon
	addon = xbmcaddon.Addon(id='ptv3')
	root_dir = addon.getAddonInfo('path')
except:
	root_dir = os.getcwd()

#settings.set('port', 8185)
try: port = int(settings.get('port'))
except: 
	port = 8185
	settings.set('port', 8185)
if port=='': 
	port = 8185
	settings.set('port', 8185)

def mfind(t,s,e):
	r=t[t.find(s)+len(s):]
	r2=r[:r.find(e)]
	return r2

def get_ip():
	IP = settings.get('ip')
	if IP == '' or settings.get('ip_chek')!='false':
		if 'win' in sys.platform:
			try:
				L = socket.gethostbyname_ex(socket.gethostname())[2]
				for ip in L:
					if '192.168.' in ip: 
							IP = ip
							break

			except: IP = '127.0.0.1'
		else:
			try:
				Ln = ['eth0', 'eth1']
				for n in range(6):
					Ln.append('enp'+str(n)+'s0')
					Ln.append('wlp'+str(n)+'s0')
				for f in Ln:
					r = os.popen('ip addr show '+f).read()
					if 'inet ' in r:
						ip = mfind(r,'inet ','/')
						if '192.168.' in ip: 
							IP = ip
							break
			except: IP = '127.0.0.1'
		if '.' not in IP : IP = '127.0.0.1'
		settings.set('ip', IP)
	return IP


ip = get_ip()


print('----- Starting PTV3 0.11.3 -----')
print('HELP:     http://'+ip+':'+str(port))
print('PLAYLIST: http://'+ip+':'+str(port)+'/playlist')
trigger = True


# =========================== Базовые функции ================================
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

def utf(t):
	try:t=t.decode('windows-1251')
	except: pass
	try:t=t.decode(sys.getfilesystemencoding())
	except: pass
	try:t=t.encode('utf-8')
	except: pass
	return t

def win(t):
	try:t=t.decode('utf-8')
	except: pass
	try:t=t.decode(sys.getfilesystemencoding())
	except: pass
	try:t=t.encode('windows-1251')
	except: pass
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

def mfind(t,s,e):
	r=t[t.find(s)+len(s):]
	r2=r[:r.find(e)]
	return r2
	
def debug(s):
	fl = open(ru(os.path.join( addon.getAddonInfo('path'),"test.txt")), "w")
	fl.write(s)
	fl.close()



# ================================ server =====================================
set_list=[
	'id_port',
	'id_ip',
	'id_unlock',
	'id_split_1',
	'id_split_2',
	'id_split_3',
	'id_split_4',
	'id_serv21',]

tr_list=[
	'tr_unlock',
	'tr_multi',
	'tr_editor_form',
	'tr_ip_chek',
	'tr_addcnl',
	'tr_dl_logo',
	'tr_epg_on',
	'tr_epg_low',
	'tr_autoshift',
	'tr_upd14',
	'tr_upd15',
	'tr_upd16',
	'tr_upd17',
	'tr_upd18',
	'tr_upd19',
	'tr_upd21',
	'tr_upd22',
	'tr_upd31',
	'tr_upd34',
	'tr_upd35',
	'tr_upd36',
	'tr_upd37',
	'tr_upd38',
	'tr_upd52',
	'tr_upd53',
	'tr_upd81',
	'tr_upd82',
	'tr_upd83',
	'tr_upd84',
	'tr_epg_iptvx',
	'tr_epg_prtv',
	'tr_epg_vsetv_ua',
	'tr_epg_vsetv_by',
	'tr_epg_vsetv_ru',
	'tr_epg_yatv',
	'tr_epg_mail',
	'tr_epg_tviz',
	'tr_split_1',
	'tr_split_2',
	'tr_split_3',
	'tr_split_4',
	'tr_serv21',]

lb_list=[
	'lb_pr53',
	'lb_shift',
	]

upt_list=[
	'id_upt21',
	'id_upt22',
	'id_upt31',
	'id_upt32',
	'id_upt33',
	'id_upt34',
	'id_upt35',
	'id_upt36',
	'id_upt37',
	'id_upt38',
	'id_upt52',
	'id_upt53',
	'id_upt11',
	'id_upt12',
	'id_upt13',
	'id_upt14',
	'id_upt15',
	'id_upt16',
	'id_upt17',
	'id_upt18',
	'id_upt19',
	'id_upt10',
	'id_upt81',
	'id_upt82',
	'id_upt83',
	'id_upt84',
	'id_upt60',
	'id_upt9',
	'id_upt8',
	'id_upt7',
	'id_upt6',
	'id_upt1',
	'id_upt2',
	'id_upt3',
	'id_upt4',
	'id_upt5']

btn_list=['btn_upd53',]
ib_list=[
	'ib_port',
	'ib_ip',
	'ib_p2p_serv',
	'ib_scan_limit',
	'ib_mym3u1',
	'ib_mym3u2',
	'ib_mym3u3',
	'ib_mym3u4',
	'ib_myudp',
	]

for pid in range(99):
	sid=str(99-pid)
	lb_list.append ('lb_pr'+sid)
	tr_list.append ('tr_serv'+sid)
	tr_list.append ('tr_upd'+sid)
	set_list.append('id_serv'+sid)
	btn_list.append('btn_upd'+sid)

fl = open(os.path.join(root_dir,"webui.htm"), "r")
temp_ui=fl.read()
fl.close()

def splitter(ui):
	Ls=['split_1','split_2','split_3','split_4']
	for id in Ls:
		if settings.get(id) == 'false':
			ui=ui.replace('<!--s_'+id+'-->', '<!--')
			ui=ui.replace('<!--e_'+id+'-->', '-->')
	return ui

import controls
def WebUI():
		
		ui=temp_ui
		if settings.get('ip_chek')!='false': 
			get_ip()
			ui=ui.replace('ib_ip', 'id_ip')
		for i in set_list:
			id = i[3:]
			s = str(settings.get(id))
			if s=='true':  s = "<span style='color:green'>V</span>"
			if s=='false': s = "<span style='color:red'>X</span>"
			ui=ui.replace(i, s)
	
		for i in tr_list:
			id = i[3:]
			val = str(settings.get(id))
			s = controls.trigger('/settings/set/'+id+'/val/'+val)
			ui=ui.replace(i, s)
		
		for i in lb_list:
			id = i[3:]
			val = str(settings.get(id))
			s = controls.listbox('/settings/set/'+id+'/val/', ['','1','2','3','4','5'], val)
			ui=ui.replace(i, s)
		
		i='lb_p2p_proxy'
		id = i[3:]
		val = str(settings.get(id))
		s = controls.listbox('/settings/set/'+id+'/val/', ['HTTP_API','RESTREAMER','REDIRECT','AS_PROXY'], val, 120)
		ui=ui.replace(i, s)
		
		for i in ib_list:
			id = i[3:]
			val = str(settings.get(id))
			if 'mym3u' in i or 'myudp' in i : w = 200
			else:                             w = 110
			s = controls.input('/settings/set/'+id+'/val/', val, w)
			ui=ui.replace(i, s)
		
		for i in btn_list:
			id = i[7:]
			s = controls.button('/update/'+id)
			ui=ui.replace(i, s)
		
		for i in upt_list:
			id = i[6:]
			tm = core.get_cahe_time(id)
			tm = time.strftime('%H:%M %d.%m.%y',time.localtime(core.get_cahe_time(id)))
			#tm=
			ui=ui.replace(i, tm)
			
			s = str(settings.get('upd'+i[6:]))
			if s=='true': s = "<span style='color:green'>V</span>"
			if s=='false': s = "<span style='color:red'>X</span>"
			ui=ui.replace(i.replace('upt','up'), s)

		total=str(len(core.channels('all')))
		try:total=str(len(core.channels('all')))
		except: total='err'
		ui=ui.replace('id_total', total)
		ui = splitter(ui)
		return ui

def get_lock_cn(id):
		L=core.get_all_serv(id)
		for i in L:
			if i['lock']==False: return False
		return True

class cn_editor():
	def __init__(self):
		fl = open(os.path.join(root_dir,"webui.files", "cnl.htm"), "r")
		self.data = fl.read()
		fl.close()
		if settings.get('editor_form') != 'false': 
			self.data=self.data.replace('<!--form', '<form')
			self.data=self.data.replace('</p form-->', '</p>')
			self.data=self.data.replace('<!--/form-->', '</form>')
		self.Lepg=epg.get_channels_list()
		link_cnl = epg.link_cnl
		for i in link_cnl.keys():
				self.Lepg.append(link_cnl[i])
				self.Lepg.append(i)
		self.Larh=[]
		for i in archive.channels():
			self.Larh.append(i['cid'])
	
	def head(self):
		dt=self.data
		return dt[:dt.find('<!--items-->')]
	
	def list(self):
		L = core.get_base()
		return L
	
	def item(self, i):
			gr=''
			for g in i['group']:
				gr+=" | "+g
			gr=gr[3:]
			if i['enable']: option="[V]"
			else:           option="[X]"
			option+="[U]&nbsp;"
			if i['split']: option+="[S]&nbsp;"
			else:          option+="[Sp]&nbsp;"
			if i['enable']:option+="[I]"
			else:          option+="[Sp]"
			if i['id'] in self.Lepg: option+="&nbsp;[E]"
			else:                    option+="&nbsp;[SE]"
			if i['id'] in self.Larh: option+="&nbsp;[A]"
			else:                    option+="&nbsp;[AE]"

			#if get_lock_cn(i['id']): option+="&nbsp;[ ! ]"
			if settings.get('editor_form') != 'false': 
				itm = controls.item_f({'name':i['title'], 'cid':i['id'], 'group':gr, 'picon':i['picon'], 'option':option, 'enable':i['enable']})
			else:
				itm = controls.item({'name':i['title'], 'cid':i['id'], 'group':gr, 'picon':i['picon'], 'option':option, 'enable':i['enable']})
			return itm
	
	def end(self):
		dt=self.data
		return dt[dt.find('<!--items-->'):]

def editor():
		fl = open(os.path.join(root_dir,"webui.files", "cnl.htm"), "r")
		data = fl.read()
		fl.close()
		L = core.get_base()#get_DBC()#channels('all')
		items=''
		Lepg=epg.get_channels_list()
		for i in L:
			gr=''
			for g in i['group']:
				gr+=" | "+g
			gr=gr[3:]
			if i['enable']: option="[V]"
			else:           option="[X]"
			option+="[U]&nbsp;"
			if i['split']: option+="[S]&nbsp;"
			else:          option+="[Sp]&nbsp;"
			if i['enable']:option+="[I]"
			if i['id'] in Lepg: option+="&nbsp;[E]"
			itm = controls.item({'name':i['title'], 'cid':i['id'], 'group':gr, 'picon':i['picon'], 'option':option, 'enable':i['enable']})
			try:
				items+=itm
			except:
				print 'err item'
		
		return data.replace('<!--items-->',items) 

def set_epg():
		fl = open(os.path.join(root_dir,"webui.files", "epg.htm"), "r")
		ui = fl.read()
		fl.close()
		ui=ui.replace('[UPDATE]', controls.button('/epg/refresh'))
		utm=epg.get_inf_db('udata')
		if len(utm)>7: utms = utm[6:]+'-'+utm[4:6]+'-'+utm[:4]
		else: utms='--------'
		ui=ui.replace('UPTIME', utms)
		for i in tr_list:
			id = i[3:]
			val = str(settings.get(id))
			s = controls.trigger('/settings/set/'+id+'/val/'+val)
			ui=ui.replace(i, s)
		
		for i in lb_list:
			id = i[3:]
			val = str(settings.get(id))
			s = controls.listbox('/settings/set/'+id+'/val/', ["+11","+10","+9","+8","+7","+6","+5","+4","+3","+2","+1","0","-1","-2","-3","-4","-5","-6","-7","-8","-9","-10","-11"], val)
			ui=ui.replace(i, s)

		return ui

def link_epg(id1):
		fl = open(os.path.join(root_dir,"webui.files", "le.htm"), "r")
		data = fl.read()
		fl.close()
		try:    title=core.DBC[id1]['title']
		except: title=''
		data=data.replace('[TITLE]', title)
		
		items=''
		nm_dict=epg.get_nm_dict()
		L2=[]
		for nm in nm_dict.keys():
			title = nm.replace('<','[').replace('>',']').replace('&','&amp;')
			eid=nm_dict[nm]
			L2.append({'00':lower(title), 'title':title, 'id':eid})
		L2.sort()
		
		for i in L2:
			eid=i['id']
			title = i['title']
			if eid != id1 and title!='':
				if eid in core.picons.keys(): img = core.picons[eid]
				else:                         img = '\\webui.files\space.jpg'
				#img = 'http://td-soft.narod.ru/logo/picon/'+eid+'.png'
				itm = controls.item2("/epg/"+id1+"/set/"+eid, title, img)
				try:
					items+=itm
				except:
					print 'err item'
				
		
		data=data.replace('<!--items-->', items)
		
		return data

def link_arh(id1):
		fl = open(os.path.join(root_dir,"webui.files", "la.htm"), "r")
		data = fl.read()
		fl.close()
		try:    title=core.DBC[id1]['title']
		except: title=''
		data=data.replace('[TITLE]', title)
		L2=[]
		L=archive.channels()
		for i in L:
			i['00']=i['name']
			L2.append(i)
		L2.sort()
		items=''
		for i in L2:
			cid=i['cid']
			title = i['name']
			if cid != id1 and title!='':
				if cid in core.picons.keys(): img = core.picons[cid]
				else:                         img = '\\webui.files\space.jpg'
				
				itm = controls.item2("/archive/"+id1+"/set/"+cid, title, img)
				try:
					items+=itm
				except:
					print 'err item'
				
		data=data.replace('<!--items-->', items)
		
		return data

def select_picon(id):
		import picondb
		fl = open(os.path.join(root_dir,"webui.files", "lp.htm"), "r")
		data = fl.read()
		fl.close()
		try:title=core.DBC[id]['title']#win()
		except:title=''
		data=data.replace('[TITLE]', title)
		title=title.replace(' TV', '').replace(' ТВ', '').replace(' тв', '')
		L = picondb.get(title)
		items=''
		for img in L:
				itm = controls.item6("/picon/"+id+"/dl/"+base64.b64encode(img), img)
				try:    items+=itm
				except: print 'err item'
				
		data=data.replace('<!--items-->', items)
		
		return data
	


def info(id):
		fl = open(os.path.join(root_dir,"webui.files", "info.htm"), "r")
		data = fl.read()
		fl.close()
		inf=""
		inf = core.DBC[id]
		nml = inf['names']
		idl = []
		nms = ''
		for nm in nml:
			nms+=nm+"; "
			idl.append(core.get_ID(nm))
		data=data.replace('[ID]', id)
		data=data.replace('[NAME]', win(inf['title']))
		data=data.replace('[SPLIT]', win(nms))
		gr=''
		for g in core.get_cn_groups(id):
				gr+=" | "+g
		gr=gr[3:]
		data=data.replace('[GROUP]', win(gr))
		try:    picon = core.get_picon_dict()[id]
		except: picon = ''
		img = "<img border=0 width=120 height=120 src='"+picon+"'>"
		data=data.replace('[IMG]', img)
		LL=[]
		D=core.get_serv_dict()
		for s in D.keys():
			L=D[s]
			for i in L:
				if core.get_ID(i['title']) in idl:
				#if core.get_ID(i['title']) == id: 
					sid = i['url']
					if sid in core.BLs: lock = True
					else:               lock = False
					LL.append({'serv': s, 'url': i['url'], 'id':id, 'lock':lock, 'sid':sid})
		
		items=''
		for j in LL:
			itm = controls.item4(j)
			items+=itm
		
		data=data.replace('<!--items-->', win(items))
		return data

def channel_info(id):
		inf = core.DBC[id]
		gr=''
		for g in core.get_cn_groups(id):
				gr+=" | "+g
		gr=gr[3:]
		inf ['group'] = gr
		try:    picon = core.get_picon_dict()[id]
		except: picon = ''
		inf ['picon'] = picon
		
		return inf

def unite_gr(id1):
		fl = open(os.path.join(root_dir,"webui.files", "unite_gr.htm"), "r")
		data = fl.read()
		fl.close()
		
		items=''
		L=core.open_Groups()
		id2=0
		for i in L:
			if id2 == id1:
				data=data.replace('[TITLE]', i[0])
			else:
				img = '/webui.files/space.jpg'
				itm = controls.item2("/group/"+str(id1)+"/unite/"+str(id2), i[0], img)
				try:
					items+=itm
				except:
					print 'err item'
			id2+=1
		
		data=data.replace('<!--items-->', items)
		
		return data

def unite(id1):
		fl = open(os.path.join(root_dir,"webui.files", "unite.htm"), "r")
		data = fl.read()
		fl.close()
		
		items=''
		L=core.get_DBC()
		for i in L:
			if i['id'] == id1:
				data=data.replace('[TITLE]', i['title'])
			else:
				if i['id'] in core.picons.keys(): img = core.picons[i['id']]
				else:                             img = '\\webui.files\space.jpg'
				#img = 'http://td-soft.narod.ru/logo/picon/'+i['id']+'.png'
				itm = controls.item2("/channel/"+id1+"/unite/"+i['id'], i['title'], img)
				try:
					items+=itm
				except:
					print 'err item'
		
		data=data.replace('<!--items-->', items)
		
		return data

def add_to_group(gr):
		fl = open(os.path.join(root_dir,"webui.files", "add2gr.htm"), "r")
		data = fl.read()
		fl.close()
		data=data.replace('[TITLE]', gr)
		items=''
		L=core.get_DBC()
		for i in L:
				if i['id'] in core.picons.keys(): img = core.picons[i['id']]
				else:                             img = '\\webui.files\space.jpg'
				itm = controls.item2("/channel/"+i['id']+"/add_group/"+gr, i['title'], img)
				try:
					items+=itm
				except:
					print 'err item'
		
		data=data.replace('<!--items-->', items)
		
		return data

def split(id1):
		fl = open(os.path.join(root_dir,"webui.files", "split.htm"), "r")
		data = fl.read()
		fl.close()
		
		items=''
		i=core.DBC[id1]
		data=data.replace('[TITLE]', i['title'])
		L=i['names']
		for nm in L:
				img = '/webui.files/spl.jpg'
				itm = controls.item2("/channel/"+id1+"/split/"+nm, nm, img)
				try:
					items+=itm
				except:
					print 'err item'
		
		data=data.replace('<!--items-->', items)
		
		return data

def groups():
		fl = open(os.path.join(root_dir,"webui.files", "gr.htm"), "r")
		data = fl.read()
		fl.close()
		L=core.open_Groups()
		
		data=data.replace('[NEW]', controls.input('/group/add/', '', 250))
		items=''
		id=0
		for i in L:
			try: lock = i[2]
			except: lock = 'false'
			itm = controls.item3({'name':i[0], 'list':i[1], 'id': id, 'lock':lock})
			items+=itm
			id+=1
		return data.replace('<!--items-->',items) 


def group_editor(gr):
		fl = open(os.path.join(root_dir,"webui.files", "gr_cl.htm"), "r")
		data = fl.read()
		fl.close()

		L=core.open_Groups()
		Lg=[]
		for i in L:
			print i[0]
			print gr
			if i[0]==gr: Lg = i[1]
		
		data=data.replace('[GROUP]', gr)
		data=data.replace('[ADD]', controls.button('/add_to_group/'+gr))
		items=''
		n=0
		for id in Lg:
			try:    cnm = core.DBC[id]['title']
			except: cnm = id
			itm = controls.item7({'name':cnm, 'group':gr, 'id': id, 'n':n, 'total':len(Lg) })
			items+=itm
			n+=1
		return data.replace('<!--items-->',items) 

def serv_urls_off(id):
		
		Lserv=core.get_enable_serv()
		inf = core.DBC[id]
		nml = inf['names']
		idl = []
		nms = ''
		for nm in nml:
			nms+=nm+"; "
			idl.append(core.get_ID(nm))
		LL=[]
		D=core.get_serv_dict()
		for s in D.keys():
			enable_serv = False
			for sn in Lserv:
				sid=str(int(s[1:3]))
				pr = settings.get('pr'+sid)
				if sn in s: enable_serv = True
			L=D[s]
			for i in L:
				if core.get_ID(i['title']) in idl:
					uid = i['url']
					if uid in core.BLs: lock = True
					else:               lock = False
					
					LL.append({'serv': s, 'url': i['url'], 'id':id, 'lock':lock, 'serv_on': enable_serv, 'priority': pr})
		
		return LL


def get_params(params):
		if len(params)<4: return {}
		param=[]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
		return param

def edit_base(params_string):
	params=get_params(params_string)
	Lid = []
	for i in params.keys():
		id = i[3:]
		if id not in Lid: Lid.append(id)
		
	L = core.get_base()
	for i in L:
			gr=''
			for g in i['group']:
				gr+=" | "+g
			group=gr[3:]
			name=i['title']
			picon=i['picon']
			enable=i['enable']
			cid=i['id']
			
			bl = enable
			if 'on_'+cid in params.keys():
				if enable==False: 
					core.add_to_base(cid)
					bl=True
			else:
				if enable==True: 
					core.rem_from_base(cid)
					bl=False
			
			
			if cid in Lid and bl:
				if 'nm_'+cid in params.keys():
					val = urllib.unquote_plus(params['nm_'+cid])
					if name != val:
						core.rename_cnl(cid, val)
			
				if 'gr_'+cid in params.keys():
					val = urllib.unquote_plus(params['gr_'+cid])
					if group != val:
						core.set_group_cnl(cid, val)

def make_list(L):
	print '=== make_list ==='
	lst='#EXTM3U\n'
	for i in L:
		lst+='#EXTINF:1,\n'
		lst+=i+'\n'
	return lst

from threading import Thread
class MyThread(Thread):
	def __init__(self, param):
		Thread.__init__(self)
		self.BS = param['BS']
		self.n = param['n']
	
	def run(self):
		trd[0]=1
		dat = self.BS.get_data()
		if dat != None and dat!='error':
			buf[self.n]=dat
			trd[0]=0
		else:
			trd[0]=-1

def create_thread(param):
		my_thread = MyThread(param)
		my_thread.start()


class MyThread2(Thread):
	def __init__(self, param):
		Thread.__init__(self)
		self.wfile = param['wfile']
		self.n = param['n']
	
	def run(self):
		twr[0]=1
		#self.wfile.write(buf[self.n])
		try:
			self.wfile.write(buf[self.n])
			twr[0]=0
		except: 
			print 'err write'
			twr[0]=-1
			#self.wfile.write(buf[self.n])
		

def create_thread2(param):
		my_thread = MyThread2(param)
		my_thread.start()

class MyThread3(Thread):
	def __init__(self, param):
		Thread.__init__(self)
		self.param = param
	
	def run(self):
		exec(self.param)

def run_string(param):
		my_thread = MyThread3(param)
		my_thread.start()

CEPG={}
LGET=[]
LGET2=[]
LRE=[]
WFL=[None, None,0]
wfl=None
class HttpProcessor(BaseHTTPRequestHandler):
	def do_HEAD(self):
		pass
	
	def do_POST(self):
		print 'POST'
		print self.path
		self.data_string = self.rfile.read(int(self.headers['Content-Length']))
		#print self.data_string
		edit_base(self.data_string)
		self.send_response(302)
		self.send_header('Location', '/editor')
		self.end_headers()
	
	def do_GET(self):
		global vfl
		#print '=============='
		#print self.headers
		#print '=============='
		if 'Range:' in self.headers: data = '404 Not Found'
		else: data=get_on(self.path)
		try: head = data[:4]
		except: head = '    '
		#print head
		header=''
		
		if '|' in data and 'HLS' in data: 
			header = data.split('|')[1]
			data = data.split('|')[0].strip()
			#self.send_header(header.split('=')[0],header.split('=')[1])
			#print '====== header ======'
			#print data
			#print header.split('=')[0]
			#print header.split('=')[1]
			#print '===================='
		
		if len(head) < 2 and head!='/': head = '    '
		WFL[1]=0
		if head[:3]=='BS:':WFL[0]=self.wfile
		#if head[:3]=='ACE':WFL[0]=self.wfile
		if self.path in LGET: 
			WFL[0]=self.wfile
			if head[:3]=='BS:':
				WFL[0]=self.wfile
				WFL[1]=1
				head = 'RS:'
			
			if head[:3]=='MS2:':
				#vfl=self.wfile
				WFL[0]=self.wfile
				WFL[1]=1
				head = 'RS:'
		#else: LGET.append(self.path)
		if data == '404 Not Found':
			self.send_response(404)
		else:
			if head =='http' or head[0] =='/':
				#print '302'
				self.send_response(302)
				self.send_header('Location', data)
				self.send_header('content-type','image/jpeg')
			
			elif head =='udp:' or head =='rtmp':
				#print 'UDP/RTMP'
				self.send_response(200)
				self.send_header('content-type','application/vnd.apple.mpegurl')
				data='#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-STREAM-INF:PROGRAM-ID=1\n'+data
				
			elif 'JFIF' in data or 'IHDR' in data:
				#print 'IMG'
				self.send_response(200)
				self.send_header('content-type','image/jpeg')
			else:
				#print '200'
				self.send_response(200)
				if head[:3]=='BS:':   
					self.send_header('content-type','video/mp4')
				elif head[:3]=='HLS': 
					#if header!='': self.send_header(header.split('=')[0],header.split('=')[1])
					self.send_header('content-type','video/mp4')
				else:
					self.send_header('content-type','text/html')
				if False:
					self.send_header('Content-Encoding', 'gzip')
					import StringIO
					import gzip
					out = StringIO.StringIO()
					with gzip.GzipFile(fileobj=out, mode="w") as f:
						f.write(data)
					data=out.getvalue()
			
			
			
		self.end_headers()
		
		if head[:3]=='CLE':
			CLE = cn_editor()
			self.wfile.write(CLE.head())
			L  = CLE.list()
			for i in L:
				itm = CLE.item(i)
				self.wfile.write(itm)
			self.wfile.write(CLE.end())
		
		
		elif head[:3]=='XML':
			Lid=[]
			Lc = core.channels('all')#get_DBC()#core.get_base('true')
			for i in Lc:
				#if i['enable']: 
					Lid.append(i['id'])
			
			link = epg.link_cnl
			for i in link.keys():
					Lid.append(link[i])
					Lid.append(i)
			
			XTV=epg.xmltv()
			r = XTV.cnl_part(Lid)
			p1 = r[0]
			L  = r[1]
			self.wfile.write(p1)
			
			n=0
			for cid in L:
				n+=1
				#print str(n)+'/'+str(len(L))
				if cid in Lid:
					p2=XTV.prg_part(cid)
					self.wfile.write(p2)
			self.wfile.write(XTV.end_part())
		
		elif head[:3]=='RS:': 
			print '== RS =='
			#WFL[0]=self.wfile
			n = 0
			#c = WFL[2]
			s = 0
			#twr[0]=0
			#pt = time.time()
			
			while trigger:
				time.sleep(0.01)
				if twr[0]<1:
					s=0
					#if buf[c]!=None:
						
						#create_thread2({'wfile':WFL[0], 'n':c})
						#c+=1
						#if c>9: c=0
						
					#else:
					#	print 'buf None'
				else:
					s+=1
					if s>100: 
						print 'RS: stop'
						break
					#print 'twr[0]<1'
					
			#try:LRE.remove(WFL[0])
			#except: pass
			
		elif head[:3]=='ACE': 
			print '== ACE =='
			import p2p
			curl=data[4:]
			print curl
			ACE=p2p.P2P(curl)
			err=0
			while trigger:
					part=ACE.get_data()
					if part=='ERR': break
					elif part !=None:
						try:
							self.wfile.write(part)
							#time.sleep(0.0003)
							err=0
						except:
							break
					else: 
						err+=1
					if err>1000: break
			ACE.END()
		
		elif head[:3]=='BS:': 
			print '== BS =='
			import bitstream
			curl=data[3:]
			print curl
			BS=bitstream.BS(curl)
			bsn = 0
			bst = 0
			while trigger:
				try:
					part=BS.get_data()
					if part == 'error': break
					if part !=None: 
						self.wfile.write(part)
						bsn = 0
					else: 
						if bsn > 5: break
						if bst > 15: break
						print '== RECONNECT =='
						time.sleep(0.01)
						BS=bitstream.BS(curl)
						bsn+=1
						bst+=1
					
				except:
					break
			print '== BS END =='

		elif head[:3]=='BS2:' and self.path not in LGET: 
			print '== BS =='
			LGET.append(self.path)
			#WFL[0]=self.wfile
			import bitstream
			curl=data[3:]
			'''
			print BSL
			for strm in BSL:
				if BSL!=[] and '/ace/' in strm: 
					r=core.test_url(curl)
					if r!='404':
						curl=strm
					else:
						print '404'
						BSL.remove(strm)
						#LGET.remove(self.path)
						#self.send_response(404)
						#return
			'''
			BS=bitstream.BS(curl)
			b_part = None
			pn = 0
			#buf = []
			#tmp = BS.get_data()
			#buf[0]=tmp
			for b in range (10):
				buf[b]=None
			#for b in range (10):
			#	try:buf[b]=BS.get_data()
			#	except:pass
				
			f = 0
			n = 0
			tn= 0
			c = 0
			tc= 0
			c_old = 999
			s = 0
			twr[0]=0
			rec = 0
			infb=''
			ns=0
			pt = time.time()
			while trigger:
				if trd[0] == -1 :#or tn==100
					rec+=1
					
					if rec > 18:#or tn==100
						'''
						print '==== reconnect ===='
						print curl
						try:
							BS=bitstream.BS(curl)
							for b in range (10):
								try:dt=BS.get_data()
								except:dt=None
								
								if dt!=None:
									bc=b+c
									if bc>9:bc=bc-10
									buf[b]=dt
								else:
									print 'None'
						except:
							print 'ERR get BS'
						print '== reconnect end =='
						'''
						rec = 0
				else:
					rec = 0
				
				if twr[0]<1:
					if buf[c]!=None and tc<=tn :#and tn>5
						#if WFL[1]<1 : 
						create_thread2({'wfile':WFL[0], 'n':c})#self.wfile not in LRE
						if twr[0]==0:
							c2=c
							c+=1
							tc+=1
							if c>9: c=0
							#WFL[2]=c
						if twr[0]==-1:
							time.sleep(0.01)
							s+=1
							
				
				if trd[0]<1 and tn-tc<9:
						create_thread({'BS':BS, 'n':n})
						n+=1
						tn+=1
						f+=1
						if n>9: n = 0
				else:
					time.sleep(0.01)
				
				if c_old == c : s+=1#and buf[c]!=None
				else: s=0
				#if s>100 and tn<10: time.sleep(0.1)
				if s>250: 
					#serv.shutdown()
					print 'BS: stop'
					twr[0]=-1
					#self.send_response(404)
					LGET.remove(self.path)
					break
				c_old = c
				
				
				infa = "\n|"+str(tn)+"|"+str(tc)#+"|"+str(s)+'\n'#+self.path
				
				if infa!=infb: print infa
				infb=infa
		
		elif head[:3]=='HLS': 
			print '== HLS =='
			import hls
			curl=data[4:]
			print curl
			HLS=hls.HLS(curl, header)
			n=0
			er = 0
			er2= 0
			st = 0
			while trigger:
					n+=1
					print n
					part=HLS.get_data2()
					if part !=None: 
						self.wfile.write(part)
						er=0
						st=1
					else:
						if er>3 and st==0: break
						if er>1000: break
						er+=1
						time.sleep(0.5)
						part = 'None'
			print '== HLS END =='
		elif head[:3]=='MS:': 
			print '== MS =='
			BSL = eval(data[3:])
			#print BSL
			if BSL==[]: 
				self.send_response(404)
				return 
			
			curl=BSL[0]
			for strm in BSL:
				if BSL!=[] and '/ace/' in strm: 
					r=core.test_url(curl)
					if r!='404':
						curl=strm
					else:
						print '404'
						BSL.remove(strm)
			import bitstream
			import hls
			if '/ace/' in curl or '/udp/' in curl:  MS=bitstream.BS(curl)
			else: 									MS=hls.HLS(curl)
			b_part = None
			n=0
			ns=0
			while trigger:
					print n
					n+=1
					part=MS.get_data()
					if part == 'error': 
							print '==== reconnect ===='
							MS=hls.HLS(curl)
					if part !=None: self.wfile.write(part)
					else:
						n=0
						if '/ace/' in curl or '/udp/' in curl:  MS=bitstream.BS(curl)
						else: time.sleep(0.1)


		elif head[:3]=='MS2:': 
			print '== MS =='
			LGET.append(self.path)
			#WFL[0]=self.wfile
			
			BSL = eval(data[3:])
			print BSL
			if BSL==[]: 
				self.send_response(404)
				return 
			
			curl=BSL[0]
			for strm in BSL:
				if BSL!=[] and '/ace/' in strm: 
					r=core.test_url(curl)
					if r!='404':
						curl=strm
					else:
						print '404'
						BSL.remove(strm)
						#LGET.remove(self.path)
						#self.send_response(404)
						#return
			import bitstream
			import hls
			if '/ace/' in curl or '/udp/' in curl:  MS=bitstream.BS(curl)
			else: 									MS=hls.HLS(curl)
			b_part = None
			pn = 0
			#buf = []
			#tmp = BS.get_data()
			#buf[0]=tmp
			for b in range (10):
				buf[b]=None
			f = 0
			n = 0
			tn= 0
			c = 0
			tc= 0
			c_old = 999
			s = 0
			twr[0]=0
			rec = 0
			infb=''
			ns=0
			pt = time.time()
			while trigger:
				
				if trd[0] == -1 :#or tn==100
					rec+=1
					if rec>3: print 'rec:'+str(rec)
					if rec > 18:#or tn==100
						print '==== reconnect ===='
						print curl
						if len(BSL)>1:
							ns+=1
							if ns>=len(BSL):ns=0
							print ns
							curl=BSL[ns]
						print curl
						#for b in range (10):
						#	buf[b]=None
						try:
							if '/ace/' in curl or '/udp/' in curl:  MS=bitstream.BS(curl)
							else: 									MS=hls.HLS(curl)
							for b in range (10):
								try:dt=MS.get_data()
								except:dt=None
								
								if dt!=None:
									bc=b+c
									if bc>9:bc=bc-10
									buf[b]=dt
								else:
									print 'None'
						except:
							print 'ERR get MS'
						print '== reconnect end =='
						rec = 0
				else:
					rec = 0
				
				if twr[0]<1:
					if buf[c]!=None and tc<tn :#and tn>2
						#if WFL[1]<1 : 
							create_thread2({'wfile':WFL[0], 'n':c})#self.wfile not in LRE
							c2=c
							c+=1
							tc+=1
							if c>9: c=0
							WFL[2]=c
				
				if trd[0]<1 and tn-tc<8:#
						create_thread({'BS':MS, 'n':n})
						n+=1
						tn+=1
						f+=1
						if n>9: n = 0
				else:
					time.sleep(0.01)
				
				if c_old == c : s+=1#and buf[c]!=None
				else: s=0
				if s>180: 
					print 'MS: stop'
					twr[0]=-1
					WFL[0]=None
					#LGET.remove(self.path)
					break
				c_old = c
				
				
				infa = "\n|"#+str(tn)+"|"+str(tc)+"|"+str(s)+'\n'#+self.path
				time.sleep(0.01)
				if infa!=infb: print infa
				infb=infa
						
						
		else:
			self.wfile.write(data)
		#quit_event.set()
		
		try:LGET.remove(self.path)
		except: pass

class MyThreadingHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
	pass

serv = MyThreadingHTTPServer(("0.0.0.0",port), HttpProcessor)
threading.Thread(target=serv.serve_forever).start()



#===================================================================
fch={}
#BSL=[]
def get_on(addres):
		print addres
		global trigger
		addres=utf(addres)
		if '/nofollow' in addres: 
			nofollow=True
			addres=addres.replace('/nofollow', '')
		else:                     
			nofollow=False
		data='404 Not Found'
		if addres == "/":
			data = WebUI()#help
		elif "/webui.files/" in addres:
			nmf=addres[13:]
			nmf=addres[addres.rfind('webui.files/')+12:]
			if nmf in fch.keys():
				data = fch[nmf]
			else:
				fl = open(os.path.join(root_dir,"webui.files", nmf), "rb")#
				data = fl.read()
				fl.close()
				fch[nmf]=data
		
		elif "/logo/" in addres:
			nmf=addres[addres.rfind("/logo/")+6:]
			#print nmf
			if nmf in fch.keys():
				data = fch[nmf]
			else:
				fl = open(os.path.join(root_dir,"logo", nmf), "rb")
				data = fl.read()
				fl.close()
				fch[nmf]=data
		
		elif "/picon/" in addres:
			if "/get/" in addres:
				cid=addres[addres.rfind('/')+1:]
				data=select_picon(cid)
			if "/dl/" in addres:
				cid = mfind(addres, '/picon/','/')
				bu=addres[addres.find('/dl/')+4:]
				print bu
				try:purl=base64.b64decode(bu)
				except:purl=''
				#print purl
				if purl!='': core.GETimg(purl, cid, True)
				data='/editor#'+cid
		
		elif "/info/" in addres:
			id=addres[addres.find('/info/')+6:]
			if '#' in addres:
				sid=mfind(addres, '#', '/')
				if '/lock'   in addres: core.add_BLs(sid)
				if '/unlock' in addres: core.rem_BLs(sid)
			data = '/groups'
			
			data = info(id)
		
		elif '/settings/' in addres:
			if '/get/' in addres:
				key=addres[addres.find('/get/')+5:]
				data=settings.get(key)
			elif '/set/' in addres:
				key=addres[addres.find('/set/')+5:addres.find('/val/')]
				if 'val=' in addres:
					val=urllib.unquote_plus(addres[addres.find('val=')+4:])
				else:
					val=urllib.unquote_plus(addres[addres.find('/val/')+5:])
				data=settings.set(key, val)
				if 'editor_' in addres: data='/editor'#data='http://'+get_ip()+':'+str(port)+'/editor'
				elif 'epg_' in addres: data='/epg'
				#elif 'epgon' in addres: data='/epg'
				else:                       data='/'#data='http://'+get_ip()+':'+str(port)
		elif "/gr_edit/" in addres:
			gr = urllib.unquote_plus(addres[addres.find('gr_edit/')+8:])
			data=group_editor(gr)
		elif "/add_to_group/" in addres:
			gr = urllib.unquote_plus(addres[addres.find('group/')+6:])
			data=add_to_group(gr)
		elif "/editor" in addres:
			if '/editor?' in addres:
				prm=edit_base(addres[addres.find('/editor?')+8:])
				data = '/editor'
			else: 
				prm=''
				data = 'CLE:'#editor()
		elif '/serv/stop' in addres: 
			trigger = False
			data = 'stop'
		elif '/groups' in addres:
			if '/groups/' in addres:
				if '/groups/list' in addres: data = core.groups()
				if '/groups/dict' in addres: data = core.open_Groups()
				if '/groups/json' in addres: data = json.dumps(core.open_Groups())
			else:
				data = groups()
		
		elif '/group/' in addres:
			try:
				id = int(mfind(addres, '/group/','/'))
				gr = core.open_Groups()[id][0]
			except:
				id = ''
				gr = ''
			if '/add/' in addres: 
				if 'val=' in addres: gnm =addres[addres.find('val=')+4:]
				else:                gnm =addres[addres.find('add/')+4:]
				core.add_gr(utf(urllib.unquote_plus(gnm)))
				
			if '/del/' in addres: 
				if 'val=' in addres: gnm =addres[addres.find('val=')+4:]
				else:                gnm =addres[addres.find('del/')+4:]
				core.rem_gr(utf(urllib.unquote_plus(gnm)))
			
			if '/lock'    in addres: core.lock_gr(id, 'true')
			if '/unlock'  in addres: core.lock_gr(id, 'false')
			if '/rem'     in addres: core.rem_gr(gr)
			if '/up'      in addres: core.move_gr(id, id-1)
			if '/down'    in addres: core.move_gr(id, id+1)
			if '/rename'  in addres: 
				if 'val=' in addres: gnm =addres[addres.find('val=')+4:]
				else:                gnm =addres[addres.find('/rename/')+8:]
				core.rename_gr(id, utf(urllib.unquote_plus(gnm)))
			data='/groups'
			if '/list'    in addres: 
				gr  = urllib.unquote_plus(mfind(addres, '/group/','/'))
				data = core.group_list(gr)
			
			if '/unite' in addres:
				if '/unite/' in addres:
					id2 = int(addres[addres.find('/unite/')+7:])
					core.unite_gr(id, id2)
				else:
					data=unite_gr(id)
			if '/set_cn/' in addres:
				gr  = urllib.unquote_plus(mfind(addres, '/group/','/'))
				cid = mfind(addres, '/set_cn/','/')
				num = int(addres[addres.rfind('/')+1:])
				core.set_num_cn(gr, cid, num)
				data='/gr_edit/'+gr
		
		elif '/channels/' in addres:
			if '/dict' in addres:
				gr = 'all'
				if '/dict/' in addres: gr = urllib.unquote_plus(addres[addres.find('/dict/')+6:])
				data = core.channels(gr)
			elif '/json' in addres:
				data = core.jsonlist()
			elif '/tvh' in addres:
				data = core.tvhlist()
			elif '/list' in addres or '/playlist' in addres:
				if 'list/' in addres:  id=addres[addres.find('list/')+5:]
				else: 						id = ''
				if id == '': data = core.playlist()
				else:        data = core.playlist(id)
		
		elif '/playlist' in addres:
				if '/make/' in addres:
						print '===== make ======'
						id=addres[addres.find('/make/')+6:]
						try:    streams = eval(base64.b64decode(id))
						except: streams = []
						print streams
						data = make_list(streams)
						print data
				
				elif 'list/' in addres:
						id=addres[addres.find('list/')+5:]
						data = core.playlist(id)
				else: 	data = core.playlist()
		
		elif '/channel/' in addres:
			id1 = mfind(addres, '/channel/','/')
			if '/data' in addres: data=core.DBC[id1]
			elif '/set_group/' in addres: 
											if 'val=' in addres: gs =addres[addres.find('val=')+4:]
											else:                gs =addres[addres.find('/set_group/')+11:]
											core.set_group_cnl(id1, urllib.unquote_plus(gs))
			elif '/add_group/' in addres: 
											if 'val=' in addres: gs =addres[addres.find('val=')+4:]
											else:                gs =addres[addres.find('/add_group/')+11:]
											core.add_to_gr(id1, urllib.unquote_plus(gs))
			elif '/rem_group/' in addres: 
											if 'val=' in addres: gs =addres[addres.find('val=')+4:]
											else:                gs =addres[addres.find('/rem_group/')+11:]
											core.rem_from_gr(id1, urllib.unquote_plus(gs))
			
			elif '/add'    in addres: 			core.add_to_base(id1)
			elif '/rem'    in addres: 			core.rem_from_base(id1)
			elif '/rename' in addres: 
				if 'val='  in addres: cnm =addres[addres.find('val=')+4:]
				else:                cnm =addres[addres.find('rename/')+7:]
				core.rename_cnl(id1, urllib.unquote_plus(cnm))
				
			if '/rem_group/' in addres: data='/gr_edit/'+addres[addres.find('/rem_group/')+11:]
			elif '/add_group/' in addres: data='/gr_edit/'+addres[addres.find('/add_group/')+11:]
			else: data='/editor#'+id1
			
			if '/inf'   in addres: 
					data=channel_info(id1)#core.DBC[id1]
			
			if '/unite' in addres:
				if '/unite/' in addres:
					id2 = addres[addres.find('/unite/')+7:]
					if '#' in id2: id2=id2[:id2.rfind('#')]
					#print id1
					#print id2
					core.unite_cnl(id1, id2)
					data='/editor#'+id2
				else:
					data=unite(id1)
			
			if '/split' in addres: 
				if '/split/' in addres:
					nm = urllib.unquote_plus(addres[addres.find('/split/')+7:])
					core.split_cnl(id1, nm)
				else:
					data=split(id1)
		
		elif '/acestream/' in addres:
			id=addres[addres.find('stream/')+7:]
			redir=''
			prx = settings.get("p2p_proxy")
			if prx == 'RESTREAMER':
				redir='ACE:'+id
			elif prx == 'REDIRECT':
				import p2p
				redir=p2p.START(id)
			
			if redir=='': data="404 Not Found"
			else:         data=redir

		elif '/stream/' in addres:
			id=addres[addres.find('stream/')+7:]
			redir=core.stream(id)
			if redir=='': data="404 Not Found"
			else:         data=redir
			
		elif '/restream/' in addres:
			print '########## RESTREAM ############'
			#for i in BSL:
			#	BSL.remove(i)
			id=addres[addres.find('restream/')+9:]
			#print id
			if len(id)>8:
				try:    stream = base64.b64decode(id)
				except: stream = ''
			else: 
						stream=core.stream(id)
			print stream
			if stream !='':
				if '/restream/' in stream:   data=stream
				elif '/ace/'   in stream:    data='BS:' +stream
				elif '/udp/' in stream:      data='BS:' +stream
				else:                        data='HLS:'+stream
				print data
			else:
				data='404 Not Found'
		elif '/restreams/' in addres:
			id=addres[addres.find('restreams/')+10:]
			streams=core.streams(id)
			#for i in BSL:
			#	BSL.remove(i)
			#for stream in streams:
			#	if stream !='':
			#			BSL.append(stream)
			data='MS:' +repr(core.streams(id))
			
			print data
					#else:
						
						#BSL.append(stream)
						#data='MS:' +BSL[0]
						#stream = 'http://'+ip+':'+str(port)+'/restream/'+base64.b64encode(stream)


		elif '/streams/' in addres:
			if '/streams/json_ds' in addres:
				id=addres[addres.find('json_ds/')+8:]
				data = json.dumps(core.streams_ds(id))
				#data=core.json_streams(id)
			elif '/streams/json' in addres:
				id=addres[addres.find('json/')+5:]
				data = json.dumps(core.streams(id))
			elif '/streams/list' in addres:
				id=addres[addres.find('list/')+5:]
				data=core.streams(id)
			else:
				id=addres[addres.find('streams/')+8:]
				data=core.sublist(id)
		elif '/update/' in addres:
			id=addres[addres.find('/update/')+8:]
			core.upd_canals_by_id(id)
			data='/'#'http://'+get_ip()+':'+str(port)
		elif '/back_list/' in addres:
			#sid=base64.b64decode(mfind(addres, '/back_list/', '/'))
			if '/lock'   in addres: bu=addres[addres.find('/back_list/')+11: addres.rfind('/lock')]
			if '/unlock' in addres: bu=addres[addres.find('/back_list/')+11: addres.rfind('/unlock')]
			try:sid=base64.b64decode(bu)
			except:sid=''
			if '/lock'   in addres: core.add_BLs(sid)
			if '/unlock' in addres: core.rem_BLs(sid)
			
			if '/json'   in addres: data = json.dumps({'back_list':'ok'})
			elif 'lock/' in addres: data = '/info/'+addres[addres.find('lock/')+5:]
			else: data = '/'
			
		elif '/black_list/' in addres:
			#sid=base64.b64decode(mfind(addres, '/back_list/', '/'))
			if '/lock'   in addres: bu=addres[addres.find('/black_list/')+12: addres.rfind('/lock')]
			if '/unlock' in addres: bu=addres[addres.find('/black_list/')+12: addres.rfind('/unlock')]
			try:sid=base64.b64decode(bu)
			except:sid=''
			if '/lock'   in addres: core.add_BLs(sid)
			if '/unlock' in addres: core.rem_BLs(sid)
			
			if '/json'   in addres: data = json.dumps({'black_list':'ok'})
			elif 'lock/' in addres: data = '/info/'+addres[addres.find('lock/')+5:]
			else: data = '/'
			
		elif '/epg' in addres:
			if '/epg/' in addres:
				if  '/refresh' in addres:
					data="epg refresh"
					epg.upepg()
				
				if  '/data' in addres:
					try:	data = epg.get_inf_db('udata')
					except: data = '0'
				
				if  '/dict' in addres:
					data=repr(epg.EPG)
				
				if  '/json' in addres:
					data=json.dumps(epg.EPG)
				
				if  '/xmltv' in addres:
					data='XMLTV'
					#epg.xmltv()
					#import StringIO
					#import gzip
					#out = StringIO.StringIO()
					#with gzip.GzipFile(fileobj=out, mode="w") as f:
					#	f.write(data)
					#data=out.getvalue()
				
				if '/current' in addres:
					if '/p=' in addres: 
						p=addres[addres.find('/p=')+3:]
						data=repr(epg.get_current_epg(p))
					else: 
						data=repr(epg.get_all_current_epg())

				if  '/id_list' in addres:
					data=repr(epg.get_channels_list())
				
				if  '/id_dict' in addres:
					data=repr(epg.get_nm_dict())
				
				if  '/id_json' in addres:
					data=json.dumps(epg.get_nm_dict())
				
				if  '/inf/' in addres:
					try:
						cid=addres[addres.rfind('/')+1:]
						if len(cid)>4:	data=repr(epg.get_channels_info(cid))
						else: 				data="id:"+'None'
					except:
						print "ERR EPG "+addres
						data="ERR 404"
				if  '/set_' in addres:
					cid=addres[addres.rfind('/')+1:]
					if '#' in cid: cid=cid[:cid.rfind('#')]
					data=link_epg(cid)
				if  '/set/' in addres:
					id2 = mfind(addres, '/epg/','/')
					id1 = addres[addres.find('/set/')+5:]
					epg.change_id(id2, id1)
					data='/editor#'+id2
				
			elif 'epg_' not in addres: data=set_epg()
			else: data='/epg'
		
		elif '/y_img/' in addres or 's-tv.ru' in addres or 'tv.mail.ru' in addres or '/tviz/' in addres:
			data=epg.get_img(addres)
		
		elif '/cache_url/' in addres:
			cid=mfind(addres, '/cache_url/', '/')
			if '/list' in addres: data=core.get_all_serv(cid)#serv_urls(cid)
			if '/json' in addres: data=json.dumps(core.get_all_serv(cid))#serv_urls(cid)
		
		elif '/ratio/' in addres:
			bu=addres[addres.find('/ratio/')+7: addres.rfind('/')]
			try:sid=base64.b64decode(bu)
			except:sid=''
			if sid!='':
				if '/good'   in addres: core.set_rating(sid, 'good')
				if '/bad'    in addres: core.set_rating(sid, 'bad')
				if '/get'    in addres: data = core.get_rating(sid)
				elif '/json' in addres: data = json.dumps(core.get_rating(sid))
				else: data='ratio ok'
			else:
				data='error base64'
		
		elif '/archive/' in addres:
			if   '/dict' in addres:
				data = archive.get_all_archive()
			elif '/list' in addres:
				data = archive.channels()
			elif '/id/'  in addres:
				if '/day/' in addres:
					id=mfind(addres, '/id/', '/')
					day = addres[addres.find('/day/')+5:]
					data = archive.archive_by_id(id, day)
				else:
					id = addres[addres.find('/id/')+4:]
					data = archive.archive_by_id(id)
			elif '/cid/' in addres:
				if '/day/' in addres:
					id=mfind(addres, '/cid/', '/')
					day = addres[addres.find('/day/')+5:]
					data = archive.archive_by_cid(id, day)
				else:
					id = addres[addres.find('/cid/')+5:]
					data = archive.archive_by_cid(id)
			elif '/record/'  in addres:
				id = urllib.unquote_plus(addres[addres.find('/record/')+8:])
				stream = archive.stream_by_id(id)
				#stream = 'http://178.162.205.76/video/6pCercjxnWetAPhq8rLreA/3/playlist-1559257200-11100.m3u8'
				data = stream
			elif '/records/' in addres:
				id = urllib.unquote_plus(addres[addres.find('/records/')+9:])
				data= archive.streams_by_id(id)
				
			elif '/set_' in addres:
				cid=addres[addres.rfind('/')+1:]
				if '#' in cid: cid=cid[:cid.rfind('#')]
				data=link_arh(cid)
			elif '/set/' in addres:
				id2 = mfind(addres, '/archive/','/')
				id1 = addres[addres.find('/set/')+5:]
				archive.change_id(id2, id1)
				data='/editor#'+id2
			if '/json' in addres: data=json.dumps(data)

		if nofollow and data!='404 Not Found': data='200 OK'
		return data

#===================================================================

def abortRequested():
	try: 
		import xbmc
		try:    r=xbmc.Monitor().abortRequested()
		except: r=xbmc.abortRequested
	except:
		r=False
	return r

print('----- PTV3_serv OK -----')
import archive
import epg

ntr = 0
while trigger:
		if abortRequested(): break
		if ntr==0:
			core.refresh_cnl()
			
			try:	udata = int(epg.get_inf_db('udata'))
			except: udata = 0
			cdata = int(time.strftime('%Y%m%d'))
			#print('----- EPG ud:'+str(udata))
			if cdata>udata and settings.get("epg_on")!='false':
						print('----- EPG update -----')
						epg.upepg()
						#run_string('epg.upepg()')
			
		ntr+=1
		if ntr>10: ntr = 0
		time.sleep(6)

try:serv.shutdown()
except:pass

print('----- PTV3_serv stopped -----')

