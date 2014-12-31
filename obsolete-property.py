import gzip
import json

#This script is supposed to check for obsolete Properties - Properties who have 'instance of obsolete Wikidata property'

def isInstanceOfObsoleteProperty(json_l):
	#check if the things we will look for are actually there (otherwise there are errors, e.g. when there is no datavalue attribute)
		if 'claims' in json_l and 'P31' in json_l['claims'] and 'datavalue' in json_l['claims']['P31'][0]['mainsnak']:
			#check if instance of (P31) obsolete Wikidata property (Q18644427):
			instanceOf_id = json_l['claims']['P31'][0]['mainsnak']['datavalue']['value']['numeric-id']
			if instanceOf_id == 18644427: 
				return True
		else:
			return False


#open thw wikidata dump here, adjust the name of the dump file accordingly!
f = gzip.open('20141229.json.gz')

#iterate through the file line by line 
for line in f:
	line = line.rstrip().rstrip(',')
	try:
		json_l = json.loads(line)
	except ValueError, e:
		continue

	if isInstanceOfObsoleteProperty(json_l):
		print json_l['id']