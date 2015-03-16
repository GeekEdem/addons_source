""" addons.xml generator """

import os
import md5

pass_dirs = ['utils']

class Generator:
	"""
		Generates a new addons.xml file from each addons addon.xml file
		and a new addons.xml.md5 hash file. Must be run from the root of
		the checked-out repo. Only handles single depth folder structure.
	"""
	def __init__( self, *args, **kwargs ):
		# generate files
		self.version = kwargs.get('version')
		print('version %s' % self.version)
		if self.version == '2.1.0':
			self.release_dir = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'zip')
		elif self.version == '2.0':
			self.release_dir = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'edem-addons')
		self.generate_addons_file()
		self.generate_md5_file()
		# notify user
		print "Finished updating addons xml and md5 files"

	def generate_addons_file( self ):
		# addon list
		addons = sorted(os.listdir( "." ))
		# final addons text
		addons_xml = u"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n"
		# loop thru and add each addons addon.xml file
		for addon in addons:
			if addon in pass_dirs:
				continue
			try:
				# skip any file or .svn folder
				if ( not os.path.isdir( addon ) or addon.startswith('.') ): continue
				# create path
				_path = os.path.join( addon, "addon.xml" )
				# split lines for stripping
				xml_lines = open( _path, "r" ).read().splitlines()
				# new addon
				addon_xml = ""
				# loop thru cleaning each line
				for line in xml_lines:
					# skip encoding format line
					if ( line.find( "<?xml" ) >= 0 ): continue
					# add line
					addon_xml += unicode( line.rstrip() + "\n", "UTF-8" )
				# we succeeded so add to our final addons.xml text
				addons_xml += addon_xml.rstrip() + "\n\n"
			except Exception, e:
				# missing or poorly formatted addon.xml
				print "Excluding %s for %s" % ( _path, e, )
		# clean and add closing tag
		addons_xml = addons_xml.strip() + u"\n</addons>\n"
		# save file
		self.save_file(addons_xml.encode("UTF-8"), file=os.path.join(self.release_dir, "addons.xml"))
		
	def generate_md5_file( self ):
		try:
			# create a new md5 hash
			m = md5.new( open( os.path.join(self.release_dir,"addons.xml") ).read() ).hexdigest()
			# save file
			self.save_file( m, file=os.path.join(self.release_dir, "addons.xml.md5") )
		except Exception, e:
			# oops
			print "An error occurred creating addons.xml.md5 file!\n%s" % ( e, )

	def save_file( self, data, file ):
		try:
			# write data to the file
			open( file, "w" ).write( data )
		except Exception, e:
			# oops
			print "An error occurred saving %s file!\n%s" % ( file, e, )

# if ( __name__ == "__main__" ):
	# start
#	Generator()