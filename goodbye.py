#!/usr/bin/python

import datetime
import hashlib
import json
import optparse
import os
import sys
import urllib2
import zipfile
import re

from incode.httputils import *



print ("""

                     GoodBye v1
..................................................................
               Made By ybenel - ybenel@molero.xyz

	MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
	MMMMMMMMMMNKWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
	MMMMMMMMMNc.dWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
	MMMMMMMMWd. .kWMMMMMMMMMMMMMMMMMMMMMMW0KMMMMMMMMMM
	MMMMMMMMk:;. 'OMMMMMMMMMMMMMMMMMMMMMWx.,0MMMMMMMMM
	MMMMMMMK:ok.  ,0MMMMMMMMMMMMMMMMMMMWO. .cXMMMMMMMM
	MMMMMMNl:KO.   ;KWNXK00O0000KXNWMMWO' .c;dWMMMMMMM
	MMMMMMx,xNk.    .;'...    ....';:l:.  ,0l,0MMMMMMM
	MMMMMK;,l;. .,:cc:;.                  .dx,lWMMMMMM
	MMMMWo    ,dKWMMMMWXk:.      .cdkOOxo,. ...OMMMMMM
	MMMM0'   cXMMWKxood0WWk.   .lkONMMNOOXO,   lWMMMMM
	MMMWl   ;XMMNo.    .lXWd. .dWk;;dd;;kWM0'  '0MMMMM
	kxko.   lWMMO.      .kMO. .OMMK;  .kMMMNc   oWMMMM
	X0k:.   ;KMMXc      :XWo  .dW0c,lo;;xNMK,   'xkkk0
	kko'     :KMMNkl::lkNNd.   .dkdKWMNOkXO,    .lOKNW
	0Kk:.     .lOXWMMWN0d,       'lxO0Oko;.     .ckkOO
	kkkdodo;.    .,;;;'.  .:ooc.     .        ...ck0XN
	0XWMMMMWKxc'.          ;dxc.          .,cxKK0OkkOO
	MMMMMMMMMMMN0d:'.  .'        .l'  .;lxKWMMMMMMMMMN
	MMMMMMMMMMMMMMMN0xo0O:,;;;;;;xN0xOXWMMMMMMMMMMMMMM
	MMMMMMMMMMMMMMMMMMMMMMWWWWWMMMMMMMMMMMMMMMMMMMMMMM
	MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
	MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
	MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
	MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM

Options

-u [URL] 	: Start the scan at the indicated URL
-a 		: Update the vulnerability database

Proxy settings

-p [URL]	: Proxy url (http)
-b [user]	: User to authenticate in proxy
-c [password]	: Password to authenticate in proxy
-d [protocol]  : Proxy authentication protocol: basic, ntlm

""")

parser = optparse.OptionParser()

parser.add_option('-u', '--url', dest="url", help="Address of the website to be scanned")
parser.add_option('-p', '--proxy', dest="prox", help="Http address of the proxy")
parser.add_option('-b', '--proxy-user', dest="proxu", help="User to authenticate in proxy")
parser.add_option('-c', '--proxy-pass', dest="proxp", help="Password to authenticate in proxy")
parser.add_option('-d', '--proxy-auth', dest="proxa", help="Proxy authentication protocol: basic, ntlm")
parser.add_option('-a', action="store_true",dest="act", help="Update database")

options, remainder = parser.parse_args()

def update():
	#TODO: catch HTTP errors (404, 503, timeout, etc)
	print ("New version of the database found, updating...")
	urlup = "https://raw.githubusercontent.com/m1ndo/moodlescan/master/update/data.zip"
	fileDownload(urlup, "data.zip")
	if (r):
			print("An error occurred connecting to the update server: " + str(r.reason) )
			sys.exit()
			
	zip_ref = zipfile.ZipFile('data.zip', 'r')
	zip_ref.extractall('data')
	zip_ref.close()
	os.remove('data.zip')
	print ("\nThe database has been updated correctly.\n")


