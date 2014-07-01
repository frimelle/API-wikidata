# -*- coding: utf-8  -*-

#included in wd-stats.py file already
import re
import urllib2
import json

def url_opener(url):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Script to get the statistics, lucie.kaffee@wikimedia.de')] 
	infile = opener.open(url)
	page = json.load(infile)
	return page


def number_properties():
	props = []
	for i in range(1, 10):
		if i == 9: 
			url = "https://www.wikidata.org/w/api.php?action=query&list=allpages&aplimit=500&apnamespace=120&format=json&apfrom=P9"
		else:
			url = "https://www.wikidata.org/w/api.php?action=query&list=allpages&aplimit=500&apnamespace=120&format=json&apfrom=P" + str(i) + "&apto=P" + str(i+1)	
		props.append(url_opener(url))
	property_titles = []
	for x in range(0, 9): 
		my_dict = props[x]
		for y in range(0, len(my_dict["query"]["allpages"])):
			pro= my_dict["query"]["allpages"][y]["title"]
			tmp = pro.split(':')
			property_titles.append(tmp[1])	
	return len(property_titles)
	
	
print number_properties()


