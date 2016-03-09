#-----------------------------------------------------------------------
# XSPIF: a (X)cross Standard PlugIn Framework
# Copyright (C) 2003 IRCAM - Centre Pompidou
# Authors: Remy Muller and Vincent Goudard
# Module xspif.parsexml : validate and parse a xspif file.
#-----------------------------------------------------------------------

import sys
import os
import string
import xml.dom
import xml.dom.minidom
from xml.parsers.xmlproc import xmlval  # module used to validate with DTD
from xml.parsers.xmlproc.xmlapp import ErrorHandler


class BadXspifPluginErrorHandler(ErrorHandler):
    """
    the BadXspifPluginErrorHandler gets the error(s) from the
    validating parser and output a message.
    """
    def warning(self, msg):
        print "XSPIF Warning: ", msg
    
    def error(self, msg):
        print "XSPIF Error: ", msg
	sys.exit("XSPIF ERROR: the meta-plugin does not respect XML/DTD syntax")
    
    def fatal(self, msg):
        print "XSPIF Fatal error: ", msg
	sys.exit("XSPIF ERROR: the meta-plugin does not respect XML/DTD syntax")

def getText(node, label):
    """
    routine to the text value of the attribute or sub-element 'label'
    of the node 'node'
    
    """
    if node == None:
        return ''
    else:
        Att = node.getAttributeNode(label)
        if (None != Att):
            return Att.nodeValue
        else:
            tmp = node.getElementsByTagName(label).item(0)
            if (tmp != None and node==tmp.parentNode)  :
                if tmp.hasChildNodes():
                    for child in  tmp.childNodes:
                        if (child.nodeName == "#text") or (child.nodeName == "#cdata-section"):
                            return child.nodeValue
                        else :
                            return  ''
                else :
                    return  ''
            else :
                return  ''


def validate_xml(xml_filename):
    """
    validate the xspif file WRT its DTD.
    """
    
    xv = xmlval.XMLValidator()
    bh = BadXspifPluginErrorHandler(xv.app.locator)

    xv.set_error_handler(bh)
    xv.parse_resource(xml_filename)
    return


def analyze(xml_filename):
    """
    Analyse and convert the xml file into a dictionnary.
    """
    
    # try to open input file
    fxml = open(xml_filename,'r')
    
    # Get the xml document as a DOM tree
    doc =  xml.dom.minidom.parse(fxml)
    domTree = doc.documentElement

    # return a DOM tree with all the information
    return(domTree)

# EOF #