def checkupdate():
	#TODO: catch HTTP errors (404, 503, timeout, etc)

	urlup = "https://raw.githubusercontent.com/m1ndo/moodlescan/master/update/update.dat"
	
	try:

		fo = open("update.dat", "r+")
		actual = int(fo.readline())
		fo.close()
		
		r = fileDownload(urlup, "update.dat")
		if (r):
			print("An error occurred connecting to the update server: " + str(r.reason) )
			sys.exit()
		
		fo = open("update.dat", "r+")
		ultima = int(fo.readline())
		fo.close()
		
		if ultima > actual:
			update()
		else:
			print("The moodlescan database is already updated (version: " + str(actual) + ").\n")
		
	except IOError as e:
		if e.errno == 2:
			print(e)
			urllib.urlretrieve (urlup, "update.dat")
			fo = open("update.dat", "r+")
			update()
		else:
			print (e)
	



def getheader(url, proxy):
	print ("Obtaining data from the server" + url + " ...\n")
	
	try:
		cnn = httpConnection(url, proxy)
		headers = ['server', 'x-powered-by', 'x-frame-options', 'date', 'last-modified']		
		for el in headers:
			if cnn.info().get(el):
				print (el.ljust(15) + "	: " + cnn.info().get(el))
	except urllib2.URLError as e:
		print("An error occurred connecting to the target : " + str(e.reason) )
		sys.exit()
	except Exception as e:
		print ("\nAn error occurred while trying to connect to the target. Verify the URL.\n\nFind search completed.\n")
		sys.exit()
	

def getversion(url):
	print ("\nGetting .... version...")

	s = [['/admin/environment.xml'], ['/admin/upgrade.txt'], ['/lib/upgrade.txt'], ['/tags.txt'], ['/README.txt']]
	
	i = 0
	for a in s:		
		#TODO: no cache y catch HTTP errors (404, 503, timeout, etc)
		try:
			cnn = urllib2.urlopen(url + a[0])
			cnt = cnn.read()
			s[i].append(hashlib.md5(cnt).hexdigest())
			
		except urllib2.URLError as e:
			if e.code == 404:
				s[i].append(0)
		i = i + 1

	with open('data/version.txt', 'r') as fve:
    		data = fve.read()
		
	f = 100
	version = 0
	for m in s:
		if m[1] != 0:
			l = re.findall(".*" + m[1] + ".*", data)
			if (len(l) < f) and (len(l) > 0) :
				f = len(l)
				version = l[0]

	if version != 0:
		print ("\nFound version via " + version.split(';')[2] + " : Moodle " +  version.split(';')[0])
		return version.split(';')[0].replace("v","")
		
	print ("\nMoodle version not found")
	return False

def getcve(version):	
	print("\nSearching for vulnerabilities...")
	f = open('data/cve.txt','r')
	jsond = json.load(f)
	f.close()
	
	version = "," + version + ","
	
	nvuln = 0
	nexpl = 0
	
	for a in jsond['vulnerabilities']:
		for k , b in a.items():
			if version  in b['affected']:
				nvuln +=1
				print ("\nCVE		: " + k + " ### Kind : " + b['kind'] + " ### Authentication? : " + b['auth'] + " ### Exploit? : " + b['exploit'])
				print ("description	: " + b['description'])
				

	print("\nVulnerabilities found: " + str(nvuln))			
				
				
if options.act:
	checkupdate()

if options.url:
	proxy = httpProxy()

	# is checked if it is necessary to create a proxy instance
	if (options.prox):	

		proxy.url = options.prox

		if (options.proxu):
			proxy.user = options.proxu

		if (options.proxp):
			proxy.password = options.proxp
		
		if (options.proxa):
			proxy.auth = options.proxa

	getheader(options.url, proxy)
	v = getversion(options.url)
	if v:
		getcve(v)
		
	print ("\nFinished search.\n")





