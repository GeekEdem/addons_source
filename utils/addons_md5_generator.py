""" .zip.md5 generator """

import os
import md5
import xml.etree.ElementTree

dir_with_script = 'utils'

class Generator:
	
	def __init__( self, *args, **kwargs ):
		# generate files
		self.version = kwargs.get('version')
		if self.version == '2.1.0':
			self.release_dir = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'zip')
		elif self.version == '2.0':
			self.release_dir = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'edem-addons')

		os.chdir(self.release_dir)
		dirs = (os.listdir('.'))
		for addon_dir in dirs:
			if(not os.path.isdir(addon_dir)):
					continue		
			if(addon_dir.startswith('.')):
					# skip hidden dirs
					continue
			self.generate_md5_file(addon_dir)

	def generate_md5_file(self, addon_dir):
		try:
			# create a new md5 hash
			addon_file = os.path.join(addon_dir, 'addon.xml')
			data = open(addon_file, 'r').read()
			node = xml.etree.ElementTree.XML(data)	
			m = md5.new( open( os.path.join(addon_dir, "addon.xml") ).read() ).hexdigest()
			# save file
			self.save_file( m, file=os.path.join(addon_dir, "%s-%s.zip.md5" % (addon_dir, node.get('version'))) )
		except Exception, e:
			# oops
			print "An error occurred creating addons.xml.md5 file!\n%s" % ( e, )

	def save_file(self, data, file):
		try:
			# write data to the file
			open( file, "w" ).write( data )
		except Exception, e:
			# oops
			print "An error occurred saving %s file!\n%s" % ( file, e, )

#if __name__ == '__main__':
#	main()
