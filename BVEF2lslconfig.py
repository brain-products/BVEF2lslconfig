import sys
import os
import xml.etree.ElementTree as ET
import re
import ntpath

bvefin_name = sys.argv[1]
configin_name = sys.argv[2]

bv_tree = ET.parse(bvefin_name)
bv_root = bv_tree.getroot()

# do this because LSL config files typically do not have roots
# and python can't parse such xml files
with open(configin_name) as f:
	xml = f.read()
con_root = ET.fromstring(re.sub(r"(<\?xml[^>]+\?>)", r"\1<root>", xml)+"</root>")

electrode_names = []

for electrode in bv_root.findall('Electrode'):
	#electrode = electrodes.find('Electrode')
	electrode_names.append(electrode.find('Name').text)

for n in electrode_names:
	if n == 'GND':
		electrode_names.remove('GND')
		break
for n in electrode_names:
	if n == 'REF':
		electrode_names.remove('REF')

for n in electrode_names:
	if n == 'Fpz Gnd':
		electrode_names.remove(n)
		break

for n in electrode_names:
	if n == 'FCz Ref':
		electrode_names.remove(n)
		break
for channels in con_root.findall('channels'):
	con_root.remove(channels)

channels = ET.SubElement(con_root, 'channels')
labels = ET.SubElement(channels, 'labels')
for electrode_name in electrode_names:
	ET.SubElement(labels,'label').text=electrode_name

con_name_bits = re.split('.cfg', configin_name)
bvefin_basename = ntpath.basename(bvefin_name)
bvef_name_bits = re.split('.bvef', bvefin_basename)
configout_name = con_name_bits[0] + '-' + bvef_name_bits[0] + '.cfg'

s = ET.tostring(con_root).decode('utf-8')
s = re.sub(r"<root>","<?xml version=\"1.0\" encoding=\"utf-8\"?>", s)
s = re.sub(r"</root>","", s)

f = open(configout_name, "w")
f.write(s)



