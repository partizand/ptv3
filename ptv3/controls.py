# -*- coding: utf-8 -*-
import base64
def trigger(link):
	F='<a href="LINK"><img border=0 width=37 height=19 src="webui.files/off.jpg"></a>'
	T='<a href="LINK"><img border=0 width=37 height=19 src="webui.files/on.jpg"></a>'
	N='<a href="LINK"><img border=0 width=37 height=19 src="webui.files/def.jpg"></a>'

	if 'val/true' in link:
		return T.replace('LINK', link.replace('true','false'))
	elif 'val/false' in link:
		return F.replace('LINK', link.replace('false','true'))
	else:
		return N.replace('LINK', link[:link.rfind('/')+1]+'true')


def on_off(link):
	F='<a href="LINK"><img border=0 width=37 height=19 src="webui.files/off.jpg"></a>'
	T='<a href="LINK"><img border=0 width=37 height=19 src="webui.files/on.jpg"></a>'
	N='<a href="LINK"><img border=0 width=37 height=19 src="webui.files/def.jpg"></a>'
	
	if '/rem' in link:
		return T.replace('LINK', link)
	elif '/add' in link:
		return F.replace('LINK', link)

def lock_btn(link):
	L='<a href="LINK"><img border=0 width=37 height=19 src="/webui.files/lock2.jpg"></a>'
	U='<a href="LINK"><img border=0 width=37 height=19 src="/webui.files/unlock2.jpg"></a>'
	
	if '/lock' in link:
		return U.replace('LINK', link)
	elif '/unlock' in link:
		return L.replace('LINK', link)

def button (link):
	ico = ''
	if '/update/' in link: ico = 'ref'
	elif '/refresh' in link: ico = 'ref'
	elif '/unite' in link: ico = 'unt'
	elif '/split' in link: ico = 'spl'
	elif '/up'    in link: ico = 'up'
	elif '/icu'   in link: ico = 'up'
	elif '/down'  in link: ico = 'down'
	elif '/icd'   in link: ico = 'down'
	elif '/rem'   in link: ico = 'rem'
	elif '/lock'  in link: ico = 'lock'
	elif '/unlock'in link: ico = 'unlk'
	elif '/info'  in link: ico = 'inf'
	elif '/set_b' in link: ico = 'bepg'
	elif '/set_s' in link: ico = 'sepg'
	elif '/set_aa' in link: ico = 'ara'
	elif '/set_ab' in link: ico = 'arb'
	elif '/icb'   in link: ico = 'icb'
	elif '/ice'   in link: ico = 'ice'
	elif '/gr_ed' in link: ico = 'lgc'
	elif '/add_'  in link: ico = 'add'
	B = '<a href="LINK"><img border=0 width=19 height=19 src="webui.files/'+ico+'.jpg"></a>'
	return B.replace('LINK', link)

def button2 (link):
	ico = ''
	if '/update/' in link: ico = 'ref'
	elif '/unite' in link: ico = 'unt'
	elif '/split' in link: ico = 'spl'
	elif '/up'    in link: ico = 'up'
	elif '/down'  in link: ico = 'down'
	elif '/rem'   in link: ico = 'rem'
	elif '/lock'  in link: ico = 'lock'
	elif '/unlock'in link: ico = 'unlk'
	elif '/info'  in link: ico = 'inf'
	B=' <form><input type="hidden" name="val" value="'+link+'"><button>'+ico+'</button></form>'
	return B.replace('LINK', link)


