#-----------------------------------------------------------------------
# XSPIF: a (X)cross Standard PlugIn Framework
# Copyright (C) 2003 IRCAM - Centre Pompidou
# Authors: Remy Muller and Vincent Goudard
# xspif.py : Script generating plugin source files from xspif files.
#-----------------------------------------------------------------------
#
# syntax: python xspif.py [OPTION] [FILE]   


import sys
import os
import string
import xspif
import xspif.tools
import xspif.parsexml
import xspif.vst
import xspif.au
import xspif.ladspa
import xspif.pd


help = '''
XSPIF: a Cross(X) Standard PlugIn Framework
Copyright (C) 2003 Remy Muller and Vincent Goudard
XSPIF comes with ABSOLUTELY NO WARRANTY;
This is free software, and you are welcome to redistribute it
under certain conditions. See LICENSE for more details.

XSPIF writes C/C++ source-files for differents plugin standards
from a unique description written in XML (i.e. a .xspif file)

Usage: python xspif.py [OPTION] [FILE]

Examples:
 python xspif.py vst lowpass.xspif  
 python xspif.py all lowpass.xspif 

OPTION:
  all       write the source-files for all supported standards

  vst       write the source-files for a VST plugin
  au        write the source-files for an AudioUnit plugin
  ladspa    write the source-files for a LADSPA plugin
  pd        write the source-files for a PD object 

'''

standards = ['vst','au','ladspa', 'pd']


#-----------------------------------------------------------------------
# command line arguments

if len(sys.argv)==3:
	python_filename = sys.argv[0]
	option          = sys.argv[1]
	xml_filename 	= sys.argv[2]
	plugin_prefix   = xml_filename.replace(".xspif","")
	
else :
	print help
	sys.exit("bad syntax")

#-----------------------------------------------------------------------
#

if option == 'all':
	print 'Writting sources for all standards'
elif standards.count(option) > 0:
	standards = [option]
else:
	print help
	sys.exit("option unknown")

#-------------------------------------------------------------------------
# VALIDATING THE XML FILE
print 'validating the XML file' 
xspif.parsexml.validate_xml(xml_filename)
print 'done'

#-------------------------------------------------------------------------
# PARSING THE XML FILE TO A DOM TREE
print 'parsing the XML file' 
domTree = xspif.parsexml.analyze(xml_filename)
print 'done'

#-------------------------------------------------------------------------
# ADDITIONNAL CHECK
print 'performing additionnal verifications' 
if xspif.tools.generalCheck(domTree) == -1:
	sys.exit("XSPIF ERROR: the file do not respect the xspif rules")
print 'done'


#---------------------------------------------------------------------------
# create subdirectories where the XML file is and one directory per standard

if os.access(plugin_prefix,os.F_OK):
	os.chdir(plugin_prefix)
	print 'cd '+plugin_prefix
else:
	os.mkdir(plugin_prefix)
	print 'mkdir '+plugin_prefix
	os.chdir(plugin_prefix)
	print 'cd '+plugin_prefix

for standard in standards:
	if os.access(standard,os.F_OK):
		os.chdir(standard)
		print 'cd '+standard
	else:
		os.mkdir(standard)
		print 'mkdir '+standard
		os.chdir(standard)
		print 'cd '+standard

	my_string = string.split(plugin_prefix,'/')
	plugin_prefix = my_string[len(my_string)-1]
    
	#-------------------------------------------------------------------------
	# WRITE THE SOURCE FILES

	print 'writing the source files'

	if standard == 'vst':
		xspif.vst.write(domTree,plugin_prefix)
	elif standard == 'au':
		xspif.au.write(domTree,plugin_prefix)
	elif standard == 'ladspa':
		xspif.ladspa.write(domTree,plugin_prefix)
	elif standard == 'pd':
		xspif.pd.write(domTree,plugin_prefix)
			
	print 'done'
	os.chdir(os.pardir)

# EOF #
