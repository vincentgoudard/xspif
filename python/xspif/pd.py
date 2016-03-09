#-----------------------------------------------------------------------
# XSPIF: a (X)cross Standard PlugIn Framework
# Copyright (C) 2003 IRCAM - Centre Pompidou
# Authors: Remy Muller and Vincent Goudard
# Module xspif.pd : XSPIF to PD (PureData) translator
#-----------------------------------------------------------------------

import sys
import os
import string
from xspif.parsexml import getText

tab = 2
T = ' '*tab

def writeGetStates(fc, states):
    if ([] != states):
        fc.write('\n')
        fc.write(T + "// Get the states from plugin's structure:" + '\n')
        for s_node in states:
            s_label = getText(s_node, 'label')
            s_type  = getText(s_node, 'type')
            fc.write(T + s_type + ' ' + s_label
                     + ' = x->' + s_label + ';' + '\n')
    return

def writeGetParams(fc, params):
    if ([] != params):
        fc.write('\n')
        fc.write(T + "// Get the params from plugin's structure:" + '\n')
        for p_node in params:
            p_label = getText(p_node, 'label')
            p_type  = getText(p_node, 'type')
            fc.write(T +p_type + ' ' + p_label
                     +' = x->m_f'+p_label+';' + '\n')
    return

def writeUpdateStates(fc, states):
    if ([] != states):
        fc.write('\n')
        fc.write(T + "// Update the states in plugin's structure:" + '\n')
        for s_node in states:
            s_label = getText(s_node, 'label')
            s_type  = getText(s_node, 'type')
            fc.write(T + 'x->' + s_label + ' = '
                     + s_label + ';' + '\n')
    return

def writeGetControlouts(fc, controlouts):
    if ([] != controlouts):
        fc.write('\n')
        fc.write(T + "// Get the pointers to the outlets:" + '\n')
        for c_node in controlouts:
            c_label = getText(c_node, 'label')
            c_type  = getText(c_node, 'type')
            fc.write(T + 't_outlet *' + c_label
                     + ' = x->' + c_label + ';' + '\n')
            fc.write('\n')
    return

def writeCallbackCode(fc, callback):
    if callback:
        code = getText(callback, 'code')
        label = getText(callback, 'label')
        fc.write('\n')
        fc.write(T + '// Code from callback <' + label
                 + '> of XSPIF meta-plugin' + '\n')
        fc.write(T + '{' + '\n')
        fc.write(code)
        fc.write('\n'+T+ '}' + '\n')
    return

