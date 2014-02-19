from datetime import datetime
from pymongo import MongoClient
import calendar as cal
import json

INIT = 119145600

client = MongoClient('localhost')
db = client.dev

j = open('US-STATES.json').read()
j = unicode(j, errors='ignore')
j = json.loads(j)

for y in range(2008, 2014):
    for m in range(1, 12, 3):
        d = cal.timegm(datetime.timetuple(datetime(y, m, 1, 0, 0, 0)))
        f = open(str(d)+'.tsv', 'w')
        f.write('id\trate\n')
        for each in j['features']:
            geometry = each['geometry']
            try:
                if geometry['type'] == 'Polygon':
                    count = db.rentals_v2.find({
                        'instantiated': {
                            '$gte': INIT,
                            '$lte': d+7862400
                        }, 'latLng': {
                            '$geoWithin': {
                                '$geometry': {
                                    "type": "Polygon",
                                    "coordinates": geometry['coordinates']
                                }
                            }
                        }, 'propType.id': 0
                    }).count()
                else:
                    count = 0
                    for array in geometry['coordinates']:
                        count += db.rentals_v2.find({
                            'instantiated': {
                                '$gte': INIT,
                                '$lte': d+7862400
                            }, 'latLng': {
                                '$geoWithin': {
                                    '$geometry': {
                                        "type": "Polygon",
                                        "coordinates": array
                                    }
                                }
                            }, 'propType.id': 0
                        }).count()
                print each['properties']['GEO_ID'].split('US')[-1], count
                f.write(each['properties']['GEO_ID'].split('US')[-1]+'\t'+str(count)+'\n')
            except:
                break
        f.close()