def item(param):#&nbsp;<img border=0 width=20 height=19 src='[IMG]'>&nbsp;
	it=" <tr style='border:solid black 1.0pt;'>\
	  <td>&nbsp;[IMG]</td>\
	  <td>[NAME]</td>\
	  <td>[ON]</td>\
	  <td>&nbsp;&nbsp;&nbsp;[OPTION]</td>\
	  <td>[GROUP]</td>\
	  <td><a name='[CID]'>&nbsp;[CID]</a></td>\
	 </tr>"
	
	gr     = param['group']
	cid    = param['cid']
	option = param['option']
	name   = param['name']
	enable = param['enable']
	img    = param['picon']
	BIMG   = '<a href="/picon/get/'+cid+'"><img border=0 width=19 height=19 src="'+img+'"></a>'
	
	#spc  ='<a><img border=0 width=19 height=19 src="webui.files/space.jpg"></a>'
	#on =  f_on_off2('on_'+cid, 'false')#
	on = on_off('/channel/'+cid+'/rem')
	#off = f_on_off2('on_'+cid, 'true')#
	off = on_off('/channel/'+cid+'/add')
	unt = button ('/channel/'+cid+'/unite'+"#"+name[:2])
	spl = button ('/channel/'+cid+'/split')
	inf = button ('/info/'+cid)
	bepg= button ('/epg/set_b/'+cid+"#"+name[:2])
	sepg= button ('/epg/set_s/'+cid+"#"+name[:2])
	aarh= button ('/archive/set_aa/'+cid+"#"+name[:2])
	barh= button ('/archive/set_ab/'+cid+"#"+name[:2])

	if '[V]' in option: 
		#onoff = f_on_off2('on_'+cid, 'false')
		onoff = on
	else:
		#onoff = f_on_off2('on_'+cid, 'true')
		onoff = off
	
	option = option.replace('[U]', unt).replace('[S]', spl).replace('[I]', inf).replace('[V]', '').replace('[X]', '').replace('[E]', bepg).replace('[SE]', sepg).replace('[A]', aarh).replace('[AE]', barh).replace('[Sp]', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')+'&nbsp;&nbsp;'
	
	
	it=it.replace('[NAME]',   input('/channel/'+cid+'/rename/', name, 200, enable))
	#it=it.replace('[NAME]',   f_text('nm_'+cid, name, 200, enable))
	it=it.replace('[CID]',    cid )
	it=it.replace('[ON]', onoff)
	it=it.replace('[OPTION]', option)
	#it=it.replace('[GROUP]',  f_text('gr_'+cid, gr, 200, enable))
	it=it.replace('[GROUP]',   input('/channel/'+cid+'/set_group/', gr, 200, enable))
	try:it=it.replace('[IMG]', BIMG)#img
	except:pass
	#try:it=it.decode('utf-8')
	#except: pass
	#try:it=it.encode('windows-1251')
	#except: pass
	return it

def item_f(param):# style='padding:0cm 1.4pt 0cm 1.4pt'
	it=" <tr style='border:solid black 1.0pt;'>\
	  <td>&nbsp;[IMG]</td>\
	  <td>[NAME]</td>\
	  <td>[ON]</td>\
	  <td>&nbsp;&nbsp;&nbsp;[OPTION]</td>\
	  <td>[GROUP]</td>\
	  <td><a name='[CID]'>&nbsp;[CID]</a></td>\
	 </tr>"
	
	gr     = param['group']
	cid    = param['cid']
	option = param['option']
	name   = param['name']
	enable = param['enable']
	img    = param['picon']
	BIMG   = '<a href="/picon/get/'+cid+'"><img border=0 width=19 height=19 src="'+img+'"></a>'
	
	#spc  ='<a><img border=0 width=19 height=19 src="webui.files/space.jpg"></a>'
	#on =  f_on_off2('on_'+cid, 'false')#on_off('/channel/'+cid+'/rem')
	#off = f_on_off2('on_'+cid, 'true')#on_off('/channel/'+cid+'/add')
	unt = button ('/channel/'+cid+'/unite'+"#"+name[:2])
	spl = button ('/channel/'+cid+'/split')
	inf = button ('/info/'+cid)
	bepg= button ('/epg/set_b/'+cid+"#"+name[:2])
	sepg= button ('/epg/set_s/'+cid+"#"+name[:2])
	aarh= button ('/archive/set_aa/'+cid+"#"+name[:2])
	barh= button ('/archive/set_ab/'+cid+"#"+name[:2])
	
	if '[V]' in option: 
		onoff = f_on_off2('on_'+cid, 'false')
	else:
		onoff = f_on_off2('on_'+cid, 'true')
	
	option = option.replace('[U]', unt).replace('[S]', spl).replace('[I]', inf).replace('[V]', '').replace('[X]', '').replace('[E]', bepg).replace('[SE]', sepg).replace('[A]', aarh).replace('[AE]', barh).replace('[Sp]', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')+'&nbsp;&nbsp;'#.replace('[V]', on).replace('[X]', off)
	
	#it=it.replace('[NAME]',   input('/channel/'+cid+'/rename/', name, 200, enable))
	it=it.replace('[NAME]',   f_text('nm_'+cid, name, 200, enable))
	it=it.replace('[CID]',    cid )
	it=it.replace('[ON]', onoff)
	it=it.replace('[OPTION]', option)
	it=it.replace('[GROUP]',  f_text('gr_'+cid, gr, 200, enable))
	#it=it.replace('[IMG]', img)
	try:it=it.replace('[IMG]', BIMG)#img
	except:pass
	return it


def item2(link, name, img=''):
	it=" <tr style='mso-yfti-irow:1'>\
	  <td width=366 valign=top style='width:274.75pt;border:solid black 1.0pt;\
	  mso-border-themecolor:text1;border-top:none;mso-border-top-alt:solid black .5pt;\
	  mso-border-top-themecolor:text1;mso-border-alt:solid black .5pt;mso-border-themecolor:text1;\
	  padding:0cm 5.4pt 0cm 5.4pt'>\
	  <p class=MsoNormal style='margin-bottom:0cm;margin-bottom:.0001pt;line-height:normal'>\
	  <span lang=EN-US style='mso-ansi-language:EN-US'> <img border=0 width=20 height=20 src='[IMG]'> <a name='[MARC]' href='[LINK]'>[NAME]</a><o:p></o:p></span></p>\
	  </td>\
	 </tr>"
	 
	try: it=it.replace('[MARC]',  name[:2])
	except: pass
	it=it.replace('[NAME]',  name)
	it=it.replace('[LINK]',  link)
	it=it.replace('[IMG]',   img)
	
	#try:it=it.decode('utf-8')
	#except: pass
	#try:it=it.encode('windows-1251')
	#except: pass
	
	return it

def item3(param):
	it=" <tr style='border:solid black 1.0pt;'>\
	  <td>[NAME]</td>\
	  <td style='padding:0cm 5.4pt 0cm 5.4pt'><p>[OPTION]</p></td>\
	 </tr>"
	
	option = '[>] [<] [U] [L] [Sp] [I] [Sp] [X]'
	name = param['name']
	lock = param['lock']
	gid = str(param['id'])
	
	spc  ='<a><img border=0 width=19 height=19 src="webui.files/space.jpg"></a>'
	up   = button ('/group/'+gid+'/up')
	down = button ('/group/'+gid+'/down')
	unt  = button ('/group/'+gid+'/unite')
	rem  = button ('/group/'+gid+'/rem')
	lc   = button ('/gr_edit/'+name)
	if lock == 'true': lk = lock_btn('/group/'+gid+'/unlock')
	else:              lk = lock_btn('/group/'+gid+'/lock')
	option = option.replace('[<]', up).replace('[>]', down).replace('[U]', unt).replace('[L]', lk).replace('[X]', rem).replace('[I]', lc).replace('[Sp]', spc)
	
	it=it.replace('[NAME]',   input('/group/'+gid+'/rename/', name, 200))
	it=it.replace('[OPTION]', option)
	
	try:it=it.decode('utf-8')
	except: pass
	try:it=it.encode('windows-1251')
	except: pass
	return it

def item4(param):
	it=" <tr style='border:solid black 1.0pt;'>\
	  <td style='padding:0cm 5.4pt 0cm 5.4pt'>[NAME]</td>\
	  <td style='padding:0cm 5.4pt 0cm 5.4pt'><p>[LINK]</p></td>\
	  <td style='padding:0cm 5.4pt 0cm 5.4pt'><p>[B]</p></td>\
	 </tr>"
	
	lock=param['lock']
	sid=base64.b64encode(param['sid'])
	if lock: lk = lock_btn('/black_list/'+sid+'/unlock/'+param['id'])
	else:    lk = lock_btn('/black_list/'+sid+'/lock/'+param['id'])
	
	it=it.replace('[NAME]', param['serv'])
	it=it.replace('[LINK]', param['url'])
	it=it.replace('[B]', lk)
	
	try:it=it.decode('utf-8')
	except: pass
	try:it=it.encode('windows-1251')
	except: pass
	return it

def item5(param):
	it=" <tr style='border:solid black 1.0pt;'>\
	  <td style='padding:0cm 1.4pt 0cm 1.4pt'><img border=0 width=20 height=19 src='[IMG]'></td>\
	  <td>[NAME]</td>\
	  <td style='padding:0 5.4pt'>[OPTION]</td>\
	  <td><p>[GROUP]</p></td>\
	  <td style='padding:0 5.4pt'><a name='[CID]'>[CID]</a></td>\
	 </tr>"
	
	try:it=it.decode('utf-8')
	except: pass
	try:it=it.encode('windows-1251')
	except: pass
	return it


def item6(link, img=''):
	it=" <tr>\
	  <td>\
	  <a href='[LINK]'><img border=0 width=80 height=80 src='[IMG]'></a>\
	  </td>\
	 </tr>"
	 
	it=it.replace('[LINK]',   link )
	it=it.replace('[IMG]', img)
	
	try:it=it.decode('utf-8')
	except: pass
	try:it=it.encode('windows-1251')
	except: pass
		
	return it

def item7(param):
	it=" <tr style='border:solid black 1.0pt;'>\
	  <td>[NAME]</td>\
	  <td style='padding:0cm 5.4pt 0cm 5.4pt'><p>[OPTION]</p></td>\
	 </tr>"
	
	option = '[>] [<] [B] [E] [Sp] [X]'
	name = param['name']
	ncl = param['n']
	cid = str(param['id'])
	gr = str(param['group'])
	total = param['total']
	next=ncl+1
	if next>=total: next=0
	prev=ncl-1
	if prev<0: prev=total
	
	spc  ='<a><img border=0 width=19 height=19 src="webui.files/space.jpg"></a>'
	up   = button ('/group/'+gr+'/set_cn/'+cid+'/icd/'+str(next))
	down = button ('/group/'+gr+'/set_cn/'+cid+'/icu/'+str(prev))
	begin= button ('/group/'+gr+'/set_cn/'+cid+'/icb/0')
	end  = button ('/group/'+gr+'/set_cn/'+cid+'/ice/'+str(total))
	rem  = button ('/channel/'+cid+'/rem_group/'+gr)
	option = option.replace('[<]', up).replace('[>]', down).replace('[B]', begin).replace('[E]', end).replace('[X]', rem).replace('[Sp]', spc)
	
	it=it.replace('[OPTION]', option)
	it=it.replace('[NAME]', name)
	return it

def input(link, val='', width=105, enable=True):
	if enable: dis =''
	else: dis = 'disabled'
	t="<form style='width:"+str(width)+"pt;height:3.3pt;' action='[ADR]' method='get'><input style='padding:0cm 1.4pt; height:12pt; border:0; width:"+str(width-28)+"pt;' type='text' name='val' value='[VAL]'/><input type='submit' value='ok' "+dis+"/></form>"
	t=t.replace('[ADR]', link)
	t=t.replace('[VAL]', val)
	return t

def listbox(link, L=[], val='', width=65):
	
	t1='<form style="width:'+str(width)+'pt; height:3.3pt;" action="[LINK]" method="get">\
		<select style="border:0; padding:0cm 1.4pt;" size="1" name="val">'
	t2='	</select>\
		<input type="submit" value="ok"></form>'
	it = '		<option [SEL]>[VAL]</option>'
	lit = ''
	for i in L:
		if i == val: sel = 'selected'
		else:        sel = ''
		lit+=it.replace('[SEL]',sel).replace('[VAL]',i)
	t1=t1.replace('[LINK]',link)
	
	return t1+lit+t2


def f_text(ID, val='', width=110, enable=True):
	if enable: dis =''
	else: dis = 'disabled'
	t="<input style='padding:0cm 1.4pt; border:0; width:"+str(width)+"pt;' type='text' name='"+ID+"' value='"+val+"' "+dis+"/>"
	return t

def f_on_off(ID, val):
	if val=='true': ck =''
	else: ck = 'checked'
	t="<input type='checkbox' name='"+ID+"' value='true' "+ck+"/>"
	return t

def f_on_off2(ID, val):
	if val=='true': ck =''
	else: ck = 'checked'
	t="<label><input type='checkbox' name='"+ID+"' value='true' "+ck+"><span></span></label>"
	return t