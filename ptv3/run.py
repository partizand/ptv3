# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import threading, SocketServer, BaseHTTPServer
import sys, os, json
import time
import urllib, urllib2, socket
import base64

sys.path.append(os.getcwd())
serv_py = os.path.join(os.getcwd(), "server.py" )
fl = open(serv_py, "r")
t=fl.read()
fl.close()

exec(t)
#pyinstaller -F -w d:\ptv3\run.py