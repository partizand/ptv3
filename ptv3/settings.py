# -*- coding: utf-8 -*-
import os


# Singleton
class Settings:
	__instance = None

	def __init__(self):
		self.isKodi = False
		try:
			import xbmcaddon, xbmc
			self.isKodi = True
		except ImportError:
			self.isKodi = False

		if self.isKodi:
			import xbmcaddon, xbmc
			addon = xbmcaddon.Addon(id='ptv3')
			addonptv = xbmcaddon.Addon(id='ptv3')
			addonptv.setSetting("ptv", '3')
			# db_dir = os.path.join(addon.getAddonInfo('path'),"settings")
			# self.db_dir = os.path.join(xbmc.translatePath("special://masterprofile/"), "addon_data", "ptv3")


			self.serv_dir = os.path.join(addon.getAddonInfo('path'), "serv")
			self.serv_py = self.serv_dir
			self.arh_serv_dir = os.path.join(addon.getAddonInfo('path'), "arh")
			self.picon_dir = os.path.join(addon.getAddonInfo('path'), 'logo')
			# UserDir = os.path.join(addon.getAddonInfo('path'), "user" )

			self.UserDir = os.path.join(xbmc.translatePath("special://masterprofile/"), "addon_data", "ptv3")
			self.root_dir = addon.getAddonInfo('path')
			self.monitor = xbmc.Monitor()
		else:
			self.root_dir = os.path.dirname(os.path.realpath(__file__))  # script dir
			self.monitor = None
			# self.db_dir = os.path.expanduser("~/.config/pazzltv3/settings")
			# if not os.path.exists(self.db_dir):
			# 	os.makedirs(self.db_dir)
			self.serv_dir = os.path.expanduser("~/.local/share/pazzltv3/serv")
			self.arh_serv_dir = os.path.join(os.getcwd(), "arh")
			self.picon_dir = os.path.expanduser("~/.local/share/pazzltv3/logo")
			self.UserDir = os.path.expanduser("~/.config/pazzltv3/settings")
			self.serv_py = os.path.join(os.getcwd(), "serv")
			if not os.path.exists(self.UserDir):
				os.makedirs(self.UserDir)

			if not os.path.exists(self.serv_dir):
				os.makedirs(self.serv_dir)

			if not os.path.exists(self.picon_dir):
				os.makedirs(self.picon_dir)

	def set(self, key, val):
		try:
			fp = os.path.join(self.UserDir, key)
			fl = open(fp, "w")
			fl.write(repr(val))
			fl.close()
			return 'ok'
		except:
			return 'error set ' + key

	def get(self, key):
		try:
			fp = os.path.join(self.UserDir, key)
			fl = open(fp, "r")
			t = fl.read()
			fl.close()
			return eval(t)
		except:
			val = self.default(key)
			if val != '': self.set(key, val)
			return val

	def default(self, key):
		try:
			if key == 'serv5':
				return 'true'
			elif 'p2p_serv' in key:
				return '127.0.0.1'
			elif 'serv' in key:
				return 'false'
			if 'upd3' in key and key != 'upd3': return 'true'
			if 'upd8' == key:
				return ''
			elif 'upd8' in key:
				return 'true'
			if 'epg_' in key:   return 'false'
			D = {
				'ip': '127.0.0.1',
				'p2p_proxy': 'HTTP_API',
				'ip_chek': 'true',
				'epg_on': 'true',
				'editor_form': 'true',
				'tr_dl_logo': 'false',
				'autoshift': 'true',
				'shift': '0',
				'port': 8185,
				'split_1': 'true',
				'split_2': 'false',
				'split_3': 'false',
				'split_4': 'false',
				'unlock': 'true',
				'addcnl': 'false',
				'multi': 'true',
				'upd21': 'true',
				'upd52': 'true',
				'upd53': 'true',
				'upd60': 'true',
			}
			if key in D.keys(): return D[key]
			return ''
		except:
			return ''

	@classmethod
	def getInstance(cls):
		if not cls.__instance:
			cls.__instance = Settings()
		return cls.__instance



