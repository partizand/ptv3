# coding: utf-8
import urllib, urllib2

def findall(http, ss, es):
	L=[]
	while http.find(es)>0:
		s=http.find(ss)
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L

def mfind(t,s,e):
	r=t[t.find(s)+len(s):]
	r2=r[:r.find(e)]
	return r2

def getURL3(url,Referer = 'http://emulations.ru/'):
	urllib2.install_opener(urllib2.build_opener()) 
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	req.add_header('Referer', Referer)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def get(title):
	print '== select_icon =='
	#if " TV" not in title: title=title+" TV"
	title=title.replace(' HD', '').replace('(+1)', '').replace('(+2)', '').replace('(+3)', '').replace('(+4)', '').replace('(+5)', '').replace('(+6)', '')
	url='https://tvpedia.fandom.com/ru/wiki/Служебная:Search?search='+urllib.quote_plus(title)+'&fulltext=Search&ns6=1&filters%5B%5D=is_image&rank=default'
	print url
	hp=getURL3(url)
	#print hp
	ss='data-src="'
	es='" onload='
	L=findall(hp, ss, es)
	L2=[]
	for i in L:
		if 'http' in i: L2.append(i[10:].replace('&amp;', '&'))
	return L2
	
#print get_picons('mezzo')