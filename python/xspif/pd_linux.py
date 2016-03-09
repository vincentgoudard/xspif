#-----------------------------------------------------------------------
#
# Module xspif.pd_linux
#
#-----------------------------------------------------------------------
# TODO : implement -if needed- free method + add it in setup


import sys
import os
import string

def write(plugin, filenamePrefix):
    
    # Mandatory stuffs
    if plugin.has_key('plugId'):
        pluginId = plugin.get('plugId')
    else:
         print('Error: The plugin you build has no Id!' + '\n'
               '       The Id is mandatory and needed to identify the plugin.')
         return

    if plugin.has_key('plugLabel'):
        pluginLabel = plugin.get('plugLabel')
    else:
         print('Error: The plugin you build has no label!' + '\n'
               '       The label is mandatory and needed for the structure name.')
         return

    if plugin.has_key('pins'):
        pluginPins = plugin.get('pins')
    else:
         print('Error: The plugin you compile has no audio pin!')
         return

    if plugin.has_key('callbacks'):
        callbacks = plugin.get('callbacks')
    else:
         print("Warning: You haven't  implemented any callback!")

    if plugin.has_key('params'):
        params = plugin.get('params')
    else:
        print("Warning: The plugin you build has no parameter!")
    
    # Not mandatory
    pluginManufId = plugin.get('manufId', 'Anonymous')
    pluginCaption = plugin.get('plugCaption', 'NO_NAME')
    pluginComments = plugin.get('plugComments', '')
    pluginMaker = plugin.get('maker', 'Anonymous')
    pluginCopyright =  plugin.get('copyright', 'No copyright')

    # useful variables...
    pluginLabelTilde =  pluginLabel + '_tilde'
    t_pluginLabel = 't_' + pluginLabelTilde
    separator = '\n' + '/****************************************************************/' + '\n'

    # make a list with pins
    in_ports = []
    out_ports = []
    for key in pluginPins:
        pin = pluginPins.get(key)
        nb_channels = int(pin.get('pin_channels','0'))
        dir = pin.get('pin_dir')
        caption = pin.get('pin_caption','')
        for i in range(1, nb_channels + 1):
            if ('In' == dir):
                in_ports.append([pin.get('pin_label') + str(i), caption])
            elif ('Out' == dir):
                out_ports.append([pin.get('pin_label') + str(i), caption])

    # ports clockwise sorted W.R.T. the graphical representation of the object.
    out_ports.reverse()
    out_ports_cw = out_ports[:]
    out_ports.reverse()
    ports_cw = in_ports + out_ports_cw
   
    #create output file(s)
    xml_filename = (filenamePrefix + '.xml')
    c_filename = (pluginLabel + '~.pd_linux.c')
    fc = file(c_filename,'w')

    #----------------------------------------------------------------------------
    # file header

    fc.write(
        '/****************************************************************' + '\n'
        + 'XSPIF: cross(X) Standard PlugIn Framework: '
        + 'XSPIF to PD' + '\n'
        + '\t'+c_filename+'\n' + '\n'
        + pluginComments
        + ' This file is generated automatically from the file: '+xml_filename+'\n'
        + '\t'+'plugin ID: '+pluginId+'\n'
        + '\t'+'manufacturer ID: '+pluginManufId+'\n'
        + '\t'+'maker: '+pluginMaker+'\n'
        + '\t'+'copyright: '+plugin.get('copyright', 'No copyright')+'\n'
        + '****************************************************************/' + '\n'
        + '\n' + '\n' + '\n'
    )

    #----------------------------------------------------------------------------
    # includes and independant code
    fc.write('#include <stdlib.h>' + '\n'
             + '#include <string.h>' + '\n'
             + '#ifndef PD_VERSION' + '\n'
             + '#include "m_pd.h"' + '\n'
             + '#endif' + '\n'+ '\n'
             )

    # macros
    fc.write('\n' + '\n' + separator)
    fc.write('// Macro for getting the sample rate' + '\n')
    fc.write('#undef XSPIF_GET_SAMPLE_RATE'+ '\n'
             '#define XSPIF_GET_SAMPLE_RATE() (x->sample_rate)'+ '\n'
             )

    fc.write('// Macro for getting the vector_size' + '\n')
    fc.write('#undef XSPIF_GET_VECTOR_SIZE'+ '\n'
             '#define XSPIF_GET_VECTOR_SIZE() (vector_size)'+ '\n'
             )

    fc.write('\n' + '\n' + separator)
    fc.write(plugin.get('plugCode','// add independant code here') + '\n')

    #----------------------------------------------------------------------------
    # declare internal states declared in states_code as global (??) for instantiate purpose now...
    states_code   = (plugin.get('plugin_states','')).get('states_code','')
    if ('' != states_code):
        fc.write('\n' + '\n' + separator)
        fc.write('// States declared in the <code> section can only be global' + '\n')
        fc.write('// Otherwise, they cannot be accessed in the process functon' + '\n')
        fc.write(states_code + '\n')


    #----------------------------------------------------------------------------
    # Declare the class which contains ...

    fc.write('\n' + '\n' + separator)
    fc.write('static t_class *' + pluginLabelTilde + '_class;' + '\n')
    fc.write('\n')

    # ...a t_object as first entry!! ...
    fc.write('typedef struct _' + pluginLabelTilde + ' {' + '\n'
             + '\t' + 't_object  x_obj;' + '\n')
    
    # ...the sample rate ...
    fc.write('\t' + 'float sample_rate;' + '\n')
    fc.write('\n')
        
    # ...a copy of the parameter for local use...
    fc.write('\t' + '// Internal copy of the parameters:\n')
    for key in params:
        param = params.get(key)
        label = param.get('param_label')
        type  = param.get('param_type')
        fc.write('\t' + type + ' m_f' + label + ';' + '\n')
    fc.write('\n')

    # ... the states ...(except the code_states declared as global)
    fc.write('\t' + '// Internal states:\n')
    states = (plugin.get('plugin_states','')).get('states','')
    if ('' != states):
        for key in states:
            state = states.get(key)
            label = state.get('state_label')
            type  = state.get('state_type')
            fc.write('\t' + type + ' ' + label + ';' + '\n')
    fc.write('\n')

    # ... and a dummy variable for signal object.
    fc.write('\t' + '//  Dummy variable needed for ~ objects:\n')
    fc.write('\t' + 't_sample dummy_f;' + '\n')
    fc.write('\n')


    fc.write('} t_' + pluginLabelTilde + ';' + '\n')



    #----------------------------------------------------------------------------
    # Methods prototypes
    #----------------------------------------------------------------------------
    
    fc.write('\n' + '\n' + separator)
    fc.write('// Prototypes' + '\n')
    if (callbacks.has_key('deinstantiate')):
        fc.write('void ' + pluginLabelTilde + '_free('+ t_pluginLabel +' *x);' + '\n')

    if (callbacks.has_key('activate')):
        fc.write('void ' + pluginLabelTilde + '_activate('+ t_pluginLabel +' *x);' + '\n')

    fc.write('static void ' + pluginLabelTilde + '_print('+ t_pluginLabel +' *x);' + '\n')


    #----------------------------------------------------------------------------
    # Print methods to show infos about the plugin
    #----------------------------------------------------------------------------

    fc.write('\n' + '\n' + separator)
    fc.write('// Output information about the plugin' + '\n')
    fc.write('static void ' + pluginLabelTilde + '_print'
                 + '('+ t_pluginLabel +' *x){' + '\n' *2)

    fc.write('// General info about the plugin' + '\n')
    fc.write('post("\nThis file has been automatically generated  with XSPIF:' + '\n'
             + 'a (X)cross Standard PlugIn Framework' + '\n'
             + 'from the XML file : ' + xml_filename + '");' + '\n')
    fc.write('post("Plugin name : ' + pluginCaption + '");' + '\n')
    fc.write('post("Plugin label : ' + pluginLabel + '~' + '");' + '\n')
    fc.write('post("Maker : ' + pluginMaker + '");' + '\n')
    fc.write('post("Copyright : ' + pluginCopyright + '");' + '\n')
    fc.write('post("Description :' + pluginComments+ '");' + '\n')

    fc.write('\n')
    fc.write('// Info about the ports' + '\n')
    fc.write('post("Control input(s):");' + '\n')
    for key in params:
        param = params.get(key)
        label = param.get('param_label')
        cap = param.get('param_caption', label)
        type = param.get('param_type','')
        min = param.get('param_min','No min value specidied')
        max = param.get('param_max','No max value specified')
        unit = param.get('param_unit', 'No unit specified')
        ind = str(params.keys().index(key))
        fc.write('post(" #' + ind + ' ' + cap + ' (' + unit + ')");' + '\n')
        fc.write('post("    '+ label + ', type: ' + type
                 + ', in range [' + min + ' ; ' + max + ']");' + '\n')    

    fc.write('post("Control output(s):");' + '\n')
    
    fc.write('post("Audio input(s):");' + '\n')
    for port in in_ports:
        ind = str(ports_cw.index(port) + 2)
        fc.write('post(" #' + ind + ' ' + port[0] + '");' + '\n')
                 
    fc.write('post("Audio output(s):");' + '\n')    
    for port in out_ports:
        ind = str(ports_cw.index(port) + 2)
        fc.write('post(" #' + ind + ' ' + port[0] + '");' + '\n')

    fc.write('}' + '\n')


    #----------------------------------------------------------------------------
    # Define methods for parameters which implies an indirect mapping
    #----------------------------------------------------------------------------

    fc.write('\n')
    for key in params:
        param = params.get(key)
        p_label = param.get('param_label')
        p_type = param.get('param_type')
        p_min = param.get('param_min')
        p_max = param.get('param_max')
        p_code =  param.get('param_code','')
        
        if ('' != p_code):
            fc.write('\n' + '\n' + separator)
            fc.write('// Method responding to a change in parameter ' + p_label +  '\n')
            fc.write('static void ' + pluginLabelTilde + '_' + p_label
                     + '('+ t_pluginLabel +' *x, t_floatarg f){' + '\n' *2)
            
            # ...a copy of the parameters for local use...
            fc.write('\t' + '// Local copy of the parameters:\n')
            for lp_key in params:
                lp_param = params.get(lp_key)
                lp_label = lp_param.get('param_label')
                lp_type  = lp_param.get('param_type')
                fc.write('\t' + lp_type + ' ' + lp_label + ' = x->m_f' + lp_label + ';' + '\n')
            fc.write('\n')

            fc.write('\t' + '// Internal states:\n')
            states = (plugin.get('plugin_states','')).get('states','')
            if ('' != states):
                for key in states:
                    state = states.get(key)
                    s_label = state.get('state_label')
                    s_type  = state.get('state_type')
                    fc.write('\t' + s_type + ' ' + s_label + ' = x->' + s_label + ';' + '\n')
                fc.write('\n')


            fc.write('\t' + ' // Check the parameter fits its range and actualize it' + '\n'
                     + '\t' + p_label + ' = '
                     + '(((f) < '+p_min+') ? '+p_min+' : (((f) > '+p_max+') ? '+p_max+' : (f)));'+'\n'*2)
           
            # Here is the state update code
            fc.write('\n' + '\t' + '{' + '\n' )
            fc.write(p_code)    
            fc.write('\t' + '}' + '\n'*2 )

            # Update the states and THIS parameter in the plugin structure
            fc.write('\t' + '// Update ' + p_label + ' and states in the plugin structure:' + '\n')
            fc.write('\t' + 'x->m_f'+p_label+ ' = '+p_label+';' + '\n')
            if ('' != states):
                for key in states:
                    state = states.get(key)
                    state_label = state.get('state_label')
                    state_type  = state.get('state_type')
                    fc.write('\t' + 'x->' + state_label + ' = ' + state_label + ';' + '\n')
                    
            fc.write('}' + '\n')

            
    #----------------------------------------------------------------------------
    # Define once the XSPIF_WRITE_SAMPLE macro for 'run-replacing' process
    #----------------------------------------------------------------------------
    fc.write('\n' + '\n' + separator)
    fc.write('// Macro for process-replacing' + '\n')
    fc.write('#undef XSPIF_WRITE_SAMPLE'+ '\n'
             '#define XSPIF_WRITE_SAMPLE(dest, index, source) ((dest)[(index)] = (source))'+ '\n'
             )



    #----------------------------------------------------------------------------
    # Plugin's 'perform' (DSP processing) function
    fc.write('\n' + '\n' + separator)
    fc.write('t_int *' + pluginLabelTilde + '_perform(t_int *w)' + '\n'
         + '{' +  '\n'
         + '\t' + t_pluginLabel + ' *x = (' + t_pluginLabel + ' *)(w[1]);' + '\n')

    for port in ports_cw:
        fc.write('\t' + 't_sample *' + port[0]
                 + ' = (t_sample *)(w[' + str(ports_cw.index(port) + 2) + ']);' + '\n')
        
    fc.write('\t' + 'int vector_size = (int)(w[' + str(len(ports_cw) + 2)  + ']);' + '\n')
    
    # ... get a copy of the parameters ...TODO: get/convert the type (enum, float...)
    fc.write('\n')
    for key in params:
        param = params.get(key)
        param_caption = param.get('param_caption')
        param_label = param.get('param_label')
        param_type = param.get('param_type')
        fc.write(
            '\t' + '/*'+ param_caption + '*/'+ '\n'
            + '\t' 'const  ' + param_type + ' '  + param_label + ' = x->m_f' + param_label +';' + '\n'
            )

    
    # ...get a copy of the states ...
    fc.write('\t' + '// States:' + '\n')
    if ('' != states):
        for key in states:
            state = states.get(key)
            state_label = state.get('state_label')
            state_type  = state.get('state_type')
            fc.write('\t' + state_type + ' ' + state_label + ' = x->' + state_label + ';' + '\n')
            
    fc.write('\n')

    # here is the DSP algorithm
    process_code = callbacks.get('process').get('code')
    #print process_code
    fc.write('// Here is the DSP algorithm:'+ '\n')
    fc.write('\t' + '{' + '\n')
    fc.write(process_code)
    fc.write('\t' + '\n' + '}' + '\n')
    fc.write('\n')

    # Update the states in the plugin structure
    fc.write('\t' + '// Update the states in the plugin structure:' + '\n')
    if ('' != states):
        for key in states:
            state = states.get(key)
            state_label = state.get('state_label')
            state_type  = state.get('state_type')
            fc.write('\t' + 'x->' + state_label + ' = ' + state_label + ';' + '\n')
    fc.write('\n')


    fc.write('\t' + 'return (w+' + str(len(ports_cw) + 3)  + ');' + '\n')
    fc.write('}' + '\n')
          

    #----------------------------------------------------------------------------
    # Plugin's 'DSP' function: declare dsp method
    fc.write('\n' + '\n' + separator)
    fc.write('// Plugin DSP method'+'\n')
    fc.write('void ' + pluginLabelTilde + '_dsp(' + t_pluginLabel +' *x, t_signal **sp)' + '\n')
    fc.write('{' + '\n')
    fc.write('\t' + 'dsp_add(' + pluginLabelTilde + '_perform, ' + str(len(ports_cw) + 2) + ', x,' + '\n' + '\t' * 2 )
    for port in ports_cw:
        fc.write(' sp[' + str(ports_cw.index(port)) + ']->s_vec,')
    fc.write('sp[0]->s_n);' + '\n')
    
    fc.write('}' + '\n')

    
    #----------------------------------------------------------------------------
    # Plugin's new (instantiate) function

    fc.write('\n' + '\n' + separator)
    fc.write('// Plugin new method' + '\n')
    fc.write('void *' + pluginLabelTilde + '_new('
             + 't_symbol *s, int argc, t_atom *arg)' + '\n' #get the params as varargs
             + '{' +  '\n'
             )
    # declare states
    if ('' != states):
        for key in states:
            state = states.get(key)
            label = state.get('state_label')
            type  = state.get('state_type')
            if (-1 != type.find('*')):
                fc.write('\t' + type + ' ' + label + ' = NULL;' + '\n')
            else:
                fc.write('\t' + type + ' ' + label + ';' + '\n')
        fc.write('\n')

    # create the object
    fc.write('\t' + t_pluginLabel + ' *x = (' + t_pluginLabel + ' *)pd_new('
             + pluginLabelTilde + '_class);' + '\n')

    # set the sample rate: # TODO: get it from PD
    fc.write('\t' + 'x->sample_rate = 44100.0;' + '\n')

    # Declare the inlet for the audio ports
    fc.write('\n')
    fc.write('\t' + '// Declare the in/out-lets for the audio ports' + '\n')
    fc.write('\t' + '// Beware: 1 inlet already declared in the "CLASS_DEFAULT"' + '\n')
    for port in in_ports[0 : (len(in_ports)-1)]:
        fc.write('\t' + 'inlet_new(&x->x_obj, &x->x_obj.ob_pd, &s_signal, &s_signal);' + '\n')
    for port in out_ports:
        fc.write('\t' + 'outlet_new(&x->x_obj, &s_signal);' + '\n')

    # Declare inlets for params
    fc.write('\n')
    for key in params:
       param = params.get(key)
       label = param.get('param_label')
       if ('' != param.get('param_code','')):
           # declare a new inlet (with dedicated method)
           # TODO: make it no only for &s_float taking param type in account
           fc.write('\t' + '// ' + label + ' calls a dedicated method' + '\n')
           fc.write('\t' + 'inlet_new(&x->x_obj, &x->x_obj.ob_pd, &s_float, '
                    + 'gensym("' + label + '")' + ');' + '\n')
       else:
           #declare un floatinlet_new (without dedicated method)
           fc.write('\t' + '// ' + label + ' is written directly' + '\n')
           fc.write('\t' + 'floatinlet_new (&x->x_obj, &x->' + label + ');' + '\n')
           
    # Put the instanciation code here:
    if (callbacks.has_key('instantiate')):
        instantiate_code = (callbacks.get('instantiate')).get('code')
        fc.write('\t' + '{' + '\n')
        fc.write('\t' * 2 + instantiate_code + '\n')
        fc.write('\t' + '}' + '\n')
    