def write(domTree, filenamePrefix):
    """
    This method is called by xspif2pd_linux.py
    It writes the PureData object's source file [filenamePrefix].pd_linux.c
    for the linux platform with the help of the DOM tree [x_plugin].
    """
   
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
                print 'XSPIF Warning: callback "processEvents" not implemented for PD for now'
                #processEvents = callback
            else:
                print('Warning: callback ' + text
                      +' is not known from pd.py' + '\n')
            
    # useful variables...
    separator = '\n' + '/****************************************************************/' + '\n'
    pluginLabelTilde =  pluginLabel + '_tilde'
    t_pluginLabel = 't_' + pluginLabelTilde

    # make a list with pins
    in_ports = []
    out_ports = []
    for pin_node in pins:
        pin_label = getText(pin_node, 'label')
        pin_channels = int(getText(pin_node, 'channels'))
        pin_dir = getText(pin_node, 'dir')
        pin_caption = getText(pin_node, 'pin_caption')
        for i in range(1, pin_channels + 1):
            if ('In' == pin_dir):
                in_ports.append([pin_label + str(i), pin_caption])
            elif ('Out' == pin_dir):
                out_ports.append([pin_label + str(i), pin_caption])

    # ports clockwise sorted W.R.T. the graphical representation of the object.
    out_ports.reverse()
    out_ports_cw = out_ports[:]
    out_ports.reverse()
    ports_cw = in_ports + out_ports_cw
   
    #create output file(s)
    xspif_filename = (filenamePrefix + '.xspif')
    c_filename = (pluginLabel + '~.c')
    print T+'writing : '+c_filename
    fc = file(c_filename,'w')


    #----------------------------------------------------------------------------
    # file header

    fc.write(
        '/****************************************************************' + '\n'
        + 'XSPIF: cross(X) Standard PlugIn Framework: '
        + 'XSPIF to PD' + '\n'
        + T+ c_filename+'\n' + '\n'
        + pluginComments + '\n'
        + ' This file is generated automatically from the file: '+xspif_filename+'\n'
        + T+'plugin ID: '+pluginId+'\n'
        + T+'manufacturer ID: '+pluginManufId+'\n'
        + T+'maker: '+pluginMaker+'\n'
        + T+'copyright: '+pluginCopyright+'\n'
        + '****************************************************************/' + '\n'
        + '\n' + '\n' + '\n')


    #----------------------------------------------------------------------------
    # includes

    fc.write('#include <stdlib.h>'+'\n'
             +'#include <string.h>'+'\n'
             +'#ifndef PD_VERSION'+'\n'
             +'#include "m_pd.h"'+'\n'
             +'#endif'+'\n')


    #----------------------------------------------------------------------------
    # macros

    fc.write('\n' + '\n' + separator)
    fc.write('''
// Macro for getting the sample rate
#undef XSPIF_GET_SAMPLE_RATE
#define XSPIF_GET_SAMPLE_RATE()(sys_getsr())

// Macro for getting the vector_size
#undef XSPIF_GET_VECTOR_SIZE
#define XSPIF_GET_VECTOR_SIZE()(vector_size)

// Macro for control outputs
#undef XSPIF_CONTROLOUT
#define XSPIF_CONTROLOUT(dest, index, value)(outlet_float(dest, value))

// Macros for checking parameter fit in its range
#undef FIT_RANGE
#define FIT_RANGE(value, min, max)(((value) < min) ? min : (((value) > max) ? max : (value)))
''')

    
    #----------------------------------------------------------------------------
    # independant routines
    fc.write('\n' + '\n' + separator)
    fc.write('// add independant code here' + '\n')
    fc.write(pluginCode)


    #----------------------------------------------------------------------------
    # Class declaration

    fc.write('\n' + '\n' + separator)
    fc.write('static t_class *' + pluginLabelTilde + '_class;' + '\n')
    fc.write('\n')

    # ...a t_object as first entry!! ...
    fc.write('typedef struct _' + pluginLabelTilde + ' {' + '\n'
             + T + 't_object  x_obj;' + '\n')
    
    # ...the sample rate ...
    fc.write(T + 't_float sample_rate;' + '\n'
             + T + 't_int active;' + '\n')

    fc.write('\n')
        
    # ...a copy of the parameter for local use...
    # Note: don't care about type: all numbers are float in a PD graph
    fc.write(T + '// Internal copy of the parameters:\n')
    for p_node in params:
        p_label = getText(p_node, 'label')
        p_type  = getText(p_node, 'type')
        fc.write(T + 't_float m_f' + p_label + ';' + '\n')
    fc.write('\n')

    # ... the states ...(except the code_states declared as global)
    fc.write(T + '// Internal states:\n')
    if ([] != states):
        for s_node in states:
            s_label = getText(s_node, 'label')
            s_type  = getText(s_node, 'type')
            fc.write(T + s_type + ' ' + s_label + ';' + '\n')
        fc.write('\n')

    # ...the pointers to the controlouts...
    fc.write(T + '// Pointers to the outlets:\n')
    for c_node in controlouts:
        c_label = getText(c_node, 'label')
        c_type  = getText(c_node, 'type')
        fc.write(T + c_type+' '+ c_label+'Value;'+ '\n')
        fc.write(T + 't_outlet *' + c_label + ';' + '\n')
        fc.write(T + 't_clock *p_'+c_label+'Clock;'+ '\n')
    fc.write('\n')

    # ... and a dummy variable for signal object.
    fc.write(T + '//  Dummy variable needed for ~ objects:\n')
    fc.write(T + 't_sample dummy_f;' + '\n')
    fc.write('\n')


    fc.write('} t_' + pluginLabelTilde + ';' + '\n')



    #----------------------------------------------------------------------------
    # Methods prototypes
    #----------------------------------------------------------------------------
    fc.write('\n' + '\n' + separator)
    fc.write('// Prototypes' + '\n')
    if (deinstantiate):
        fc.write('void ' + pluginLabelTilde + '_free('+ t_pluginLabel +' *x);' + '\n')

#    if (activate):
    fc.write('void ' + pluginLabelTilde + '_activate('+ t_pluginLabel +' *x);' + '\n')
