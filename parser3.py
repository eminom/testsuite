
# This module runs in python2(Before March.13th.2o16)
# Now it is in Python3

#import HTMLParser
#in Python3
import os
import sys
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.error   import HTTPError
import re
from localconf import GetRootUri
from PyXxhashMod import xxhash

class MyHrefSniffer(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self._a = []
		self._hrefs = []
	def handle_starttag(self, tag, attrs): 
		self._a.append(tag)
		#print('href is %s' % attrs['href'])
		if 'a' == tag:
			if len(attrs) > 0:
				href, hvalue = attrs[0]
				xxhasht, xxhashvalue = 'none', False
				if len(attrs) > 1:
					xxhasht, xxhashvalue = attrs[1]
				if 'href' == href:
					pre = "fetch/"
					if hvalue.startswith(pre):
						uri = hvalue[len(pre):]
						#print(uri)
						# assert( href == 'href', "Must be true")
						#hvalue[:
						entry = {'uri':uri}
						if xxhasht == 'xxhash' and type(xxhashvalue) is str:
							entry['xxhash'] = xxhashvalue
						self._hrefs.append(entry)

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
	def __makeSubDir(self, sd):
		try:
			os.makedirs(sd)
		except:
			pass
		#try except WindowsError

	def __init__(self, hrefs, startdir, seed):
		self._urls = hrefs[:]
		self._subspace = re.compile(' ')
		self._taskCount = 0
		self._passedCount = 0
		self._verifiCount = 0
		self._verifiFailed= 0
		self._failedUrl = []
		self._startdir = startdir
		self._seed = seed
		print("seed<%s>" % seed)
		self.__makeSubDir(startdir)

	def formatSub(self, sub):
		return "%s%s%s" % (self._startdir, os.sep, sub)
	def goTask(self):
		for entry in self._urls:
			assert 'uri' in entry.keys()
			uri = entry['uri']
			if 'xxhash' in entry.keys():
				assert type(entry['xxhash']) is str
				# print("%s has an xxhash value<%s>" % ( uri, entry['xxhash']))
				#pass
			self._taskCount += 1
			url = FormatMyUrl(uri)
			base, _ =  getDir(uri)
			if len(base) > 0:
				tbase = self.formatSub(base)
				self.__makeSubDir(tbase)
			else:
				pass
				#print("base is (%s)" % base)
			print("get <%s> ... " % (url), end="")
			# sys.stdout.flush()
			try:
				url = self._subspace.sub('%20', url) 
					#if there is any space in url, urlopen won't return.
				url_input = urlopen(url) 
				turi = self.formatSub(uri)
				chunk = url_input.read()
				# verify
				if 'xxhash' in entry.keys():
					thatHash = entry['xxhash']
					# print("seed %s" %self._seed)
					thisHash = xxhash(chunk, self._seed)
					if thatHash == thisHash:
						print("<%s> OK" % (thisHash), end="")
						self._verifiCount += 1
					else:
						print("verification failed for <%s> from <%s>" % (thisHash, thatHash), end="")
						self._verifiFailed += 1
				with open(turi, "wb") as fout:
					fout.write(chunk)
				#print("saved to %s" % (uri))
				#sys.stdout.flush()   # Must be flush to stay in updated.
				self._passedCount += 1
				print('.')
			except HTTPError as e:
				print('failed')
				self._failedUrl.append(url)
	def prtSummary(self):
		print("Tasks got/total/verified/v-failed = (%d/%d/<%d/%d>)" % (self._passedCount, self._taskCount, self._verifiCount, self._verifiFailed))
		if self._passedCount == self._taskCount and self._taskCount == self._verifiCount and self._taskCount > 0:
			print("all content verified")
		for failed in self._failedUrl:
			print(failed)


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

def GetSeed():
	#url = 
	#seed = urlopen(url).read()
	#print("Seed<%s>" %seed)
	seed = int(urlopen(GetRootUri() + "/seed").read().decode('utf8').strip('\r\n\x00'), 16)
	return seed

if '__main__' == __name__:
	s = MyHrefSniffer()
	s.feed(LoadChunk()) 
	#s.prt()
	d = Downloader(s.getUrls(), os.getcwd() + os.sep + 'scratch', GetSeed())
	d.goTask()
	d.prtSummary()



