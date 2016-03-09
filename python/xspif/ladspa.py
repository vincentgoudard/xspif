#-----------------------------------------------------------------------
# XSPIF: a (X)cross Standard PlugIn Framework
# Copyright (C) 2003 IRCAM - Centre Pompidou
# Authors: Remy Muller and Vincent Goudard
# Module xspif.ladspa : XSPIF to LADSPA translator
#-----------------------------------------------------------------------

import sys
import os
import string
from xspif.parsexml import getText

tab = 2
T = ' '*tab

def writeGetStates(fc, states):
    if ([] != states):
        fc.write(T + "// Get the states from plugin's structure:" + '\n')
        for state_node in states:
            state_label = getText(state_node, 'label')
            state_type  = getText(state_node, 'type')
            fc.write(T + state_type + ' ' + state_label
                     + ' = plugin_data->' + state_label + ';' + '\n')
    return

def writeGetParams(fc, params):
    if ([] != params):
        fc.write(T + "// Get the params from plugin's structure:" + '\n')
        for param_node in params:
            param_caption = getText(param_node, 'caption')
            param_label = getText(param_node, 'label')
            param_type  = getText(param_node, 'type')
            fc.write(
                T+'const LADSPA_Data ' + param_label
                + ' = *(plugin_data->m_pf' + param_label +');' + '\n')
        fc.write('\n')
    return

def writeUpdateStates(fc, states):
    if ([] != states):
        fc.write(T + "// Update the states in plugin's structure:" + '\n')
        for state_node in states:
            state_label = getText(state_node, 'label')
            state_type  = getText(state_node, 'type')
            fc.write(T + 'plugin_data->' + state_label + ' = '
                     + state_label + ';' + '\n')
    return

def writeCallbackCode(fc, callback):
    if callback:
        code = getText(callback, 'code')
        label = getText(callback, 'label')
        fc.write(T + '// Code from callback <' + label
                 + '> of XSPIF meta-plugin' + '\n')
        fc.write(T + '{' + '\n')
        fc.write(code)
        fc.write('\n'+ T + '}' + '\n')
    return