#    if (activate):
    fc.write('void ' + pluginLabelTilde + '_deactivate('+ t_pluginLabel +' *x);' + '\n')

    fc.write('static void ' + pluginLabelTilde + '_print('+ t_pluginLabel +' *x);' + '\n')


    #----------------------------------------------------------------------------
    # Print methods to show infos about the plugin
    #----------------------------------------------------------------------------
    # TODO: write the correct index for inlet number#
    fc.write('\n' + '\n' + separator)
    fc.write(
'''
// Output information about the plugin
static void ''' + pluginLabelTilde + '''_print('''+t_pluginLabel+''' *x){

// General info about the plugin

post("\nThis file has been automatically generated  with XSPIF:
a (X)cross Standard PlugIn Framework
from the XML file : ''' + xspif_filename +'''
Plugin name : ''' + pluginCaption +'''
Plugin label : ''' + pluginLabel + '''
Maker : ''' + pluginMaker + '''
Copyright : ''' + pluginCopyright + '''
Description :''' + pluginComments+ '''\n");
'''+ '\n'*2)

    fc.write('post("Control input(s):");' + '\n')
    fc.write('post("(Index for controls with a dedicated inlet are hinted with a #)");'+'\n')
    i = 0 # TODO: try to change increment: this is no true python
    for p_node in params:
        p_label = getText(p_node, 'label')
        p_min = getText(p_node, 'min')
        p_max = getText(p_node, 'max')
        p_type = getText(p_node, 'type')
        p_mapping = getText(p_node, 'mapping')
        p_unit = getText(p_node, 'unit')
        p_caption = getText(p_node, 'caption')
        p_comment = getText(p_node, 'comment')
        p_noinlet = getText(p_node, 'noinlet')
        if ('true' != p_noinlet):
            p_ind ='#'+ str(i)
        else:
            p_ind = str(i)
        fc.write('post(" ' + p_ind + ' ' + p_caption + ' = %f ('+ p_unit+')", x->m_f'
                 +p_label+ ');' + '\n')
        fc.write('post("    '+ p_label + ', type: ' + p_type
                 + ', in range [' + p_min + ' ; ' + p_max+ ']");' + '\n')
        fc.write('post("    with mapping (suggested): ' + p_mapping+'");' + '\n')
        fc.write('post("    Note:' +p_comment+'");' + '\n')
        i = i+1
                 
    fc.write('post("Control output(s):");' + '\n')
    i = 0 # TODO: try to change increment: this is no true python
    for c_node in controlouts:
        c_label = getText(c_node, 'label')
        c_min = getText(c_node, 'min')
        c_max = getText(c_node, 'max')
        c_type = getText(c_node, 'type')
        c_mapping = getText(c_node, 'mapping')
        c_unit = getText(c_node, 'unit')
        c_caption = getText(c_node, 'caption')
        c_comment = getText(c_node, 'comments')
        c_ind = str(i)
        fc.write('post(" #' + c_ind + ' ' + c_caption + ' (' + c_unit + ')");' + '\n')
        fc.write('post("    '+ c_label + ', type: ' + c_type
                 + ', in range [' + c_min + ' ; ' + c_max+ ']");' + '\n')
        fc.write('post("    with mapping (suggested): ' + c_mapping+'");'+'\n')
        fc.write('post("    Note:' +c_comment+'");' + '\n')
        i = i+1

    
    fc.write('post("Audio input(s):");' + '\n')
    for port in in_ports:
        ind = str(ports_cw.index(port) + 2)
        fc.write('post(" #' + ind + ' ' + port[0] + '");' + '\n')
                 
    fc.write('post("Audio output(s):");' + '\n')    
    for port in out_ports:
        ind = str(ports_cw.index(port) + 2)
        fc.write('post(" #' + ind + ' ' + port[0] + '");' + '\n')

    fc.write('if (x->active)' + '\n'
             +T+'post("Plugin ACTIVATED!");' + '\n'
             +'else'+'\n'
             +T+'post("Plugin DEACTIVATED!");' + '\n')    
    

    fc.write('}' + '\n')


    #----------------------------------------------------------------------------
    # Define methods for parameters which modifies any state
    #----------------------------------------------------------------------------

    fc.write('\n')
    for p_node in params:
        p_label = getText(p_node, 'label')
        p_type = getText(p_node, 'type')
        p_min = getText(p_node, 'min')
        p_max = getText(p_node, 'max')
        p_code =  getText(p_node, 'code')
        

        fc.write('\n' + '\n' + separator)
        fc.write('// Method responding to a change in parameter ' + p_label +  '\n')
        fc.write('static void ' + pluginLabelTilde + '_' + p_label
                 + '('+ t_pluginLabel +' *x, t_floatarg f){' + '\n' *2)
            
        if ('' != p_code):
            #... a copy of the states ...
            writeGetStates(fc, states)
            #... get pointers to the outlets...
            writeGetControlouts(fc, controlouts)
            # ...a copy of the parameters for local use...
            writeGetParams(fc, params)
        else:
            # ...just a copy of the parameter for update...
            fc.write(T +p_type + ' ' + p_label
                     +' = x->m_f'+p_label+';' + '\n')
           
        
        fc.write('\n')
        
        fc.write(T + ' // Check the parameter fits its range and actualize it' + '\n'
                 + T + p_label + ' = FIT_RANGE(f, '+p_min+', '+p_max+');'+'\n'*2)
           
        # Here is the state update code
        if ('' != p_code):
            fc.write('\n' + T + '{' + '\n' )
            fc.write(p_code)    
            fc.write('\n' + T + '}' + '\n'*2 )

        # Update the states and THIS parameter in the plugin structure
        fc.write(T + '// Update ' + p_label + ' and states in the plugin structure:' + '\n')
        fc.write(T + 'x->m_f'+p_label+ ' = '+p_label+';' + '\n')
        if ('' != p_code):
            writeUpdateStates(fc, states)
                    
        fc.write('}' + '\n')

            
    #----------------------------------------------------------------------------
    # Function for controlouts called by clock
    if ([]!=controlouts):
        fc.write('\n' + '\n' + separator)
        fc.write('// Function for the control outlets called by clocks'  + '\n')
       
        for c_node in controlouts:
            c_label = getText(c_node, 'label')
            fc.write('static void '+pluginLabelTilde+'_'+c_label+'('
                     +t_pluginLabel+' *x){'+'\n')
        
            fc.write(T+'outlet_float(x->'+c_label+', x->'+c_label+'Value);'+'\n')
            fc.write('}' + '\n')
        
    #----------------------------------------------------------------------------
    # Function for controlouts : setting the clock
        fc.write('\n' + '\n' + separator)
        fc.write('// Function for controlouts : setting the clock'  + '\n')
        fc.write('static void '+pluginLabelTilde+'_controlouts('
                 +t_pluginLabel+' *x, t_outlet *dest, t_float index, t_float value){'+'\n')

        for c_node in controlouts:
            c_label = getText(c_node, 'label')
            fc.write(T + 'if (dest == x->'+c_label+'){'+'\n')
            fc.write(T*2+'clock_delay(x->p_'+c_label+'Clock, index*1000/XSPIF_GET_SAMPLE_RATE());'+'\n')
            fc.write(T*2+'x->'+c_label+'Value = value;'+'\n')
            fc.write(T+'}' + '\n')
        fc.write('}' + '\n')
           

    #----------------------------------------------------------------------------
    # Define once the XSPIF_WRITE_SAMPLE macro for 'run-replacing' process
    #----------------------------------------------------------------------------
    fc.write('\n' + '\n' + separator)
    fc.write('// Macro for process-replacing' + '\n')
    fc.write('#undef XSPIF_WRITE_SAMPLE'+ '\n'
             '#define XSPIF_WRITE_SAMPLE(dest, index, value) ((dest)[(index)] = (value))'+ '\n'
             )

    #----------------------------------------------------------------------------
    # Define XSPIF_CONTROLOUTS so that it sets the clock, and does not
    # outlet_float during the thread-safe 'perform' routine.
    #----------------------------------------------------------------------------
    fc.write('\n' + '\n' + separator)
    fc.write('// Macro for control outputs in the perform method : use clock' + '\n')
    fc.write('#undef XSPIF_CONTROLOUT'+ '\n'
             '#define XSPIF_CONTROLOUT(dest, index, value)('
             +pluginLabelTilde+'_controlouts(x, dest, index*1000/XSPIF_GET_SAMPLE_RATE(), value)) '+ '\n')


    #----------------------------------------------------------------------------
    # Plugin's 'perform' (DSP processing) function
    #----------------------------------------------------------------------------
    fc.write('\n' + '\n' + separator)
    fc.write('t_int *' + pluginLabelTilde + '_perform(t_int *w)' + '\n'
         + '{' +  '\n'
         + T + t_pluginLabel + ' *x = (' + t_pluginLabel + ' *)(w[1]);' + '\n')

    for port in ports_cw:
        fc.write(T + 't_sample *' + port[0]
                 + ' = (t_sample *)(w[' + str(ports_cw.index(port) + 2) + ']);' + '\n')
        
    fc.write(T + 'int vector_size = (int)(w[' + str(len(ports_cw) + 2)  + ']);' + '\n')
    
    # process only if plugin is active
    fc.write(T+'if (x->active)'+'\n'+T*2+'{'+'\n')
    
    # ... get a copy of the parameters ...
    writeGetParams(fc, params)
    
    # ...get a copy of the states ...
    writeGetStates(fc, states)

    # ...get the pointers to the outlets
    writeGetControlouts(fc, controlouts)

    # here is the DSP algorithm
    writeCallbackCode(fc, process)

    # Update the states in the plugin structure
    writeUpdateStates(fc, states)

    fc.write(T*2+'}'+'\n')
           
    fc.write(T + 'return (w+' + str(len(ports_cw) + 3)  + ');' + '\n')
    fc.write('}' + '\n')
          

    #----------------------------------------------------------------------------
    # Plugin's 'DSP' function: declare dsp method
    #----------------------------------------------------------------------------
    fc.write('\n' + '\n' + separator)
    fc.write('// Plugin DSP method'+'\n')
    fc.write('void ' + pluginLabelTilde + '_dsp(' + t_pluginLabel +' *x, t_signal **sp)' + '\n')
    fc.write('{' + '\n')
    fc.write(T + 'dsp_add(' + pluginLabelTilde + '_perform, ' + str(len(ports_cw) + 2) + ', x,' + '\n' + T * 2 )
    for port in ports_cw:
        fc.write(' sp[' + str(ports_cw.index(port)) + ']->s_vec,')
    fc.write('sp[0]->s_n);' + '\n')
    
    fc.write('}' + '\n')

    
    #----------------------------------------------------------------------------
    # Plugin's new (instantiate) function
    #----------------------------------------------------------------------------
    fc.write('\n' + '\n' + separator)
    fc.write('// Plugin new method' + '\n')
    fc.write('void *' + pluginLabelTilde + '_new('
             + 't_symbol *s, int argc, t_atom *argv)' + '\n' #get the params as varargs
             + '{' +  '\n'
             )
    # declare variables
    fc.write(T+'int i;'+'\n'
             +T+'t_float val;'+'\n')
        
    # declare states
    if ([] != states):
        for s_node in states:
            s_label = getText(s_node, 'label')
            s_type  = getText(s_node, 'type')
            if (-1 != s_type.find('*')):
                fc.write(T + s_type + ' ' + s_label + ' = NULL;' + '\n')
            else:
                fc.write(T + s_type + ' ' + s_label + ';' + '\n')
        fc.write('\n')

    # create the object
    fc.write(T + t_pluginLabel + ' *x = (' + t_pluginLabel + ' *)pd_new('
             + pluginLabelTilde + '_class);' + '\n')

    # set the sample rate:
    fc.write(T + 'x->sample_rate = XSPIF_GET_SAMPLE_RATE();' + '\n')

    # Declare the inlet for the audio ports
    fc.write('\n')
    fc.write(T + '// Declare the in/out-lets for the audio ports' + '\n')
    fc.write(T + '// Beware: 1 inlet already declared in the "CLASS_DEFAULT"' + '\n')
    for port in in_ports[0 : (len(in_ports)-1)]:
        fc.write(T + 'inlet_new(&x->x_obj, &x->x_obj.ob_pd, &s_signal, &s_signal);' + '\n')
    for port in out_ports:
        fc.write(T + 'outlet_new(&x->x_obj, &s_signal);' + '\n')

    # Declare inlets for params with no tag "noinlet"
    fc.write('\n')
    for p_node in params:
       p_label = getText(p_node, 'label')
       p_noinlet = getText(p_node, 'noinlet')
       if ('true' != p_noinlet):
