# -*- coding: utf-8 -*-  
import urllib2
from BeautifulSoup import BeautifulSoup, Tag
import sys, getopt

class GoogleSearch():

	site = "http://www.google.com.hk"
	ua_header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.65 Safari/537.36'}

	def google(self, query, num=20, skip=0, language=None, filterResults=False, safe=False):
		if len(query)<2:
			return []
		try:
			html = self.__query__(self.getURL(query,num,skip,language,filterResults,safe))
			return self.__handleResult__(html)
		except (IOError, KeyError, urllib2.URLError, urllib2.HTTPError):
			print "Error: Unable to search Google"
			return []

	def getURL(self, query, num=20, skip=0, language=None, filterResults=False, safe=False):
		query = query.strip()
		query = query.replace(" ","+")
		query = query.replace("&","%26")

		url = ("%s/search?q=%s" % (self.site, query))
		url += "&num=" + str(num)
		if language=="English":
			url += "&lr=lang_en"
		elif language=="Chinese Simplified":
			url += "&lr=lang_zh-CN"
		if filterResults:
			url += "&filter=1"
		else:
			url += "&filter=0"
		if safe:
			url += "&safe=active"
		else:
			url += "&safe=off"
		if skip>0:
			url+= "&start="+str(skip)

		return url



	def __query__(self, url):

		req = urllib2.Request(url,headers = self.ua_header)

		htmlString = urllib2.urlopen(req).read()

		return htmlString

	def __cleanString__(self, st):
		st = st.replace("&#39;","'").replace("&nbsp;"," ")
		st = st.replace("&middot;","").replace("&quot;","\"")
		st = st.replace("&amp;","&").replace("&lt;","<").replace("&gt;",">")
		return st

	def __handleResult__(self, htmlString):
		results = []
		raw = BeautifulSoup(htmlString)
		rcs = raw.findAll('div',attrs={'class':'rc'}) #result containers
		for rc in rcs:
			part = {}

			titleRaw = rc.find(attrs={'class':'r'}).a #title
			title = ""
			for t in titleRaw.contents:
				while type(t)==Tag: #<em></em> case
					t = t.contents[0]
				title += t

			synopRaw = rc.find('span',attrs={'class':'st'}) #synopsis
			synopsis = ""
			if synopRaw!=None:				
				for s in synopRaw.contents:
					while type(s)==Tag: #<em></em> case
						s = s.contents[0]
					synopsis += s
			part['title'] = self.__cleanString__(title)
			part['url'] = titleRaw['href']
			part['synop'] = self.__cleanString__(synopsis)
			results.append(part)

		return results


def main(argv):
	
	usage = "usage: search.py -q <query> [-n <num to fetch>] [-k (skip first xxx results)] [-l English|Chinese] [-f (filter similar results)] [-s (safe search)] [-h (help)]"

	try:
		opts, args = getopt.getopt(argv, "q:k:n:l:fsh")
	except getopt.GetoptError:
		print usage
		sys.exit(2)

	num=20
	language=None
	filterResults=False
	safe=False
	skip=0
	query=""

	for opt, arg in opts:
		if opt=="-q":
			query = arg
    	if opt=="-h":
    		print usage
    		sys.exit(0)
    	elif opt=="-n":
    		num = arg
    	elif opt=="-k":
    		skip = args
    	elif opt=="-l":
    		language = arg
    	elif opt=="-f":
    		filterResults = arg
    	elif opt=="-s":
    		safe = arg


	if len(query) < 2:
		print "Query should be at least 2 characters"
		sys.exit(2)

	gsearch = GoogleSearch()
	results = gsearch.google(query,num, language, filterResults, safe)
	for res in results:
		for key ,value in res.items():
			print key, value


if __name__ == '__main__':
	main(sys.argv[1:])
