

import HTMLParser
import sys
import os
import urllib2
import re

class MyHrefSniffer(HTMLParser.HTMLParser):
	def __init__(self):
		HTMLParser.HTMLParser.__init__(self)
		self._a = []
		self._hrefs = []
	def handle_starttag(self, tag, attrs): 
		self._a.append(tag)
		#print('href is %s' % attrs['href'])
		if 'a' == tag:
			if len(attrs) > 0:
				href, hvalue = attrs[0]
				if 'href' == href:
					pre = "fetch/"
					if hvalue.startswith(pre):
						uri = hvalue[len(pre):]
						#print(uri)
						# assert( href == 'href', "Must be true")
						#hvalue[:
						self._hrefs.append(uri)

	def handle_endtag(self, tag):
		self._a.pop()
		# if 'a' == tag:
		# 	print "<", tag
	def handle_data(self, data):
		arr = self._a
		if arr and arr[len(arr)-1] == 'a':
			if data.strip():
				pass
				#self._hrefs.append(FormatMyUrl(data.strip()))

	def getUrls(self):
		return self._hrefs
	def prt(self):
		for h in self._hrefs:
			print(h)


def getDir(name):
	try:
		sp = name.rindex('/')
		return (name[:sp], name[sp+1:])
	except ValueError as e:
		return ('', name)

class Downloader():
	def __init__(self, hrefs, startdir):
		self._urls = hrefs[:]
		self._subspace = re.compile(' ')
		self._taskCount = 0
		self._passedCount = 0
		self._failedUrl = []
		self._startdir = startdir
		try:
			os.makedirs(startdir)
		except WindowsError:
			pass

	def formatSub(self, sub):
		return "%s%s%s" % (self._startdir, os.sep, sub)
	def goTask(self):
		for uri in self._urls:
			self._taskCount += 1
			url = FormatMyUrl(uri)
			base, _ =  getDir(uri)
			if len(base) > 0:
				try:
					tbase = self.formatSub(base)
					os.makedirs(tbase)
				except WindowsError:
					pass
			else:
				pass
				#print("base is (%s)" % base)
			print "retrieving <%s> ... " % (url) ,
			sys.stdout.flush()
			try:
				url = self._subspace.sub('%20', url) #if there is any space in url, urlopen won't return. 
				url_input = urllib2.urlopen(url) 
				turi = self.formatSub(uri)
				with open(turi, "wb") as fout:
					fout.write(url_input.read())
				#print("saved to %s" % (uri))
				#sys.stdout.flush()   # Must be flush to stay in updated.
				print 'done'
				self._passedCount += 1
			except urllib2.HTTPError as e:
				print 'failed'
				self._failedUrl.append(url)
	def prtSummary(self):
		print "Tasks performed done/total = (%d/%d)" % (self._passedCount, self._taskCount)
		for failed in self._failedUrl:
			print failed


def GetRootUri():
	return "http://192.168.0.102:13000"
	#return "http://127.0.0.1:13000"
	#return "http://192.168.210.176:13000"
	#return "http://127.0.0.1:13000"
	#return "http://192.168.210.179:13000"

def FormatMyUrl(name):
	return "%s/fetch/%s" % ( GetRootUri(),  name )

def LoadChunk():
	content = ''
	i = 0
	for f in sys.stdin.readlines():
		i = 1 + i
		content += f
		# if '<' == f[0]:
		# 	content += f
	return content

def LoadFromFile():
	content = ''
	target = '1.html'
	#print("Load from %s" % target)
	with open(target) as fin:
		for f in fin.readlines():
			content += f
	return content

if '__main__' == __name__:
	s = MyHrefSniffer()
	s.feed(LoadChunk()) 
	#s.prt()
	d = Downloader(s.getUrls(), os.getcwd() + os.sep + 'scratch')
	d.goTask()
	d.prtSummary()