#          if ('' != getText(p_node, 'code')):
#              declare a new inlet (with dedicated method)
#              TODO: make it no only for &s_float taking param type in account
           fc.write(T + '// ' + p_label + ' calls a dedicated method' + '\n')
           fc.write(T + 'inlet_new(&x->x_obj, &x->x_obj.ob_pd, &s_float, '
                        + 'gensym("' + p_label + '")' + ');' + '\n')
#            else:
#                #declare un floatinlet_new (without dedicated method)
#                fc.write(T + '// ' + p_label + ' is written directly' + '\n')
#                fc.write(T + 'floatinlet_new (&x->x_obj, &x->m_f' + p_label + ');' + '\n')
           
    # Declare outlets for controlouts
    fc.write('\n')
    for c_node in controlouts:
        c_label = getText(c_node, 'label')
        # TODO: make it no only for &s_float taking param type in account
        fc.write(T + '//  controlout ' + c_label + '\n')
        fc.write(T+'x->'+c_label+' = outlet_new(&x->x_obj,  &s_float);'+'\n')
        fc.write(T+'x->p_'+c_label+'Clock = clock_new(x, (t_method)'+pluginLabelTilde+'_'+c_label+');'+'\n')
        
    # Put the instanciation code here:
    writeCallbackCode(fc, instantiate)
    
    # Update the states in the plugin structure
    writeUpdateStates(fc, states)

    # Getting the parameters given at instanciation
    # Only the exact number of parameters can be given here
    if ([]!=params):
        fc.write(
            '\n'+T+'// Get the parameters'+'\n'
            +T+'switch (argc)'+'\n'
            +T*2+'{' + '\n'
            +T*2+'case 0:'+'\n')

        for p_node in params:
            p_label = getText(p_node, 'label')
            p_code = getText(p_node, 'code')
            p_default = getText(p_node, 'default')
            fc.write(T*4+pluginLabelTilde+'_' +p_label+'(x, '+p_default+');'+'\n')
            
        fc.write(
            T*3+'break;'+'\n'
            +T*2+'case '+str(len(params))+':'+'\n'+T*3+'{'+'\n'
            +T*4+'// Check all parameters are float'+'\n'
            +T*4+'for (i=0; i <= argc-1;i++)'+'\n'
            +T*5+'if (argv[i].a_type != A_FLOAT)'+'\n'
            +T*6+'{'+'\n'
            +T*7+'post("'+pluginLabelTilde+' : wrong arguments");'+'\n'                     
            +T*7+'return NULL;'+'\n'
            +T*6+'}'+'\n')
            
        p_index = 0
        for p_node in params:
            p_label = getText(p_node, 'label')
            p_min = getText(p_node, 'min')
            p_max = getText(p_node, 'max')
            p_code = getText(p_node, 'code')
            p_default = getText(p_node, 'default')
            fc.write(T*4+'val= atom_getfloatarg('+str(p_index)+', argc, argv);'+'\n')
            fc.write(T*4+pluginLabelTilde+'_' +p_label+'(x, val);'+'\n')
            p_index += 1

        fc.write(T*3+'}'+'\n'
                 +T*3+'break;'+'\n')
        fc.write(T*2+'default:'+'\n'
                 +T*3+'{'+'\n'
                 +T*4+'post( "'+pluginLabel+' : error in the number of arguments ( %d )", argc );' + '\n'
                 +T*4+'return NULL;'+ '\n'
                 +T*3+'}' + '\n'
                 +T*2+'}' + '\n')


    # call method activate
    fc.write('\n')
