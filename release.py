import sys, re, os
sys.path.append('utils')
import addons_xml_generator
import zip_generator
import addons_md5_generator

def make_release(version):
	os.chdir('C:\\! PLUGINS !\\addons_source')
	replace_version(version)
	addons_xml_generator.Generator(version=version)
	zip_generator.Generator(version=version)
	addons_md5_generator.Generator(version=version)

def replace_version(version):
	addons = sorted(os.listdir("."))
	for addon in addons:
		if addon == 'utils' or not os.path.isdir(addon) or addon.startswith('.'):
			continue
		elif addon == 'repository.evolution':
			pattern = ur'\/GeekEdem\/([^\/]*)\/'
			if version == '2.0':
				source = 'edem-addons'
			else:
				source = 'zip'
			repl = '/GeekEdem/%s/' % source
		else:
			pattern = ur'addon=\W*xbmc\Wpython\W*version=\W*([^"]*)"'
			repl = 'addon="xbmc.python" version="%s"' % version

		path = os.path.join(addon, "addon.xml")
		file_handle = open(path, 'r')
		file_string = file_handle.read()
		file_handle.close()
		file_string = (re.sub(pattern, repl, file_string))
		file_handle = open(path, 'w')
		file_handle.write(file_string)
		file_handle.close()
	
if __name__ == '__main__':
	make_release('2.0')
	make_release('2.1.0')
