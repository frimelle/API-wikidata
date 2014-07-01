# -*- coding: utf-8  -*-

import re
import urllib2
import json

def url_opener(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Script to look for statements in properties, lucie.kaffee@wikimedia.de')]
    infile = opener.open(url)
    page = json.load(infile)
    return page

def get_all_properties():
    props = []
    for i in range(1, 10):
        if i == 9:
            url = "http://localhost/mediawiki/api.php?action=query&list=allpages&aplimit=500&apnamespace=122&format=json&apfrom=P9"
        else:
            url = "http://localhost/mediawiki/api.php?action=query&list=allpages&aplimit=500&apnamespace=122&format=json&apfrom=P" + str(i) + "&apto=P" + str(i+1)   
        props.append(url_opener(url))
    return props
   
def get_property_titles(props):
    property_titles = []
    for x in range(0, 9):
        my_dict = props[x]
        for y in range(0, len(my_dict["query"]["allpages"])):
            pro= my_dict["query"]["allpages"][y]["title"]
            tmp = pro.split(':')
            property_titles.append(tmp[1])   
    return property_titles


def get_urls(titles):
	urls = []
	url = "http://localhost/mediawiki/api.php?action=wbgetentities&format=json&props=claims&ids="
	i = 1
	if len(titles) > 49:
		for x in range(0, len(titles)): # iterate through all titles
			if i < 49:
				url = url  + str(titles[x]) + "|"
				i = i + 1
			else:
				url = url + str(titles[x])
				urls.append(url)
				url = "http://localhost/mediawiki/api.php?action=wbgetentities&format=json&props=claims&ids="
				i = 0
	else:
		#one title is twice this way
		url = url + str(titles[0])
		for x in range(0, len(titles)):
			url = url + '|' + str(titles[x])
		urls.append(url)
	#print urls
	return urls

def check_claims(urls):
    for x in range(0, len(urls)):
        page = url_opener(urls[x])
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