#   if (activate):
    fc.write(T + pluginLabelTilde + '_activate(x);' + '\n')

    fc.write(T + 'return (void *)x;' + '\n')
    fc.write('}' + '\n')


    #---------------------------------------------------------------------------
    # Plugin activate function
    #---------------------------------------------------------------------------
#    if (activate):
    fc.write('\n' + '\n' + separator)
    fc.write('// Initialise and activate a plugin instance.'+ '\n')
    fc.write(
        'void ' + pluginLabelTilde + '_activate('+ t_pluginLabel +' *x) {' + '\n' * 2)
    
    # Get the states and params
    writeGetStates(fc, states)
    writeGetParams(fc, params)
    
    #... get pointers to the outlets...
    writeGetControlouts(fc, controlouts)
    
    # Put the activate code here:
    writeCallbackCode(fc, activate)

    # Update the states in the plugin structure
    writeUpdateStates(fc, states)

    # Activate the plugin
    fc.write(T+'x->active = 1;'+'\n')
    
    fc.write('}' + '\n')


    #---------------------------------------------------------------------------
    # Plugin deactivate function
    #---------------------------------------------------------------------------
#    if (activate):
    fc.write('\n' + '\n' + separator)
    fc.write('// Deactivate a plugin instance (bypass).'+ '\n')
    fc.write(
        'void ' + pluginLabelTilde + '_deactivate('+ t_pluginLabel +' *x) {' + '\n' * 2)
    
    # Get the states and params
    writeGetStates(fc, states)
    writeGetParams(fc, params)
    
    #... get pointers to the outlets...
    writeGetControlouts(fc, controlouts)
    
    # Put the activate code here:
    writeCallbackCode(fc, deactivate)

    # Update the states in the plugin structure
    writeUpdateStates(fc, states)

    # Deactivate the plugin
    fc.write(T+'x->active = 0;'+'\n')
    
    fc.write('}' + '\n')


    #----------------------------------------------------------------------------
    # Plugin's free (deinstantiate) method
    # (only implemented if the plugin need it)
    #----------------------------------------------------------------------------
    if (deinstantiate  or [] != controlouts):
        fc.write('\n' + '\n' + separator)
        fc.write('// Plugin cleanup method' + '\n')
        fc.write('void ' + pluginLabelTilde + '_free('+t_pluginLabel+' *x){' + '\n')
        
        # Get the states, so that any structure can be deleted fom memory
        writeGetStates(fc, states)
        writeGetParams(fc, params)
        
        if (deinstantiate):
            # Put the deinstantiate code here        
            writeCallbackCode(fc, deinstantiate)

        for c_node in controlouts:
            c_label = getText(c_node, 'label')
            fc.write(T+'clock_free(x->p_'+c_label+'Clock);'+'\n')
            

        fc.write('}' + '\n')


    #----------------------------------------------------------------------------
    # Plugin's setup function
    #----------------------------------------------------------------------------
    
    fc.write('\n' + '\n' + separator)
    fc.write('// Plugin setup method' + '\n')
    fc.write('void ' + pluginLabelTilde + '_setup(void) {' +  '\n'
             + T + pluginLabelTilde + '_class = class_new(gensym("' + pluginLabel+ '~"),' +  '\n'
             + T *2 + '(t_newmethod)' + pluginLabelTilde + '_new,' +  '\n')
    #if plugin needs a destructor, it should be declared here
    if (deinstantiate or [] != controlouts):
        fc.write(T *2 + '(t_method)' + pluginLabelTilde + '_free,' + '\n')
    else:
        fc.write(T *2 + '0,' + '\n')
    fc.write(T *2 + 'sizeof(' + t_pluginLabel + '),' +  '\n'
             + T *2 + 'CLASS_DEFAULT,' +  '\n'
             + T *2 + 'A_GIMME, 0);' +  '\n') #a list of argument can be given representing all parameters

    
    fc.write('\n')
    fc.write(T + 'class_addmethod(' + pluginLabelTilde + '_class,' + '\n'
             + T*2 + '(t_method)' + pluginLabelTilde + '_dsp, gensym("dsp"), 0);' + '\n')
    fc.write(T + 'class_addmethod(' + pluginLabelTilde + '_class,' + '\n'
             + T*2 + '(t_method)' + pluginLabelTilde + '_print, gensym("print"), 0);' + '\n')
    fc.write(T + 'class_addmethod(' + pluginLabelTilde + '_class,' + '\n'
             + T*2 + '(t_method)' + pluginLabelTilde + '_activate, gensym("on"), 0);' + '\n')
    fc.write(T + 'class_addmethod(' + pluginLabelTilde + '_class,' + '\n'
             + T*2 + '(t_method)' + pluginLabelTilde + '_deactivate, gensym("off"), 0);' + '\n')

    fc.write('\n')
    for p_node in params:
        p_label = getText(p_node, 'label')
