#-----------------------------------------------------------------------
# XSPIF: a (X)cross Standard PlugIn Framework
# Copyright (C) 2003 IRCAM - Centre Pompidou
# Authors: Remy Muller and Vincent Goudard
# Module xspif.tools : tools to check xspif files content.
#-----------------------------------------------------------------------
# Note to developers:
#   These tools should be STANDARD-INDEPENDANT !!!
#   Standard-specific tools should be placed in the module named after
#   the corresponding standard.
#-----------------------------------------------------------------------


import os
import string
import xml.dom.minidom
from xspif.parsexml import getText

tab = 2
T = ' '*tab

def generalCheck(domTree):
    """
    method to check the validity of the XSPIF meta-plugin with
    respect to  all constraints that are NOT handled by the DTD.
    
    """

    # Get the elements
    pluginId = getText(domTree, 'plugId')
    pluginLabel = getText(domTree, 'label')
    pluginManufId = getText(domTree, "manufId")
    pluginCaption = getText(domTree, 'caption')
    pluginComments = getText(domTree, 'comment')
    pluginMaker = getText(domTree, 'maker')
    pluginCopyright = getText(domTree, 'copyright')
    pluginCode = getText(domTree, 'code')

    pins = domTree.getElementsByTagName('pin')
    params = domTree.getElementsByTagName('param')
    states = domTree.getElementsByTagName('state')
    controlouts = domTree.getElementsByTagName('controlout')
    callbacks = domTree.getElementsByTagName('callback')
    
    process = 0
    processEvents = 0
    instantiate = 0
    deinstantiate = 0
    activate = 0
    deactivate = 0

    for cb in domTree.getElementsByTagName('callback'):
        label = getText(cb, 'label')
        if ('process' == label):
            process = cb
        elif ('processEvents' == label):
            processEvents = cb
        elif ('instantiate' == label):
            instantiate = cb
        elif ('deinstantiate' == label):
            deinstantiate = cb
        elif ('activate' == label):
            activate = cb
        elif ('deactivate' == label):
            deactivate = cb
        else:
            print(T+'Warning: callback '+label+' is not known from ladspa.py')

############################################################        

    # Check the ID:
    for Id in [pluginId, pluginManufId]:
        if (len(Id) != 6)or(Id.find("'")!=0)or(Id.rfind("'")!=5):
            print(T+ 'Warning: '+Id+': you have to specify a 32 bit label.')
            print(T+ '         you can give it as 4 characters between simple quotes.')
            return -1

    # Check every label is unique
    # Checking callback's label is unecessary because
    #  already forced by the DTD
    labels = []
    for tag in [pins, params, states, controlouts]:
        for el in tag:
            labels.append(getText(el,'label'))
    labels.append(pluginLabel)

    extraLabel = checkNotTwiceSameElement(labels)
    if (0 != extraLabel):
        print(T+"Error: label "+extraLabel+" was used more than once")
        return -1

    # Check labels do not contain bad characters
    WrongCharList = [" ","&","'",'"',"&","#","@","-","*"]
    for myString in labels:
        if ("" == myString):
            print(T+'Error: One of the labels is null!!!')
        WrongChar = stringHasChar(myString, WrongCharList)
        if (WrongChar):
            print(T+"Error: Label '"+l+"' contains bad characher '"+WrongChar+"'")
            return -1
        

    # check Min, max, and default and mapping values are OK.
    #  Warning: min, max, and mapping are here supposed to be
    #  REQUIRED by the DTD, thus we know that they exists.
    for tag in  [params, controlouts]:
        if (0 != tag.length):
            for el in tag:
                if (0 != checkMinMaxDefault(el)):
                    return -1
     
            
    if (0 == pins.length):
        print(T+"Error: The plugin you build has no audio pin!")
        return -1
    if (0 == callbacks.length):
        print(T+"Warning: The plugin you build has no callback!")
    if (0 == states.length):
        print(T+"Warning: The plugin you build has no state.")

    return


def checkNotTwiceSameElement(myList):
    """
    check that the list do not contain twice the same element
    """
    for itm in myList:
        if (myList.count(itm) > 1):
            return itm
        else:
            return 0


def stringHasChar(myString, charList):
    """
    check if myString contains characters given in charList
    If it does, it return the first occurence
    """
    for c in charList:
        if (-1 != myString.find(c)):
            print(T+"character '"+c+"' found at pos %d" % myString.find(c))
            return c
        else:
            return 0
            

def checkMinMaxDefault(el):
    """
    check that min, max, and default values are OK
    """
    label = getText(el,'label')
    min = float(getText(el,'min'))
    max = float(getText(el,'max'))
    mapping = getText(el,'mapping')
    defaultTxt = getText(el,'default')
    # protection against non-existing defaults in controlouts
    if ("" != defaultTxt):
        default = float(defaultTxt)
    else:
        default = min
        
    if float(min) >= float(max) :
        print(T+"Error: "+label+" min > max !!!")
        return 1
    elif float(default) > float(max) :
        print(T+"Error: "+label+" default > max !!!")
        return 2
    elif float(default) < float(min) :
        print(T+"Error: "+label+" default < min !!!")
        return 3
    elif((mapping=='log') and (min <= 0)):
        print(T+"Error: "+label+" negative min is not allowed with logarithmic mapping")
        return 4
    else:
        return 0
