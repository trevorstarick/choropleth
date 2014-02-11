from pprint import pprint
from pymongo import MongoClient
import json

client = MongoClient('api.outpost.travel')
db = client.dev
db.authenticate('write','Cycm1C&SiTOh')

j = open('US-COUNTIES.json').read()
j = unicode(j, errors='ignore')
j = json.loads(j)

f = open('US.tsv','w')
f.write('name\tid\trate\n')

for each in j['features']:
	geometry = each['geometry']
	try:
		if geometry['type'] == 'Polygon':
			count = db.rentals_v2.find({
				'latLng': {
					'$geoWithin': {
						'$geometry': {
							"type": "Polygon",
							"coordinates": geometry['coordinates']
						}
					}
				}
			}).count()
		else:
			count = 0
			for array in geometry['coordinates']:
				count += db.rentals_v2.find({
					'latLng': {
						'$geoWithin': {
							'$geometry': {
								"type": "Polygon",
								"coordinates": array
							}
						}
					}
				}).count()
		print each['properties']['GEO_ID'].split('US')[-1],count
		f.write(each['properties']['GEO_ID'].split('US')[-1]+'\t'+str(count)+'\n')
	except:
		print '[!] Skipped',each['properties']['GEO_ID'].split('US')[-1]
f.close()