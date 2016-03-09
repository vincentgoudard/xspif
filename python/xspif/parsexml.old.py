#-----------------------------------------------------------------------
# Vincent Goudard and Rémy Muller                                06/2003
# xspif.parsexml.py
# This function is called to parse an xml file describing a plugin
# and returns a tuple with all the information needed to build the
# plugin C/C++ source file
#-----------------------------------------------------------------------

import sys
import os
import string
import xml.dom
import xml.dom.minidom
import xml.dom.ext
# import xml.xpath
from xml.parsers.xmlproc import xmlval  # module used to validate with DTD
from xspif.xpHandlers import BadXspifPluginErrorHandler

#--------------------------------------
# routine to get an element's text value
def getTextValue(node):
    if (node != None)  :
        if node.hasChildNodes():
            for child in  node.childNodes:
                if (child.nodeName == "#text") or (child.nodeName == "#cdata-section"):
                    return child.nodeValue
                else :
                    return  ''
        else :
            return  ''
    else:
        return  ''

def validate_xml(xml_filename):

    xv = xmlval.XMLValidator()
    bh = BadXspifPluginErrorHandler(xv.app.locator)

    xv.set_error_handler(bh)
    xv.parse_resource(xml_filename)

    return


#----------------------------------------------------
# Analyse and convert the xml file into a dictionnary
def analyze(xml_filename):

    # try to open input file
    fxml = open(xml_filename,'r')

    # Get the xml document as a DOM tree
    doc =  xml.dom.minidom.parse(fxml)
    x_plugin = doc.documentElement
    return x_plugin

#########################################################

    plugin = {}

#----------------------------------------------------------------------------
# get plugin element's attributes 

    plugin['plugLabel'] = x_plugin.getAttribute("label")
    plugin['plugId']       = x_plugin.getAttribute("plugId")
    plugin['manufId']      = x_plugin.getAttribute("manufId")
    plugin['maker']        = x_plugin.getAttribute("maker")
    plugin['copyright']    = x_plugin.getAttribute("copyright")

#----------------------------------------------------------------------------
# get plugin caption

    plug_caption  = getTextValue((x_plugin.getElementsByTagName("caption")).item(0))
 
    # add it to the plugin dico
    
    plugin['plugCaption'] = plug_caption
    
#----------------------------------------------------------------------------
# get plugin comments
    x_comments = x_plugin.getElementsByTagName("comment")
    plug_comment = ""
    index = range(0, x_comments.length)
    for i in index:
        plug_comment += " " + getTextValue(x_comments.item(i))+"\n"
    # add this dico to the plugin dico
    plugin['plugComments'] = plug_comment


#----------------------------------------------------------------------------
# get includes,  independant code and routines
    plug_code = getTextValue(x_plugin.getElementsByTagName("code").item(0))
    # add this dico to the plugin dico
    plugin['plugCode'] = plug_code

#----------------------------------------------------------------------------
# get audio ports (pins)

    x_pins = x_plugin.getElementsByTagName("pin")
    if ([] != x_pins):
        pins = {}
        for p in x_pins:
            # use the pin label as key in the 'pins' dico
            pin_label = p.getAttribute("label")

            #put all these elements / attributes in a dictionnary
            pins[pin_label] = {
                'pin_channels' : p.getAttribute("channels"),
                'pin_dir'      : p.getAttribute("dir"),
                'pin_label'    : pin_label,
                'pin_caption'  : getTextValue(p.getElementsByTagName("caption").item(0)),
                'pin_comment'  : getTextValue(p.getElementsByTagName("comment").item(0))
                }

            # add this dico to the plugin dico
            plugin['pins'] = pins

#----------------------------------------------------------------------------
# get plugin's parameters
    x_params = x_plugin.getElementsByTagName("param")
    if ([] != x_params):
        params = {}
        i = 0
        for par in x_params:
            param_label = str(i) #+par.getAttribute("label")
            # put all these elements / attributes in a dictionnary
            params[param_label] = {
                'param_min'     : par.getAttribute("min"),
                'param_max'     : par.getAttribute("max"),
                'param_default' : par.getAttribute("default"),
                'param_type'    : par.getAttribute("type"),
                'param_mapping' : par.getAttribute("mapping"),
                'param_unit'    : par.getAttribute("unit"),
                'param_label'   : par.getAttribute("label"),
                'param_caption' : getTextValue(par.getElementsByTagName("caption").item(0)),
                'param_code'    : getTextValue(par.getElementsByTagName("code").item(0)),
                'param_comment' : getTextValue(par.getElementsByTagName("comment").item(0))
                }
            i += 1
        # add this dico to the plugin dico    
        plugin['params'] =  params

#----------------------------------------------------------------------------
# get plugin's states
    x_states = x_plugin.getElementsByTagName("states").item(0)

    if ([] != x_states):
        x_state = x_states.getElementsByTagName("state")

        if ([] != x_state ):
            states = {}

            for state_key in x_state:
                state_label = state_key.getAttribute("label")
                # put all these elements / attributes in a dictionnary
                states[state_label] = {
                    'state_type' : state_key.getAttribute("type"),
                    'state_label': state_label
                    }

            plugin_states = {}
            plugin_states['states'] = states
            
        # add this dico to the plugin dico
        plugin['plugin_states'] = plugin_states

#----------------------------------------------------------------------------
# get plugin's callbacks
    x_callbacks = x_plugin.getElementsByTagName("callback")
    if ([] != x_callbacks):
        callbacks = {}
        for cb in x_callbacks:
            cb_label = cb.getAttribute("label")
            callbacks[cb_label] = {

                'label' : cb.getAttribute("label"),
                'code'  : getTextValue(cb)
                }
        
        # add this dico to the plugin dico    
        plugin['callbacks'] = callbacks
 
#----------------------------------------------------------------------------
# return a dictionnary with all the information
    return(plugin)



# EOF #