#        if ('' != getText(p_node, 'code')):
            # declare a new inlet (with dedicated method)
            # TODO: make it no only for &s_float taking param type in account
        fc.write(T + '// Declare a method for the parameter ' + p_label +  '\n')
        fc.write(T + 'class_addmethod(' + pluginLabelTilde + '_class,' + '\n'
                 + T*2 + '(t_method)' + pluginLabelTilde + '_' + p_label
                 + ', gensym("' + p_label + '"), A_FLOAT, 0);' + '\n')


    fc.write(T + '' + '\n')
    fc.write(T + 'CLASS_MAINSIGNALIN(' + pluginLabelTilde + '_class, '
             + t_pluginLabel + ', dummy_f);' + '\n')

    fc.write('}' + '\n')


# float ParameterCheck (char* name, float value, float min, float max )
# {

#     if (value > max)
#     {
# 	printf("Parameter: %s out of range [%.1f...%.1f]. Value limited.\n", name,
# 	       min, max );
# 	return(max);
#     }

#     if(value < min)
#     {
# 	printf("Parameter: %s out of range [%.1f...%.1f]. Value limited.\n", name,
# 	       min, max );
# 	return(min);	
#     }
#     return(value);
# }

    fc.close
    print T+'done'



    #---------------------------------------------------------------------------
    # MAKFILE
    #---------------------------------------------------------------------------

    print T+'writing : Makefile'
    fm = file('Makefile','w')

    fm.write('''
NAME = '''+pluginLabel+'''

current:
	echo make pd_linux, pd_nt, pd_irix5, or pd_irix6

clean: ; rm -f *.pd_linux *.o

# ----------------------- NT -----------------------

pd_nt: $(NAME)~.dll

.SUFFIXES: .dll

# Change this to match you pd path:
PD_NT_PATH = "C:/pd"

PDNTCFLAGS = /W3 /WX /DNT /DPD /nologo
VC="C:\Program Files\Microsoft Visual Studio\Vc98"

PDNTINCLUDE = /I. /I\tcl\include /I$(PD_NT_PATH)\src /I$(VC)\include

PDNTLDIR = $(VC)\lib
PDNTLIB = $(PDNTLDIR)\libc.lib $(PDNTLDIR)\oldnames.lib $(PDNTLDIR)\kernel32.lib $(PD_NT_PATH)/bin/pd.lib 

.c.dll:
	cl $(PDNTCFLAGS) $(PDNTINCLUDE) /c $(NAME)~.c
	link /dll /export:$(NAME)_tilde_setup $(NAME)~.obj $(PDNTLIB)

# ----------------------- IRIX 5.x -----------------------

pd_irix5: $(NAME)~.pd_irix5

.SUFFIXES: .pd_irix5

SGICFLAGS5 = -o32 -DPD -DUNIX -DIRIX -O2


SGIINCLUDE =  -I../../src/

.c.pd_irix5:
	cc $(SGICFLAGS5) $(SGIINCLUDE) -o $*.o -c $*.c
	ld -elf -shared -rdata_shared -o $*.pd_irix5 $*.o
	rm $*.o

# ----------------------- IRIX 6.x -----------------------

pd_irix6: $(NAME)~.pd_irix6

.SUFFIXES: .pd_irix6

SGICFLAGS6 = -n32 -DPD -DUNIX -DIRIX -DN32 -woff 1080,1064,1185 \
	-OPT:roundoff=3 -OPT:IEEE_arithmetic=3 -OPT:cray_ivdep=true \
	-Ofast=ip32

.c.pd_irix6:
	cc $(SGICFLAGS6) $(SGIINCLUDE) -o $*.o -c $*.c
	ld -IPA -n32 -shared -rdata_shared -o $*.pd_irix6 $*.o
	rm $*.o

# ----------------------- LINUX i386 -----------------------

pd_linux: $(NAME)~.pd_linux

.SUFFIXES: .pd_linux

LINUXCFLAGS = -DPD -O6 -funroll-loops -fomit-frame-pointer \
    -Wall -W -Wshadow -Wstrict-prototypes \
    -Wno-unused -Wno-parentheses -Wno-switch

LINUXINCLUDE =  -I/usr/local/lib/pd/include

.c.pd_linux:
	cc $(LINUXCFLAGS) $(LINUXINCLUDE) -o $*.o -c $*.c
	ld -export_dynamic  -shared -o $*.pd_linux $*.o -lc -lm
	strip --strip-unneeded $*.pd_linux
	rm $*.o

# ----------------------- Mac OSX -----------------------

pd_darwin: $(NAME)~.pd_darwin

.SUFFIXES: .pd_darwin

DARWINCFLAGS = -DPD -O2 -Wall -W -Wshadow -Wstrict-prototypes \
    -Wno-unused -Wno-parentheses -Wno-switch

.c.pd_darwin:
	cc $(DARWINCFLAGS) $(LINUXINCLUDE) -o $*.o -c $*.c
	cc -bundle -undefined suppress  -flat_namespace -o $*.pd_darwin $*.o 
	rm -f $*.o ../$*.pd_darwin
	ln -s $*/$*.pd_darwin ..

''')

    fm.close
    print T+'done'

    return
# ------------- (E.O.F.)--------------------