# TODO!!!
    fc.write('\n')
    fc.write('\t' + '// Get the arguments given at instanciation' + '\n')    
    fc.write('\t' + 'if (argc > ' + str(len(params.keys()))
             + ') post("'+ pluginLabelTilde +': extra arguments ignored");' +'\n')

#TODO: get params and generates protection with min and max
# values (see lowpass.c)
#    for key in params:
#        param = params.get(key)
#        label = param.get('param_label')
#        fc.write('\t'*2 + 'x->' + label + '= arg[' + str(params.keys().index(key)) + '];' + '\n')
#    fc.write('\t'*2 + '}' + '\n')

    # Update the states in the plugin structure
    fc.write('\t' + '// Update the states in the plugin structure:' + '\n')
    if ('' != states):
        for key in states:
            state = states.get(key)
            state_label = state.get('state_label')
            state_type  = state.get('state_type')
            fc.write('\t' + 'x->' + state_label + ' = ' + state_label + ';' + '\n')

    # call method activate
    fc.write('\n')
    if (callbacks.has_key('activate')):
        fc.write('\t' + pluginLabelTilde + '_activate(x);' + '\n')

    fc.write('\t' + 'return (void *)x;' + '\n')
    fc.write('}' + '\n')


    #---------------------------------------------------------------------------
    # Plugin activate function
    # (only implemented if the plugin need it)
    #---------------------------------------------------------------------------
    if (callbacks.has_key('activate')):
        activate_code = (callbacks.get('activate')).get('code','')
        fc.write('\n' + '\n' + separator)
        fc.write('// Initialise and activate a plugin instance.'+ '\n')
        fc.write(
        'void ' + pluginLabelTilde + '_activate('+ t_pluginLabel +' *x) {' + '\n' * 2)
        # Get the states, so that any structure can be deleted fom memory
        fc.write('\t' + '// States:' + '\n')
        if ('' != states):
            for key in states:
                state = states.get(key)
                state_label = state.get('state_label')
                state_type  = state.get('state_type')
                fc.write('\t' + state_type + ' ' + state_label
                         + ' = x->' + state_label + ';' + '\n')

        # Put the activate code here:
        fc.write('\t' + '{' + '\n')
        fc.write(activate_code)
        fc.write('\t' + '}' + '\n')

        # Update the states in the plugin structure
        fc.write('\t' + '// Update the states in the plugin structure:' + '\n')
        if ('' != states):
            for key in states:
                state = states.get(key)
                state_label = state.get('state_label')
                state_type  = state.get('state_type')
                fc.write('\t' + 'x->' + state_label + ' = ' + state_label + ';' + '\n')
        fc.write('}' + '\n')


    #----------------------------------------------------------------------------
    # Plugin's free (deinstantiate) method
    # (only implemented if the plugin need it)
    #----------------------------------------------------------------------------
    if (callbacks.has_key('deinstantiate')):
        fc.write('\n' + '\n' + separator)
        fc.write('// Plugin cleanup method' + '\n')
        fc.write('void ' + pluginLabelTilde + '_free('+t_pluginLabel+' *x){' + '\n')
        
        # Get the states, so that any structure can be deleted fom memory
        fc.write('\t' + '// States:' + '\n')
        if ('' != states):
            for key in states:
                state = states.get(key)
                state_label = state.get('state_label')
                state_type  = state.get('state_type')
                fc.write('\t' + state_type + ' ' + state_label + ' = x->' + state_label + ';' + '\n')

        # Put the deinstantiate code here        
        deinstantiate_code = (callbacks.get('deinstantiate')).get('code')
        fc.write('\t' + '{' + '\n')
        fc.write(deinstantiate_code + '\n')
        fc.write('\t' + '}' + '\n')

        fc.write('}' + '\n')


    #----------------------------------------------------------------------------
    # Plugin's setup function
    #----------------------------------------------------------------------------
    
    fc.write('\n' + '\n' + separator)
    fc.write('// Plugin setup method' + '\n')
    fc.write('void ' + pluginLabelTilde + '_setup(void) {' +  '\n'
             + '\t' + pluginLabelTilde + '_class = class_new(gensym("' + pluginLabel+ '~"),' +  '\n'
             + '\t' *2 + '(t_newmethod)' + pluginLabelTilde + '_new,' +  '\n'
             )
    #if plugin needs a destructor, it should be declared here
    if (callbacks.has_key('deinstantiate')):
        fc.write('\t' *2 + '(t_method)' + pluginLabelTilde + '_free,' + '\n')
    else:
        fc.write('\t' *2 + '0,' + '\n')

    fc.write('\t' *2 + 'sizeof(' + t_pluginLabel + '),' +  '\n'
             + '\t' *2 + 'CLASS_DEFAULT,' +  '\n'
             + '\t' *2 + 'A_GIMME, 0);' +  '\n' #a list of argument can be given representing all parameters
             )
    
    fc.write('\n')
    fc.write('\t' + 'class_addmethod(' + pluginLabelTilde + '_class,' + '\n'
             + '\t'*2 + '(t_method)' + pluginLabelTilde + '_dsp, gensym("dsp"), 0);' + '\n')
    fc.write('\t' + 'class_addmethod(' + pluginLabelTilde + '_class,' + '\n'
             + '\t'*2 + '(t_method)' + pluginLabelTilde + '_print, gensym("print"), 0);' + '\n')


    fc.write('\n')
    for key in params:
        param = params.get(key)
        label = param.get('param_label')
        if ('' != param.get('param_code','')):
            # declare a new inlet (with dedicated method)
            # TODO: make it no only for &s_float taking param type in account
            fc.write('\t' + '// Declare a method for the parameter ' + label +  '\n')
            fc.write('\t' + 'class_addmethod(' + pluginLabelTilde + '_class,' + '\n'
                     + '\t'*2 + '(t_method)' + pluginLabelTilde + '_' + label
                     + ', gensym("' + label + '"), A_FLOAT, 0);' + '\n')


    fc.write('\t' + '' + '\n')
    fc.write('\t' + 'CLASS_MAINSIGNALIN(' + pluginLabelTilde + '_class, '
             + t_pluginLabel + ', dummy_f);' + '\n')

    fc.write('}' + '\n')


