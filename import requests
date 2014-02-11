import requests
from bs4 import BeautifulSoup

colours = []

#hex = raw_input('HEX: '
hex = '0a1a34'
limit = 25
r = requests.get('http://0to255.com/'+hex)
soup = BeautifulSoup(r.text)
array = soup.findAll('span','hex_color')
for each in array:
	colours.append(each.string)

lindx = colours.index('#'+hex)

print "['"+"','".join(colours[lindx-limit:lindx])+"']"