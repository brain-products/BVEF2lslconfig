import sys
import os
import xml.etree.ElementTree as ET
import re
import ntpath

try:
	import configparser as CP
except ImportError:
	import ConfigParser as CP

bvefin_name = sys.argv[1]
configin_name = sys.argv[2]
num_args = len(sys.argv)
if num_args is 4:
	if sys.argv[3] == 'XML':
		is_conf_XML = True
	else:
		is_conf_XML = False
else:
	is_conf_XML = False

# setup output file name
con_name_bits = re.split('.cfg', configin_name)
bvefin_basename = ntpath.basename(bvefin_name)
bvef_name_bits = re.split('.bvef', bvefin_basename)
configout_name = con_name_bits[0] + '-' + bvef_name_bits[0] + '.cfg'

# parse bvef file
electrode_names = []
bv_tree = ET.parse(bvefin_name)
bv_root = bv_tree.getroot()
for electrode in bv_root.findall('Electrode'):
	# electrode = electrodes.find('Electrode')
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

# parse config file as xml and write new one
if is_conf_XML is True:

	# do this because LSL config files typically do not have roots
	# and python can't parse such xml files
	with open(configin_name) as f:
		xml = f.read()
	con_root = ET.fromstring(re.sub(r"(<\?xml[^>]+\?>)", r"\1<root>", xml) + "</root>")
	for channels in con_root.findall('channels'):
		con_root.remove(channels)

	channels = ET.SubElement(con_root, 'channels')
	labels = ET.SubElement(channels, 'labels')
	for electrode_name in electrode_names:
		ET.SubElement(labels, 'label').text = electrode_name

	s = ET.tostring(con_root).decode('utf-8')
	s = re.sub(r"<root>", "<?xml version=\"1.0\" encoding=\"utf-8\"?>", s)
	s = re.sub(r"</root>", "", s)
	f = open(configout_name, "w")
	f.write(s)

# parse config file as ini and write new one
else:

    cp_out = CP.ConfigParser()
    cp_in = CP.ConfigParser()
    cp_in.read(configin_name)
    str = ''
    for name in electrode_names[:-1]:
        str = str + name + ', '
    str = str + electrode_names[-1]
    try:
        for section in cp_in.sections():
            if section != 'channels':
                cp_out[section] = cp_in[section]

        cp_out['channels'] = {'labels': str}
    except AttributeError:
        for section in cp_in.sections():
            if section != 'channels':
                cp_out.add_section(section)
                for option in cp_in.options(section):
                    cp_out.set(section, option, cp_in.get(section, option))
        cp_out.add_section('channels')
        cp_out.set('channels', 'labels', str)
    with open(configout_name, 'w') as configfile:
        cp_out.write(configfile)


