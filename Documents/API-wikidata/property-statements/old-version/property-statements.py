# -*- coding: utf-8  -*-

import re
import urllib2

import json

def get_all_properties():
	props = []
	for i in range(1, 10):
		if i == 9: 
			url = "https://www.wikidata.org/w/api.php?action=query&list=allpages&aplimit=500&apnamespace=120&format=json&apfrom=P9"
		else:
			url = "https://www.wikidata.org/w/api.php?action=query&list=allpages&aplimit=500&apnamespace=120&format=json&apfrom=P" + str(i) + "&apto=P" + str(i+1)
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Script to look for statements in properties, lucie.kaffee@wikimedia.de')] 
		infile = opener.open(url)
		page = json.load(infile)
		props.append(page)
		#print props
	return props
	
def get_property_titles():
	props = get_all_properties()
	property_titles = []
	for x in range(0, 9): 
		my_dict = props[x]
		for y in range(0, len(my_dict["query"]["allpages"])):
			pro= my_dict["query"]["allpages"][y]["title"]
			tmp = pro.split(':')
			property_titles.append(tmp[1])
	#print property_titles	
	return property_titles


def get_urls():
	titles = get_property_titles()
	urls = []
	url = "https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=claims&ids="
	i = 1
	if len(titles) > 49:
		for x in range(0, len(titles)): # durch alle titles durchgehen.
			if i < 49:
				url = url  + str(titles[x]) + "|"
				i = i + 1
			else: 
				url = url + str(titles[x])
				urls.append(url)
				url = "https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=claims&ids="
				i = 0
	else:
		url = "https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=claims&ids=" + titles[0]
		for x in range(1, len(titles)):
			url = url + "|" + str(titles[x])
		urls.append(url)
	return urls

def check_claims(): 
	urls = get_urls()
	for x in range(0, len(urls)):
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Script to look for statements in properties, lucie.kaffee@wikimedia.de')] 
		infile = opener.open(urls[x])
		page = json.load(infile)
		if "claim" in str(page):
			print "Found claims!"
			break;
		else:
			print "All good!"

check_claims()		
#print get_property_titles()
#print get_all_properties()
