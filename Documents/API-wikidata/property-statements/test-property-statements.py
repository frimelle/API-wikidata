# -*- coding: utf-8  -*-

import re
import urllib2

import json

#to open the urls I use further on
def url_opener(url):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Script to look for statements in properties, lucie.kaffee@wikimedia.de')] 
	infile = opener.open(url)
	page = json.load(infile)
	return page

#Goes through all properties (since they are not ordered in an usual numeric way, this looks pretty weird but works well) and opens them
#returns the data of all properties
def get_all_properties():
	props = []
	for i in range(1, 10):
		if i == 9: 
			url = "http://localhost/mediawiki/api.php?action=query&list=allpages&aplimit=500&apnamespace=122&format=json&apfrom=P9"
		else:
			url = "http://localhost/mediawiki/api.php?action=query&list=allpages&aplimit=500&apnamespace=122&format=json&apfrom=P" + str(i) + "&apto=P" + str(i+1)	
		props.append(url_opener(url))
	return props
	
#splits the data of get_all_properties, so it can get the titles of the properties
#returns all the titles of all properties (P1, P1 etc)
def get_property_titles(props):
	property_titles = []
	for x in range(0, 9): 
		my_dict = props[x]
		for y in range(0, len(my_dict["query"]["allpages"])):
			pro= my_dict["query"]["allpages"][y]["title"]
			tmp = pro.split(':')
			property_titles.append(tmp[1])	
	return property_titles

#uses the titles of properties to make an array of links with up to 50 properties in one link
#returns links, which could use the API and have up to 50 properties they could request at once
def get_urls(titles):
	#titles = get_property_titles()
	urls = []
	url = "http://localhost/mediawiki/api.php?action=wbgetentities&format=json&props=claims&ids="
	i = 1
	if len(titles) > 49:
		for x in range(0, len(titles)): # durch alle titles durchgehen.
			if i < 49:
				url = url  + str(titles[x]) + "|"
				i = i + 1
			else: 
				url = url + str(titles[x])
				urls.append(url)
				url = "http://localhost/mediawiki/api.php?action=wbgetentities&format=json&props=claims&ids="
				i = 0
	else:
		url = "http://localhost/mediawiki/api.php?action=wbgetentities&format=json&props=claims&ids=" + titles[0]
		for x in range(1, len(titles)):
			url = url + "|" + str(titles[x])
		urls.append(url)
	return urls

# opens the array of links to check if they include the word "claim" to see if the properties have claims
# prints "All good" for all the links that don't have claims and "Found claims!" for links that include properties, which have claims
def check_claims(urls): 
	for x in range(0, len(urls)):
		page = url_opener(urls[x])
		print page
		if "claim" in str(page):
			print "Found claims!"
			print urls[x]
			break;
		else:
			print "All good!"		

props = get_all_properties()
titles = get_property_titles(props)
urls = get_urls(titles)
check_claims(urls)
