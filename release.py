import sys
sys.path.append('utils')
import addons_xml_generator
import zip_generator
import addons_md5_generator

def make_release():
	addons_xml_generator.Generator()
	zip_generator.main()
	addons_md5_generator.main()

if __name__ == '__main__':
	make_release()
