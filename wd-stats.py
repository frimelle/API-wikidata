import re
import urllib2
import json

#different statistics regarding wikidata

def url_opener(url):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Script to get the statistics, lucie.kaffee@wikimedia.de')] 
	infile = opener.open(url)
	page = json.load(infile)
	return page
	

#calculates the number of properties by getting all properties and titles and then counts the titles
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
	
#saves the json data in a python dictonary to get the data from the statistic already made
statsdict = url_opener('https://www.wikidata.org/w/api.php?action=query&meta=siteinfo&siprop=statistics&format=json')

pages = statsdict["query"]["statistics"]["pages"]
articles = statsdict["query"]["statistics"]["articles"]
edits = statsdict["query"]["statistics"]["edits"]
users = statsdict["query"]["statistics"]["users"]
active_users = statsdict["query"]["statistics"]["activeusers"]
admins = statsdict["query"]["statistics"]["admins"]

#percent_active_users = (float(active_users)/float(users)) * 100.0 //calculating the number of active users doesn't make sense in this case. 
average_edits_per_page = float(edits) / float(pages)
# round average_edits_per_page to two decimal places
average_edits_per_page = round(average_edits_per_page, 2)

properties = number_properties()

print "Pages: " + str(pages) + "\nArticles: " + str(articles) + "\nEdits: " + str(edits) + "\nUsers: "+ str(users) + "\nActive Users: " + str(active_users) + "\nAdmins: " + str(admins) + "\nAverage Edits per Page: " + str(average_edits_per_page) + "\nNumber of Properties: " + str(properties)
