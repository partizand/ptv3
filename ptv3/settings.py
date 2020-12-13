# -*- coding: utf-8 -*-
import os
try:
	import xbmcaddon, xbmc
	addon = xbmcaddon.Addon(id='ptv3')
	set=xbmcaddon.Addon(id='ptv3')
	set.setSetting("ptv",'3')
	#db_dir = os.path.join(addon.getAddonInfo('path'),"settings")
	db_dir = os.path.join(xbmc.translatePath("special://masterprofile/"),"addon_data","ptv3")
except:
	db_dir = os.path.join(os.getcwd(), "settings" )

def set(key, val):
	try:
		fp=os.path.join(db_dir, key)
		fl = open(fp, "w")
		fl.write(repr(val))
		fl.close()
		return 'ok'
	except:
		return 'error set '+key

def get(key):
	try:
		fp=os.path.join(db_dir, key)
		fl = open(fp, "r")
		t=fl.read()
		fl.close()
		return eval(t)
	except:
		val=default(key)
		if val!='': set(key, val)
		return val

def default(key):
	try:
		if key == 'serv5':      return 'true'
		elif 'p2p_serv' in key: return '127.0.0.1'
		elif 'scan_limit' in key: return '20'
		elif 'serv' in key:     return 'false'
		elif 'restream_list' in key:   return 'zabava, vrzh-htlive, yandex, ucom.am, peers.tv, /udp/'
		elif key == 'restreamer': return 'true'
		if 'upd3' in key and key!='upd3' : return 'true'
		if 'upd8' == key :      return ''
		elif 'upd8' in key :      return 'true'
		if 'epg_' in key :   return 'false'
		D={
		'ip':			'127.0.0.1',
		'p2p_proxy':	'HTTP_API',
		'ip_chek':		'true',
		'epg_on':		'true',
		'editor_form':	'true',
		'tr_dl_logo':	'false',
		'autoshift':	'true',
		'shift':		'0',
		'port' :		8185,
		'split_1':		'true',
		'split_2':		'false',
		'split_3':		'false',
		'split_4':		'false',
		'unlock' :		'true',
		'addcnl' :		'false',
		'multi':		'true',
		'upd21':		'true',
		'upd52':		'true',
		'upd53':		'true',
		'upd60':		'true',
		}
		if key in D.keys(): return D[key]
		return ''
	except:
		return ''

#print set('KEY', 'VALUE')
#print get('KEY')