def write(domTree, filenamePrefix):
    """
    This method is called by xspif2ladspa.py
    It writes the LADSPA plugin's source file [filenamePrefix].ladspa.c
    for the linux platform with the help of the DOM tree [domTree].
    """
    
    #create output file(s)
    xml_filename = (filenamePrefix + '.xspif')
    c_filename = (filenamePrefix + '.ladspa.c')
    fc = file(c_filename,'w')

    # Get the domTree direct childs
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

    # Get the callbacks by their name
    instantiate   = None
    deinstantiate = None
    process       = None
    processEvents = None
    activate      = None
    deactivate    = None
    if callbacks == [] : 
        print T+ "Warning: you haven't implemented any callback"+'\n'
    else :
        for callback in callbacks:
            text = str(getText(callback,'label'))
            if text == 'instantiate':
                instantiate = callback
            elif text == 'deinstantiate':
                deinstantiate = callback
            elif text == 'activate':
                activate = callback
            elif text == 'deactivate':
                deactivate = callback
            elif text == 'process':
                process = callback
            elif text == 'processEvents':
                print 'XSPIF Warning: callback "processEvents" not implemented for LADSPA for now'
                #processEvents = callback
            else:
                print('Warning: callback ' + text
                      +' is not known from ladspa.py' + '\n')
            
    # useful variables...
    separator = '\n' + '/****************************************************************/' + '\n'

    #----------------------------------------------------------------------------

    # make lists with ports
    # make a list with pins
    audio_ports = []
    for pin_node in pins:
        pin_label = getText(pin_node, 'label')
        pin_channels = int(getText(pin_node, 'channels'))
        pin_dir = getText(pin_node, 'dir')
        pin_caption = getText(pin_node, 'caption')
        for i in range(1, pin_channels + 1):
            audio_ports.append([pin_label + str(i), pin_dir, pin_caption])
            
    # make a list with params
    param_ports = []
    for p_node in params:
        p_label = getText(p_node, 'label')
        p_caption = getText(p_node, 'caption')
        p_type = getText(p_node, 'type')
        param_ports.append([p_label, 'param', p_caption, p_type])
    
    # make a list with controlouts
    controlout_ports = []
    for c_node in controlouts:
        c_label = getText(c_node, 'label')
        c_caption = getText(c_node, 'caption')
        c_type = getText(c_node, 'type')
        controlout_ports.append([c_label, 'controlout', c_caption, c_type])

    # make a list with all ports
    ports = audio_ports + param_ports + controlout_ports
    
    #----------------------------------------------------------------------------
    # file header

    fc.write(
        '/****************************************************************' + '\n'
        + 'XSPIF: cross(X) Standard PlugIn Framework: '
        + 'XSPIF to LADSPA' + '\n'
        + T+c_filename+'\n' + '\n'
        + pluginComments
        + ' This file is generated automatically from the file: '+xml_filename+'\n'
        + T+'plugin ID: '+pluginId+'\n'
        + T+'manufacturer ID: '+pluginManufId+'\n'
        + T+'maker: '+pluginMaker+'\n'
        + T+'copyright: '+pluginCopyright+'\n'
        + '****************************************************************/' + '\n'
        + '\n' + '\n' + '\n'
        )

    #----------------------------------------------------------------------------
    # includes and independant code
    fc.write('#include <stdlib.h>' + '\n'
             + '#include <string.h>' + '\n'
             + '#include "ladspa.h"' + '\n'+ '\n'
             )
    # macros
    fc.write('\n' + '\n' + separator)
    fc.write('// Macro for getting the sample rate' + '\n')
    fc.write('#undef XSPIF_GET_SAMPLE_RATE'+ '\n'
             '#define XSPIF_GET_SAMPLE_RATE() (plugin_data->sample_rate)'+ '\n')
    
    fc.write('// Macro for getting the vector_size' + '\n')
    fc.write('#undef XSPIF_GET_VECTOR_SIZE'+ '\n'
             '#define XSPIF_GET_VECTOR_SIZE() (sample_count)'+ '\n')

    if ([] != controlouts):
        fc.write('// Macro for control output' + '\n')
        fc.write('#undef XSPIF_CONTROLOUT'+ '\n'
                 '#define XSPIF_CONTROLOUT(dest, index, source)'
                 + '(*(dest) = (LADSPA_DATA(source)))'+ '\n')

    
    fc.write('\n' + '\n' + separator)
    fc.write(pluginCode + '\n')
    
    
    #----------------------------------------------------------------------------
    # Port declaration
    
    # write ports declaration in the c file
    fc.write('\n' + '\n' + separator)
    fc.write('/* Audio and parameters ports */' + '\n')
    for port in ports:
        fc.write('#define PORT_' + port[0].upper() + T * 2 + str(ports.index(port)) + '\n')
        
       
    #---------------------------------------------------
    # LADSPA DESCRIPTOR
    #---------------------------------------------------
    fc.write('\n' + '\n' + separator)
    fc.write('static LADSPA_Descriptor *'
             + pluginLabel.lower()
             + 'Descriptor = NULL;' + '\n')

    #---------------------------------------------------
    # The plugin structure contains ...
    #---------------------------------------------------
    fc.write('\n' + '\n' + separator)
    fc.write('// The plugin structure '+ '\n')
    fc.write('typedef struct {' + '\n' + '\n')

    # the sample rate
    fc.write(T + 'LADSPA_Data sample_rate;' + '\n')
    
    # ...the pointers for the ports ...
    fc.write(T + '// Pointers to the ports:\n')
    for port in ports:
              fc.write(T + 'LADSPA_Data *m_pf' + port[0] + ';' + '\n')
    fc.write('\n')
    
    # ...a copy of the parameter and its last value for local use...
    fc.write(T + '// Internal copy of the parameters and its last value:\n')
    for port in param_ports:
        fc.write(T + port[3] + ' ' + port[0] + ';' + '\n')
        fc.write(T + port[3] + ' _last_' + port[0] + ';' + '\n')
    fc.write('\n')
        
    # ... and the states ...(except the code_states declared as global)
    fc.write(T + '// Internal states:\n')
    if ([] != states):
        for state_node in states:
            state_label = getText(state_node, 'label')
            state_type  = getText(state_node, 'type')
            fc.write(T + state_type + ' ' + state_label + ';' + '\n')

    # run adding gain
    fc.write(T + 'LADSPA_Data run_adding_gain;' + '\n')

    fc.write('}' + pluginLabel + ';' + '\n')

 
    #----------------------------------------------------------------------------
    # Plugin descriptor
    # TODO: handle case with multiple plugs in a dll with a 'for' loop
    #----------------------------------------------------------------------------
    fc.write('\n' + '\n' + separator)
    fc.write(
        'const LADSPA_Descriptor *ladspa_descriptor(unsigned long index) {' + '\n' * 2
        + T + 'switch (index) {' + '\n'
        + T + 'case 0:' + '\n'
        + T * 2 + 'return ' + pluginLabel.lower() + 'Descriptor;' + '\n'
        + T + 'default:' + '\n'
        + T * 2 + 'return NULL;' + '\n'
        + T + '}' + '\n' + '}' + '\n'
        )
         
    #---------------------------------------------------------------------------
    #  Plugin activate function
    #---------------------------------------------------------------------------
    if (activate):
        activate_code = getText(activate, 'code')
        fc.write('\n' + '\n' + separator)
        fc.write('// Initialise and activate a plugin instance.'+ '\n')
        fc.write(
            'static void activate' + pluginLabel + '(LADSPA_Handle instance) {'
            + '\n' * 2
            + T + pluginLabel + ' *plugin_data = (' + pluginLabel +'*)instance;' + '\n')
        
        writeGetStates(fc, states)
        writeGetParams(fc, params)
        writeCallbackCode(fc, activate)
        writeUpdateStates(fc, states)
        
        fc.write('\n' + '}' + '\n')
        

    #---------------------------------------------------------------------------
    #  Plugin deactivate function
    #---------------------------------------------------------------------------
    if (deactivate):
        deactivate_code = getText(deactivate, 'code')
        fc.write('\n' + '\n' + separator)
        fc.write('// Deactivate a plugin instance.'+ '\n')
        fc.write(
            'static void deactivate' + pluginLabel + '(LADSPA_Handle instance) {' + '\n' * 2
            + T + pluginLabel + ' *plugin_data = (' + pluginLabel +'*)instance;' + '\n')
        
        writeGetStates(fc, states)
        writeGetParams(fc, params)
        writeCallbackCode(fc, deactivate)
        writeUpdateStates(fc, states)

        fc.write('\n' + '}' + '\n')

    #----------------------------------------------------------------------------
    # Plugin cleanup function (=deinstantiate)
    #----------------------------------------------------------------------------
    fc.write('\n' + '\n' + separator)
    fc.write('/* Cleanup is the "de-instantiate" function.' + '\n'
             + 'Free the memory allocated in "instantiate" in this function */' + '\n')
    fc.write(
        'static void cleanup' + pluginLabel + '(LADSPA_Handle instance) {' + '\n' * 2
        + T + pluginLabel + '* plugin_data = (' + pluginLabel + '*)instance;' + '\n'
        )
    
    
    # If deinstantiate is implemented in the meta-plugin
    # Get the states, so that any structure can be deleted fom memory:
    if (deinstantiate):
        writeGetStates(fc, states)
        writeGetParams(fc, params)
        writeCallbackCode(fc, deinstantiate)

    fc.write(T + 'free(instance);'+ '\n' + '}' + '\n')
    

    #----------------------------------------------------------------------------
    # Plugin connect function
    #----------------------------------------------------------------------------
    fc.write('\n' + '\n' + separator)
    head =  'static void connectPort' + pluginLabel + '('
    fc.write(
        head + ' LADSPA_Handle instance,' + '\n'
        + ' ' * len(head) + ' unsigned long port,' + '\n'
        + ' ' * len(head) + ' LADSPA_Data *data) {' + '\n' * 2
        + T + pluginLabel + ' *plugin;' + '\n' + '\n'
        + T + 'plugin = (' + pluginLabel + ' *)instance;' + '\n'
        + T + 'switch (port) {' + '\n'
        )

     
    for port in ports:
        fc.write(T + 'case PORT_' + port[0].upper() + ':' + '\n'
                 +T* 2 + 'plugin->m_pf' + port[0] + ' = data;' + '\n'
                 +T* 2 + 'break;'+ '\n')
        
    fc.write(T + '}' + '\n' + '}' + '\n')
    

            
    #----------------------------------------------------------------------------
    # Instantiate function
    #----------------------------------------------------------------------------
    head = 'static LADSPA_Handle instantiate' + pluginLabel + '('
    fc.write('\n' + '\n' + separator)
    fc.write(
        head + ' const LADSPA_Descriptor *descriptor,' + '\n'
        + ' ' * len(head) + ' unsigned long s_rate) {' + '\n' * 2
        + T + pluginLabel + ' *plugin_data = (' + pluginLabel
        +' *)malloc(sizeof(' + pluginLabel +'));' + '\n'*2
        )
    
    if (instantiate):
        fc.write(T + '// States:' + '\n')
        if ([] != states):
            for state_node in states:
                state_label = getText(state_node, 'label')
                state_type  = getText(state_node, 'type')
                fc.write(T + state_type + ' ' + state_label + ';' + '\n')

  #    fc.write(T + 'if (plugin_data) {'+ '\n')
    fc.write(T  * 2 + 'plugin_data->sample_rate =(LADSPA_Data)s_rate;' + '\n')


    if (instantiate):
        writeCallbackCode(fc, instantiate)
        writeUpdateStates(fc, states)
       
    fc.write('\n' + T + 'return (LADSPA_Handle)plugin_data;'+ '\n'
             + '}' + '\n')

    #----------------------------------------------------------------------------
    # Define once the XSPIF_WRITE_SAMPLE macro for 'run-replacing' process
    #----------------------------------------------------------------------------
    fc.write('\n' + '\n' + separator)
    fc.write('// Macro for run-replacing processing' + '\n')
    fc.write('#undef XSPIF_WRITE_SAMPLE'+ '\n'
             '#define XSPIF_WRITE_SAMPLE(dest, index, source) ((dest)[(index)] = (source))'+ '\n'
             )

   
    #----------------------------------------------------------------------------
    # Run (process) function
    #----------------------------------------------------------------------------
    head = 'static void run'+ pluginLabel+ '('
    fc.write('\n' + '\n' + separator)
    fc.write(
        head + 'LADSPA_Handle instance,' + '\n'
        + ' ' * len(head) + 'unsigned long sample_count) {' + '\n' * 2
        + T + pluginLabel + ' *plugin_data = ('  + pluginLabel + '*)instance;' + '\n' + '\n')
    
    # get the parameters new and last values
    for param_node in params:
        param_caption = getText(param_node, 'caption')
        param_label = getText(param_node, 'label')
        param_type  = getText(param_node, 'type')
        fc.write(
            T + '/*'+ param_caption + '*/'+ '\n'
            + T+'const LADSPA_Data ' + param_label
            + ' = *(plugin_data->m_pf' + param_label +');' + '\n')
        fc.write(
            T + param_type + ' _last_' + param_label
            + ' = plugin_data->_last_' + param_label + ';' + '\n')
    fc.write('\n')
       
    for port in audio_ports:
        if port[1] == 'In':
            fc.write(T + '/* Audio input: '+ port[0] + '*/'+ '\n')
            fc.write(T + 'const LADSPA_Data * const ' + port[0])
        elif port[1] == 'Out':
            fc.write(T + '/* Audio output: '+ port[0] + '*/'+ '\n')
            fc.write(T+'LADSPA_Data * const ' + port[0])
        fc.write(' = plugin_data->m_pf' + port[0] +';' + '\n' + '\n')

    for port in controlout_ports:
        fc.write(T + '/* Control output: '+ port[1] + '*/'+ '\n')
        fc.write(T+'LADSPA_Data * ' + port[0]
                 + ' = plugin_data->m_pf' + port[0] +';' + '\n' + '\n')

    # ...the states...
    writeGetStates(fc, states)

    # check if param changed and perform necessary conversions if any:
    fc.write('\n')
    fc.write(T + '// Check if param changed and perform necessary conversions if any:' + '\n')
    for param_node in params:
        param_label = getText(param_node, 'label')
        fc.write(T + 'if ('+ param_label + ' != _last_' + param_label +') {'
                 + '\n')
        param_code = getText(param_node, 'code')
        if ('' != param_code):
            fc.write(param_code + '\n')    
        fc.write(T * 2 + 'plugin_data->_last_' + param_label
                 + ' = ' + param_label +';' + '\n'
                 + T + '}' + '\n')

    fc.write('\n')
    # here is the DSP algorithm
    writeCallbackCode(fc, process)

    # Update the states in the plugin structure
    writeUpdateStates(fc, states)

    fc.write('}' + '\n')
    
    #----------------------------------------------------------------------------
    # Re- define then the XSPIF_WRITE_SAMPLE macro for 'run-adding' process
    #----------------------------------------------------------------------------
    fc.write('\n' + '\n' + separator)
    fc.write('// Macro for run-adding processing' + '\n')
    fc.write('#undef XSPIF_WRITE_SAMPLE'+ '\n'
             '#define XSPIF_WRITE_SAMPLE(dest, index, source) ((dest)[(index)] += (source))'+ '\n'
             )

    #----------------------------------------------------------------------------
    # setRunAddinGain function
    #----------------------------------------------------------------------------
    fc.write('\n' + '\n' + separator)
    fc.write('static void setRunAddingGain' + pluginLabel + '(LADSPA_Handle instance,' + '\n'
             + T * 3 +'LADSPA_Data gain) {' + '\n' * 2
             + T + '((' + pluginLabel + '*)instance)->run_adding_gain = gain;' + '\n'
             + '}' + '\n'
             )

    #----------------------------------------------------------------------------
    # Run_adding (process with accumulation) function
    #----------------------------------------------------------------------------
    fc.write('\n' + '\n' + separator)
    fc.write(
        'static void runAdding' + pluginLabel
        + '(LADSPA_Handle instance, unsigned long sample_count) {' + '\n' * 2
        + T + pluginLabel + ' *plugin_data = ('  + pluginLabel + '*)instance;' + '\n'
        + T + 'LADSPA_Data run_adding_gain = plugin_data->run_adding_gain;'  + '\n' + '\n'
        )

   # get the parameters new and last values
    for param_node in params:
        param_caption = getText(param_node, 'caption')
        param_label = getText(param_node, 'label')
        param_type  = getText(param_node, 'type')
        fc.write(
            T + '/*'+ param_caption + '*/'+ '\n'
            + T+'const LADSPA_Data ' + param_label
            + ' = *(plugin_data->m_pf' + param_label +');' + '\n')
        fc.write(
            T + param_type + ' _last_' + param_label
            + ' = plugin_data->_last_' + param_label + ';' + '\n')
    fc.write('\n')
       
    for port in audio_ports:
        fc.write(T + '/* Audio input: '+ port[0] + '*/'+ '\n')
        if port[1] == 'In':
            fc.write(T + 'const LADSPA_Data * const ' + port[0])
        elif port[1] == 'Out':
            fc.write(T+'LADSPA_Data * const ' + port[0])
        fc.write(' = plugin_data->m_pf' + port[0] +';' + '\n' + '\n')

    for port in controlout_ports:
        fc.write(T + '/* Control output: '+ port[1] + '*/'+ '\n')
        fc.write(T+'LADSPA_Data * ' + port[0]
                 + ' = plugin_data->m_pf' + port[0] +';' + '\n' + '\n')

    # ...the states...
    writeGetStates(fc, states)
    
    # check if param changed and perform necessary conversions if any:
    fc.write('\n')
    fc.write(T + '// Check if param changed and perform necessary conversions if any:' + '\n')
    for param_node in params:
        param_label = getText(param_node, 'label')
        fc.write(T + 'if ('+ param_label + ' != _last_' + param_label +') {'
                 + '\n')
        param_code = getText(param_node, 'code')
        if ('' != param_code):
            fc.write(param_code + '\n')    
        fc.write(T * 2 + 'plugin_data->_last_' + param_label
                 + ' = ' + param_label +';' + '\n'
                 + T + '}' + '\n')
    fc.write('\n')
    
    # here is the DSP algorithm
    writeCallbackCode(fc, process)
    
    # Update the states in the plugin structure
    writeUpdateStates(fc, states)

    fc.write('}' + '\n')
    
    #----------------------------------------------------------------------------
    # Init function
    #----------------------------------------------------------------------------
    
    # define shortcuts
    pD = pluginLabel.lower() + 'Descriptor'

    fc.write('\n' + '\n' + separator)
    fc.write('/* _init() is called automatically when the plugin library is first loaded. */' + '\n')
    fc.write(
        'void _init() {' + '\n' * 2
        + T + 'char **port_names;' + '\n'
        + T + 'LADSPA_PortDescriptor *port_descriptors;' + '\n'
        + T + 'LADSPA_PortRangeHint *port_range_hints;' + '\n' + '\n'
        + T + pD + ' = ' + '\n'
        + T + '  (LADSPA_Descriptor *)malloc(sizeof(LADSPA_Descriptor));' + '\n' + '\n'

        + T + 'if (' + pD + ') {' + '\n'
        + T * 2 + pD + '->UniqueID = ' + pluginId + ';'  + '\n'
        + T * 2 + pD + '->Label = strdup("' + pluginLabel +'");' +'\n'
        + T * 2 + pD + '->Name = strdup("' + pluginCaption +'");' +'\n'
        + T * 2 + pD + '->Maker = strdup("' + pluginMaker +'");' +'\n'
        + T * 2 + pD + '->Copyright = strdup("' + pluginCopyright +'");' +'\n'
        + T * 2 + pD + '->PortCount = ' + str(len(ports)) + ';' +'\n' 
        + '\n'
        + T * 2 + 'port_descriptors = (LADSPA_PortDescriptor *)calloc(' + str(len(ports)) + ',' +'\n'
        + T * 2 + ' sizeof(LADSPA_PortDescriptor));' +'\n'
        + T * 2 + pD + '->PortDescriptors =' + '\n'
        + T * 2 + '(const LADSPA_PortDescriptor *)port_descriptors;' +'\n'
        + '\n'
        + T * 2 + 'port_range_hints = (LADSPA_PortRangeHint *)calloc(' + str(len(ports)) + ',' +'\n'
        + T * 2 + ' sizeof(LADSPA_PortRangeHint));' +'\n'
        + T * 2 + pD + '->PortRangeHints =' + '\n'
        + T * 2 + ' (const LADSPA_PortRangeHint *)port_range_hints;' +'\n'
        + '\n'
        + T * 2 + 'port_names = (char **)calloc(' + str(len(ports)) + ', sizeof(char*));' +'\n'
        + T * 2 + pD + '->PortNames =' + '\n'
        + T * 2 + ' (const char **)port_names;' + '\n'
        + '\n'
        )

    # Write descriptors for input parameters (TODO: ouput parameters in xml)
    control_nodes = params + controlouts
    for cp_node in control_nodes:
        pl = 'PORT_'+ getText(cp_node, 'label').upper()  # shortcut
        fc.write(
            T * 2 + '/* Parameters for '  + getText(cp_node, 'caption') +' */' + '\n'
            + T * 2 + 'port_descriptors['+ pl + '] =' + '\n')
        if ('param'==cp_node.nodeName):
            fc.write(T*2+' LADSPA_PORT_INPUT | LADSPA_PORT_CONTROL;' + '\n')
        elif ('controlout'==cp_node.nodeName):
            fc.write(T*2+' LADSPA_PORT_OUTPUT | LADSPA_PORT_CONTROL;' + '\n')
        fc.write(
            T * 2 + 'port_names[' + pl + '] =' + '\n'
            + T * 2 + ' strdup("' +  getText(cp_node, 'caption') + '");' + '\n'
            + T * 2 + 'port_range_hints[' + pl + '].HintDescriptor =' + '\n'
            + T * 2
            )

        cp_hint = 0  # for these ' | ' sake!!
        cp_min =  getText(cp_node, 'min').replace('f', '', 1)
        cp_max =  getText(cp_node, 'max').replace('f', '', 1)
        cp_default = getText(cp_node, 'default').replace('f', '', 1)

        if ('' != cp_min):
            fc.write(' LADSPA_HINT_BOUNDED_BELOW')            
            cp_hint = 1

        if ('' != cp_max):
            if (1 == cp_hint): fc.write(' | LADSPA_HINT_BOUNDED_ABOVE')
            else:
                fc.write(' LADSPA_HINT_BOUNDED_ABOVE')
                cp_hint = 1
               
        if ('' != cp_default): # TODO: add default_low and default_high
            if float(cp_default) <= float(cp_min):
                if (1 == cp_hint): fc.write(' | LADSPA_HINT_DEFAULT_MINIMUM')
                else:
                    fc.write(' LADSPA_HINT_DEFAULT_MINIMUM')
                    cp_hint = 1
                     
            elif float(cp_default) >= float(cp_max):
                if (1 == cp_hint): fc.write(' | LADSPA_HINT_DEFAULT_MAXIMUM')
                else:
                    fc.write(' LADSPA_HINT_DEFAULT_MAXIMUM')
                    cp_hint = 1
            else: # if default is neither 'min' nor 'max', let it be middle range
                if (1 == cp_hint):
                    fc.write(' | LADSPA_HINT_DEFAULT_MIDDLE')
                else:
                    fc.write(' LADSPA_HINT_DEFAULT_MIDDLE')
        else:
            if (1 == cp_hint): fc.write(' | LADSPA_HINT_DEFAULT_NONE')
            else:
                fc.write(' LADSPA_HINT_DEFAULT_NONE')
                cp_hint = 1

        if ('log' == getText(cp_node, 'mapping')):
            if (1 == cp_hint): fc.write(' | LADSPA_HINT_LOGARITHMIC')
            else:
                fc.write(' LADSPA_HINT_LOGARITHMIC')
                cp_hint = 1

        if ('int' == getText(cp_node, 'type')):
            if (1 == cp_hint): fc.write(' | LADSPA_HINT_INTEGER')
            else:
                fc.write(' LADSPA_HINT_INTEGER')
                cp_hint = 1
        fc.write(';' + '\n')

        if ('' != cp_min):
            fc.write(
                T * 2 + 'port_range_hints[' + pl + '].LowerBound = ' + cp_min + ';' + '\n'
                )
        if ('' != cp_max):
            fc.write(
                T * 2 + 'port_range_hints[' + pl + '].UpperBound = ' + cp_max + ';' + '\n'
                )
        fc.write('\n' * 2)


    # Write descriptors for audio pins
    for port in audio_ports:
        fc.write(
            T * 2  + '/* Parameters for PORT_' + port[0] + ' */'+ '\n'
            + T * 2  + 'port_descriptors[PORT_' + port[0].upper() + '] =' + '\n'
            )
        if 'In'== port[1]:
            fc.write(T * 2  + ' LADSPA_PORT_INPUT | LADSPA_PORT_AUDIO;' + '\n')
        elif 'Out'== port[1]:
            fc.write(T * 2  + ' LADSPA_PORT_OUTPUT | LADSPA_PORT_AUDIO;' + '\n')

        fc.write(
            T * 2  + 'port_names[PORT_' + port[0].upper() +'] =' + '\n'
            + T * 2  + ' strdup("' + port[2] + '");' + '\n'
            + T * 2  + 'port_range_hints[PORT_' + port[0].upper() + '].HintDescriptor = 0;'
            + '\n' + '\n'
            )

    # Declare the methods
    if (instantiate):
        fc.write(T * 2  + pD + '->instantiate = instantiate' + pluginLabel + ';' + '\n')
    else:
        fc.write(T * 2  + pD + '->instantiate = NULL;' + '\n')
    if (deinstantiate):
        fc.write(T * 2  + pD + '->cleanup = cleanup' + pluginLabel + ';' + '\n')
    else:
        fc.write(T * 2  + pD + '->cleanup = NULL;' + '\n')
    if (activate):
        fc.write(T * 2  + pD + '->activate = activate' + pluginLabel + ';' + '\n')
    else:
        fc.write(T * 2  + pD + '->activate = NULL;' + '\n')
    if (deactivate):
        fc.write(T * 2  + pD + '->deactivate = deactivate' + pluginLabel + ';' + '\n')
    else:
        fc.write(T * 2  + pD + '->deactivate = NULL;' + '\n')
    fc.write(
        T * 2  + pD + '->connect_port = connectPort'+ pluginLabel + ';' + '\n'
        + T * 2  + pD + '->run = run' + pluginLabel + ';' + '\n'
        + T * 2  + pD + '->run_adding = runAdding' + pluginLabel + ';' + '\n'
        + T * 2  + pD + '->set_run_adding_gain = setRunAddingGain' + pluginLabel + ';' + '\n'
        )

    fc.write(T + '}' + '\n' + '}' + '\n')



    #----------------------------------------------------------------------------
    # fini
    #----------------------------------------------------------------------------
    fc.write('\n' + '\n' + separator)
    fc.write('/* _fini() is called automatically when the library is unloaded. */' + '\n')
    fc.write('void _fini() {' + '\n' * 2
             + ' \t' * 1 + 'int i;'  + '\n'
             + ' \t' * 1 + 'if (' + pD + ') {' + '\n'
             + ' \t' * 2 + 'free((char *)' + pD + '->Label);' + '\n'
             + ' \t' * 2 + 'free((char *)' + pD + '->Name);' + '\n'
             + ' \t' * 2 + 'free((char *)' + pD + '->Maker);' + '\n'
             + ' \t' * 2 + 'free((char *)' + pD + '->Copyright);' + '\n'
             + ' \t' * 2 + 'free((LADSPA_PortDescriptor *)' + pD + '->PortDescriptors);' + '\n'
             + ' \t' * 2 + 'for (i = 0; i < ' + pD + '->PortCount; i++)' + '\n'
             + ' \t' * 3 + 'free((char *)(' + pD + '->PortNames[i]));' + '\n'
             + ' \t' * 2 + 'free((char **)' + pD + '->PortNames);' + '\n'
             + ' \t' * 2 + 'free((LADSPA_PortRangeHint *)' + pD + '->PortRangeHints);' + '\n'
             + ' \t' * 2 + 'free(' + pD + ');'+ '\n'
             + ' \t' * 1 +  '}' + '\n'
             )


    fc.write('}' + '\n')

    #----------------------------------------------------------------------------
    # close file
    fc.close
    print T+'done'



    #---------------------------------------------------------------------------
    # MAKFILE
    #---------------------------------------------------------------------------

    print T+'writing : Makefile'
    fm = file('Makefile','w')

    fm.write('''
###############################################################################
# XSPIF: cross(X) Standard PlugIn Framework:
# This makefile is generated automatically by the module "ladspa.py"
# and from the file: '''+xml_filename+'''
#

###############################################################################
# INSTALLATION DIRECTORIES
#
# Change these if you want to install somewhere else. In particularly
# you may wish to remove the middle "local/" part of each entry.


INSTALL_PLUGINS_DIR	=	/usr/local/lib/ladspa/
INSTALL_INCLUDE_DIR	=	/usr/include/
#INSTALL_BINARY_DIR	=	/usr/local/bin/

###############################################################################
#
# GENERAL
#

NAME		=       '''+filenamePrefix+'''
INCLUDES	=	-I$(LADSPA_PATH) -I. -I..
LIBRARIES	=	-ldl -lm
CFLAGS		=	$(INCLUDES) -DPD -O3 -Wall -funroll-loops -fPIC -Wno-unused -Wno-parentheses -Wno-switch
CXXFLAGS	=	$(CFLAGS)
SRC		=	$(NAME).ladspa.c
OBJ		=	$(NAME).ladspa.o
PLUGIN		=	$(NAME).ladspa.so
CC		=	cc
CPP		=	c++

###############################################################################
#
# RULES TO BUILD PLUGINS FROM C OR C++ CODE
#
$(PLUGIN):	$(OBJ)
	$(LD) -o $(PLUGIN) $(OBJ) -shared

$(OBJ):	$(SRC)
	$(CC) $(CFLAGS) -o $(OBJ) -c $(SRC)


# For now, all LADSPA plugins generated with XSPIF are in C
# $(PLUGIN):	$(SRC) $(OBJ) ladspa.h
# 	$(CPP) $(CXXFLAGS) -o $*.o -c $*.cpp
# 	$(CPP) -o $*.ladspa.so $*.ladspa.o -shared

###############################################################################
#
# TARGETS
#

install:	$(PLUGIN)
	cp      $(PLUGIN) $(LADSPA_PATH)

targets:	$(PLUGIN)

###############################################################################
#
# UTILITIES
#

clean:
	-rm -f `find . -name "*.o"`
	-rm -f `find .. -name "*~"`
	-rm -f `find .. -name "core*"`

###############################################################################

''')

    fm.close
    print T+'done'
  
    return
# ------------- (E.O.F.)--------------------
