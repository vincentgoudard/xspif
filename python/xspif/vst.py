#-----------------------------------------------------------------------
# XSPIF: a (X)cross Standard PlugIn Framework
# Copyright (C) 2003 IRCAM - Centre Pompidou
# Authors: Remy Muller and Vincent Goudard
# Module xspif.vst : XSPIF to VST translator
#-----------------------------------------------------------------------

from xspif.parsexml import getText

tab = 2
T = ' '*tab

def write(plugin,filename_prefix):
    print T+'writing : '+filename_prefix+'.vst.cpp'
    fcpp = file(filename_prefix + '.vst.cpp','w')
    xml_filename  = filename_prefix + ".xspif"

    ######## independent code here ############

    # Variables
    plugId        = getText(plugin,'plugId')
    manufId       = getText(plugin,'manufId')
    maker         = getText(plugin,'maker')
    pluginLabel   = getText(plugin,'label')
    # forces the first letter to upper case becaus it will be used to name the C++ class
    pluginLabel.title(); 
    copyright     = getText(plugin,'copyright')
    comment = getText(plugin,'comment')+'\n'
    pluginCode = getText(plugin,'code')+'\n'
    pluginCaption = getText(plugin,'caption')
 
    params = plugin.getElementsByTagName('param')
    controlouts = plugin.getElementsByTagName('controlout')   
    states = plugin.getElementsByTagName("state")
    pins = plugin.getElementsByTagName("pin")
    callbacks = plugin.getElementsByTagName('callback')

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
            if text == 'deinstantiate':
                deinstantiate = callback
            if text == 'activate':
                activate = callback
            if text == 'deactivate':
                deactivate = callback
            if text == 'process':
                process = callback
            if text == 'processEvents':
                print 'XSPIF Warning: callback "processEvents" not implemented in VST for now'
                #processEvents = callback  

    instantiateCode = getText(instantiate,'code')
    deinstantiateCode = getText(deinstantiate,'code')
    activateCode = getText(activate,'code')
    deactivateCode = getText(deactivate,'code')
    processCode = getText(process,'code')

    #----------------------------------------------------------------------------
    # CPP file
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # file header

    fcpp.write(
        '/****************************************************************\n'
        + 'XSPIF: cross(X) Standard PlugIn Framework: '
        + 'XSPIF to VST\n'
        + T+filename_prefix+'.vst.cpp'+'\n\n'
        + comment
        + ' This file is generated automatically from the file: '+xml_filename+'\n'
        + ' DO NOT EDIT BY HAND'+'\n'
        + T+'plugin ID: '+plugId+'\n'
        + T+'manufacturer ID: '+manufId+'\n'
        + T+'maker: '+maker+'\n'
        + T+'copyright: '+copyright+'\n'
        + ' ***************************************************************/\n'
        + '\n'
        )

    #----------------------------------------------------------------------------
    # includes and independant code

    fcpp.write('#include "audioeffectx.h"\n'
               +'#include <string.h>\n'
               +'\n'
               +'#define XSPIF_GET_SAMPLE_RATE() (sr)'+'\n'
               +'#define XSPIF_GET_VECTOR_SIZE() (vector_size)'+'\n'
               +'#define XSPIF_CONTROLOUT(label, index, value) (controlOut(label,index,value))'+'\n'
               +'\n')

    fcpp.write('// from '+xml_filename+'\n'
               +pluginCode)
    
    #----------------------------------------------------------------------------
    # parameters constants and declaration ...
    if params != []:
        fcpp.write('\n'
                   +'//-------------------------------------------------------------\n'
                   +'// Parameters constant and declarations\n'
                   +'\n'
                   +'const double e = exp(1.0);'+'\n')

        for param in params:
            label   = getText(param,'label')
            caption = getText(param,'caption')
            comment = getText(param,'comment')
            default = getText(param,'default')
            min     = getText(param,'min')
            max     = getText(param,'max')
            mapping = getText(param,'mapping')
            fcpp.write('\n' 
                       +'// '+caption+'\n'
                       +'// '+comment+'\n'
                       +'const float '+label+'Default'+' = '+default+';\n'
                       +'const float '+label+'Min'+' = '+min+';\n'
                       +'const float '+label+'Max'+' = '+max+';\n'
                       +'\n')  
            
        # write params enumeration 
        fcpp.write('enum\n'
                   +'{\n')

        for param in params:            
            label   = getText(param,'label')
            fcpp.write(T+'k'+label+',\n')  
            
        fcpp.write('\n'
                   +T+'kNumParams'+'\n'
                   +'};\n'
                   +'\n')

    #----------------------------------------------------------------------------
    # controlouts
    if controlouts != []:
        fcpp.write('\n'
                   +'//-------------------------------------------------------------\n'
                   +'// control out ranges constant and declarations\n'
                   +'\n')

        for controlout in controlouts:
            label   = getText(controlout,'label')
            caption = getText(controlout,'caption')
            comment = getText(controlout,'comment')
            min     = getText(controlout,'min')
            max     = getText(controlout,'max')
            fcpp.write('\n' 
                       +'// '+caption+'\n'
                       +'// '+comment+'\n'
                       +'const float '+label+'Min'+' = '+min+';\n'
                       +'const float '+label+'Max'+' = '+max+';\n'
                       +'\n')  
            
        # write controlouts enumeration 
        fcpp.write('enum\n'
                   +'{\n')

        for controlout in controlouts:            
            label   = getText(controlout,'label')
            fcpp.write(T+label+',\n')  
            
        fcpp.write('\n'
                   +T+'kNumControlouts'+'\n'
                   +'};\n'
                   +'\n')
            
    #----------------------------------------------------------------------------
    # classes
    
    fcpp.write('\n'
               +'class '+pluginLabel+';\n'
               +'\n')
    
    # PluginProgram classdeclaration
    fcpp.write('//-------------------------------------------------------------\n'
               +'//'+pluginLabel+'Program'+'\n'
               +'\n'
               +'class '+pluginLabel+'Program'+'\n'
               +'{'+'\n'
               +'friend class '+pluginLabel+';'+'\n'
               +'public:'+'\n'
               +T+pluginLabel+'Program();'+'\n'
               +T+'~'+pluginLabel+'Program() {}'+'\n'
               +'private:'+'\n')

    if params != []:
        for param in params:
            label   = getText(param,'label')
            fcpp.write(T+'float f'+label+'; // normalized param'+'\n')  
            
    fcpp.write(T+'char name[24];'+'\n'
                   +'};'+'\n'
                   +'\n')

    # Plugin classdeclaration
    fcpp.write(
"""
//-------------------------------------------------------------
//"""+pluginLabel+"""

class """+pluginLabel+""" : public AudioEffectX
{
public:
  """+pluginLabel+"""(audioMasterCallback audioMaster);
  ~"""+pluginLabel+"""();

  virtual void process(float **inputs, float **outputs, long sampleframes);
  virtual void processReplacing(float **inputs, float **outputs, long sampleFrames);
  virtual void setProgram(long program);
  virtual void setProgramName(char *name);
  virtual void getProgramName(char *name);
  virtual void setParameter(long index, float value);
  virtual float getParameter(long index);
  virtual void getParameterDisplay(long index, char *text);
  virtual void getParameterName(long index, char *text);
  virtual void getParameterLabel(long index, char *label);
  virtual bool getEffectName(char *name);
  virtual bool getVendorString(char *text);
  virtual void resume();
  virtual long canDo(char *text);
  virtual void suspend();

private:
  """+pluginLabel+"""Program *programs;

""")
    if controlouts != []:
        fcpp.write('void '+pluginLabel+'::controlout(long label, long index, float value)'+'\n')
        
    if params != []:
        fcpp.write(T+'// <parameters>'+'\n')
        for param in params:
            label   = getText(param,'label')
            type    = getText(param,'type')
            default = label+'Default'
            min     = label+'Min'
            max     = label+'Max'
            fcpp.write(T+type+' '+label+'; // param'+'\n'
                       +T+'float f'+label+'; // normalized param'+'\n'
                       +'\n')  

        fcpp.write(T+'// </parameters>'+'\n'
                       +'\n')

    # macros
    fcpp.write(T+'float sr;'+'\n'
               +T+'long vector_size;'+'\n'
               +'\n')

    # states
    if states != []:
        fcpp.write(T+'// states'+'\n')
        for state in states:
            label = getText(state,'label')
            type  = getText(state,'type')
            fcpp.write(T+type+' '+label+';'+'\n')
            
    fcpp.write('};'+'\n'
               +'\n')

    fcpp.write("""
//----------------------------------------------------------------------------
// IMPLEMENTATION 
//----------------------------------------------------------------------------

""")

    #----------------------------------------------------------------------------
    # includes 
    
    fcpp.write('#include <stdio.h>\n'
               +'#include <string.h>\n')

    #----------------------------------------------------------------------------
    # Topology

    numInputs = numOutputs = 0
    
    for pin in pins:
        dir      = getText(pin,'dir')
        channels = int(str(getText(pin,'channels')))
        if dir == 'In':
            numInputs += channels
        elif dir == 'Out':
            numOutputs += channels

    numInputs  = str(numInputs)
    numOutputs = str(numOutputs)

    fcpp.write('//-------------------------------------------------------------'+'\n'
               +'// Config'+'\n'
               +'#define NUM_INPUTS '+numInputs+'\n'
               +'#define NUM_OUTPUTS '+numOutputs+'\n'
               +'#define NUM_PRESETS '+'4'+'\n'
               +'//infos'+'\n'
               +'#define ID '+plugId+'\n'
               +'#define NAME "'+pluginCaption+'"'+'\n'
               +'#define VENDOR "'+maker+'"'+'\n'
               +'\n'
               +'#define CAN_PROCESS_REPLACING true'+'\n'
               +'#define CAN_MONO true'+'\n'
               +'\n'
               +'\n'
               )
    
    #----------------------------------------------------------------------------
    # Presets class

    fcpp.write('//-------------------------------------------------------------'+'\n'
               +'// '+pluginLabel+'Program class implementation'+'\n'
               +'\n'
               +pluginLabel+'Program::'+pluginLabel+'Program()'+'\n'
               +'{'+'\n')
    
    if params != [] :
        for param in params:
            label   = getText(param,'label')
            default = label+'Default'
            min     = label+'Min'
            max     = label+'Max'
            mapping = getText(param,'mapping')
            type    = getText(param,'type')
            
            if mapping == 'lin':
                fcpp.write(T+'f'+label+' = ('+default+'-'+min+')/('+max+'-'+min+');'+'\n')
            elif mapping == 'log':
                # external->internal is logarithmic
                #   ( log(v)-log(min) ) / ( log(max)-log(min) )
                # = ( log(v/min) / ( log(max/min) )
                fcpp.write(T+'f'+label+' = log('+default+'/'+min+')/(log('+max+'/'+min+'));'+'\n')
            
            
    fcpp.write(T+'\n'
               +T+'strcpy(name,"'+pluginCaption+'");'+'\n'
               +'}'+'\n'
               +'\n'
               )
    #----------------------------------------------------------------------------
    # Plugin Class

    #----------------------------------------------------------------------------
    # Plugin Constructor
    
    fcpp.write('//-------------------------------------------------------------'+'\n'
               +'// '+pluginLabel+' class implementation'+'\n'
               +'\n'
               +pluginLabel+'::'+pluginLabel+'(audioMasterCallback audioMaster)'+'\n'
               +': AudioEffectX(audioMaster, NUM_PRESETS, kNumParams)'+'\n'
               +'{'+'\n'
               +T+'programs = new '+pluginLabel+'Program[numPrograms];'+'\n'
               +T+'\n'
               +T+'sr = getSampleRate();'+'\n'
               +T+'if(sr<0.f) sr = 44100.f;'+'\n'
               +'\n'
               )
    
    if params != []:
        for param in params:
            label   = getText(param,"label")
            default = label+'Default'
            min     = label+'Min'
            max     = label+'Max'
            mapping = getText(param,'mapping')
            
            if mapping == 'lin':
                fcpp.write(T+'f'+label+' = ('+default+'-'+min+')/('+max+'-'+min+');'+'\n'
                           +T+label+' = '+default+';'+'\n')
            elif mapping == 'log':
                # external->internal is logarithmic
                #   ( log(v)-log(min) ) / ( log(max)-log(min) )
                # = ( log(v/min) / ( log(max/min) )
                fcpp.write(T+'f'+label+' = log('+default+'/'+min+')/(log('+max+'/'+min+'));'+'\n')
       
    fcpp.write('\n'
               +T+'// instantiate callback'+'\n'
               +T+instantiateCode+'\n'
               +'\n')

    fcpp.write(
"""
  if(programs) setProgram(0);

  setUniqueID(ID);
  setNumInputs(NUM_INPUTS);
  setNumOutputs(NUM_OUTPUTS);
  canProcessReplacing(CAN_PROCESS_REPLACING);
  canMono(CAN_MONO);
}

""")

    #----------------------------------------------------------------------------
    # Plugin Destructor

    fcpp.write('//-------------------------------------------------------------'+'\n'
               +pluginLabel+'::~'+pluginLabel+'()'+'\n'
               +'{'+'\n'
               +T+'if(programs)'+'\n'
               +T*2+'delete[] programs;'+'\n')
    
    fcpp.write('\n'
               +T+'// deinstantiate callback'+'\n'
               +T+deinstantiateCode+'\n'
               +'\n')

    fcpp.write('}'+'\n'
               +'\n')

    #----------------------------------------------------------------------------
    # Plugin infos
    if controlouts != []:
        fcpp.write('//-------------------------------------------------------------'+'\n'
                   +'// control out'+'\n'
                   +'\n'
                   +'void '+pluginLabel+'::controlout(long label, long index, float value)'+'\n'
                   +'{'+'\n'
                   +T+'char out=0;'+'\n'
                   +T+'char cc=0;'+'\n'
                   +T+'switch(label)'+'\n'
                   +T+'{'+'\n')

    
        i = 38 # first MIDI CC that will be used fo control out
        for controlout in controlouts:
            label = getText(controlout,'label')
            max   = label+'Max'
            min   = label+'Min'
            mapping = getText(controlout,'mapping')
            controloutCode = getText(param,'code')
            
            if i >127:
                print 'warning too much controlouts CC numbers exceed 127'
                return

            fcpp.write(T*2+'case '+label+' :'+'\n' 
                       +T*3+'cc = '+str(i)+';'+'\n')
            i = i+1
                        
            if mapping == 'lin':
                fcpp.write(T*3+'out = 127*((value-'+min+')/('+max+'-'+min+'));'+'\n')            

            elif mapping == 'log':
                #
                fcpp.write(T*3+'out = 127*(log(value/'+min+')/log('+max+'/'+min+'));'+'\n')
                        
        fcpp.write(
            '\n'
            +T*2+'default: return;'+'\n'
            +T+'}'+'\n'
            +'\n'
            +T+'if(index>vector_size)'+'\n'
            +T*2+'index = vector_size;'+'\n'
            +'\n' 
        
            +T+'VstMidiEvent vstEvent;'+'\n'  
            +T+'VstEvents vstEvents; '+'\n' 
            +T+'vstEvents.numEvents =1; '+'\n' 
            +T+'vstEvents.reserved = 0; '+'\n' 
            +T+'vstEvents.events[0] = (VstEvent*)(&vstEvent); '+'\n' 
            +T+'vstEvents.events[1]= NULL; '+'\n'
            +'\n' 
        
            +T+'memset(&vstEvent, 0, sizeof(vstEvent));'+'\n' 
            +T+'vstEvent.type = kVstMidiType;'+'\n' 
            +T+'vstEvent.byteSize = 24;'+'\n' 
                
            +T+'vstEvent.deltaFrames = index; '+'\n' 
            +T+'vstEvent.midiData[0]=0xb0; // tells it sends midi CC'+'\n' 
            +T+'vstEvent.midiData[1]=cc; '+'\n' 
            +T+'vstEvent.midiData[2]=out; '+'\n' 
            +T+'((AudioEffectX *)this)->sendVstEventsToHost(&vstEvents);'+'\n' 
            +'}'+'\n'
            )

    #----------------------------------------------------------------------------
    # Plugin infos

    fcpp.write('//-------------------------------------------------------------'+'\n'
               +'// '+pluginLabel+' information'+'\n'
               +'\n'
               +'bool '+pluginLabel+'::getEffectName(char *name) {'+'\n'
               +T+'strcpy(name, NAME); // name max 32 char'+'\n'
               +T+'return true;}'+'\n'
               +'\n'
               +'bool '+pluginLabel+'::getVendorString(char *text) {'+'\n'
               +T+'strcpy(text, VENDOR); // vendor max 64 char'+'\n'
               +T+'return true;}'+'\n'
               +'\n')

    fcpp.write('long '+pluginLabel+'::canDo(char* text)'+'\n'
               +'\t'+'{'+'\n' )

    if controlouts != []:
        fcpp.write(
            T+'if (!strcmp (text, "sendVstMidiEvent")) return 1;'+'\n'
            +T+'if (!strcmp (text, "sendVstEvents")) return 1;'+'\n')

    fcpp.write(
        T+'//if (!strcmp (text, "receiveVstEvents")) return 1;'+'\n'
        +T+'//if (!strcmp (text, "receiveVstMidiEvent")) return 1;'+'\n'
        +T+"return 0; // explicitly can't do; 0 => don't know"+'\n'
        +'}'+'\n'
        )
    
    #----------------------------------------------------------------------------
    # Plugin suspend and resume
    
    fcpp.write('//-------------------------------------------------------------'+'\n'
               +'void '+pluginLabel+'::resume()'+'\n'
               +'{'+'\n')
    
    if controlouts != []:
        fcpp.write(T+'wantEvents();'+'\n')

    fcpp.write(T+activateCode+'\n'
               +'}'+'\n'
               +'\n'
               +'void '+pluginLabel+'::suspend()'+'\n'
               +'{'+'\n'
               +T+deactivateCode+'\n'
               +'}'+'\n'
               +'\n')

    
    #----------------------------------------------------------------------------
    # Params handling

    #  setProgram
    fcpp.write('//-------------------------------------------------------------'+'\n'
               +'void '+pluginLabel+'::setProgram(long program)'+'\n'
               +'{'+'\n'
               +T+pluginLabel+'Program *ap = &programs[program];'+'\n'
               +'\n'
               +T+'curProgram = program;'+'\n')

    if params != []:
        for param in params:
            label = getText(param,"label")
            fcpp.write(T+'setParameter(k'+label+', ap->f'+label+');'+'\n')
            
    fcpp.write('}'+'\n'
               +'\n')

    #setProgramName
    fcpp.write('//-------------------------------------------------------------'+'\n'
               +'void '+pluginLabel+'::setProgramName(char *name)'+'\n'
               +'{'+'\n'
               +T+'strcpy(programs[curProgram].name, name);'+'\n'
               +'}'+'\n'
               +'\n')

    #getProgramName
    fcpp.write('//-------------------------------------------------------------'+'\n'
               +'void '+pluginLabel+'::getProgramName(char *name)'+'\n'
               +'{'+'\n'
               +T+'strcpy(name, programs[curProgram].name);'+'\n'
               +'}'+'\n'
               +'\n')

    #setParameter
    fcpp.write('//-------------------------------------------------------------'+'\n'
               +'void '+pluginLabel+'::setParameter(long index, float value)'+'\n'
               +'{'+'\n'
               +T+pluginLabel+'Program *ap = &programs[curProgram];'+'\n'
               +'\n'
               +T+'switch(index)'+'\n'
               +T+'{'+'\n')

    if params != []:
        for param in params:
            label = getText(param,'label')
            max   = label+'Max'
            min   = label+'Min'
            mapping = getText(param,'mapping')
            type = getText(param,'type')
            paramCode = getText(param,'code')
            
            fcpp.write(T*2+'case k'+label+' :'+'\n' 
                       +T*3+'f'+label+' = ap->f'+label+' = value;'+'\n')
            
            if mapping == 'lin':
                fcpp.write(T*3+label+' = ('+type+')(value*('+max+'-'+min+')+'+min+');'+'\n')            

            elif mapping == 'log':
                #    normalized = (log(param/min)) / (log(max/min))
                # => log(param/min) = normalized * log(max/min)
                # => param = min * (max/min)^normalized
                fcpp.write(T*3+label+' = ('+type+')'+min+'*pow('+max+'/'+min+',f'+label+');'+'\n')

            fcpp.write(paramCode
                       +T*2+'break;'+'\n'
                       +'\n')
               
    fcpp.write(T*3+'default: break;'+'\n'
               +T+'}'+'\n'
               +'}'+'\n'
               +'\n')
    
    #getParameter
    fcpp.write('//-------------------------------------------------------------'+'\n'
               +'float '+pluginLabel+'::getParameter(long index)'+'\n'
               +'{'+'\n'
               +T+'float v = 0.f;'+'\n'
               +'\n'
               +T+'switch(index)'+'\n'
               +T+'{'+'\n')

    if params != []:
        for param in params:
            label = getText(param,'label')
            fcpp.write(T*2+'case k'+label+' : v = f'+label+'; break;'+'\n')
            
               
    fcpp.write(T*2+'default: break;'+'\n'
               +T+'}'+'\n'
               +T+'return v;'+'\n'
               +'}'+'\n'
               +'\n')

    #getParameterName
    fcpp.write('//-------------------------------------------------------------'+'\n'
               +'void '+pluginLabel+'::getParameterName(long index, char *label)'+'\n'
               +'{'+'\n'
               +T+'switch(index)'+'\n'
               +T+'{'+'\n')

    if params != []:
        for param in params:
            label   = getText(param,'label')
            caption = getText(param,'caption')
            fcpp.write(T*2+'case k'+label+' : strcpy(label, "'+caption+'"); break;'+'\n')
                   
               
    fcpp.write(T*2+'default: break;'+'\n'
               +T+'}'+'\n'
               +'}'+'\n'
               +'\n')
    
    #getParameterDisplay
    fcpp.write('//-------------------------------------------------------------'+'\n'
               +'void '+pluginLabel+'::getParameterDisplay(long index, char *text)'+'\n'
               +'{'+'\n'
               +T+'switch(index)'+'\n'
               +T+'{'+'\n')

    if params != []:
        for param in params:
            label   = getText(param,'label')
            type    = getText(param,'type')
            if type == 'float':
                fcpp.write(T*2+'case k'+label+' : float2string('+label+', text); break;'+'\n')
            elif type == 'int':
                fcpp.write(T*2+'case k'+label+' : long2string('+label+', text); break;'+'\n')
                                           
    fcpp.write(T*2+'default: break;'+'\n'
               +T+'}'+'\n'
               +'}'+'\n'
               +'\n')

    #getParameterLabel
    fcpp.write('//-------------------------------------------------------------'+'\n'
               +'void '+pluginLabel+'::getParameterLabel(long index, char *label)'+'\n'
               +'{'+'\n'
               +T+'switch(index)'+'\n'
               +T+'{'+'\n')

    if params != []:
        for param in params:
            label   = getText(param,'label')
            unit   = getText(param,'unit')
            fcpp.write(T*2+'case k'+label+' : strcpy(label, "'+unit+'"); break;'+'\n')
                   
               
    fcpp.write(T*2+'default: break;'+'\n'
               +T+'}'+'\n'
               +'}'+'\n'
               +'\n')    

    #----------------------------------------------------------------------------
    # processing
    # process
    fcpp.write('#define XSPIF_WRITE_SAMPLE(dest,index,source) ((dest)[(index)] += (source))'+'\n'
               +'\n'
               +'//-------------------------------------------------------------'+'\n'
               +'void '+pluginLabel+'::process(float **inputs, float **outputs, long sampleframes)'+'\n'
               +'{'+'\n')

    i=0
    for pin in pins:
        dir = getText(pin,'dir')
        if dir == 'In':            
            label = getText(pin,'label')
            channels = int(str(getText(pin,'channels')))
            for j in range(0,channels):
                i = i+1
                fcpp.write(T+'float *'+label+str(j+1)+' = inputs['+str(i-1)+'];'+'\n')
        
    i=0
    for pin in pins:
        dir = getText(pin,'dir')
        if dir == 'Out':
            label = getText(pin,'label')
            channels = int(str(getText(pin,'channels')))
            for j in range(0,channels):
                i = i + 1
                fcpp.write(T+'float *'+label+str(j+1)+' = outputs['+str(i-1)+'];'+'\n')
               
               
    fcpp.write(T+'vector_size = sampleframes;'+'\n'
               +'\n'
               +processCode+'\n'
               +'}'+'\n'
               +'\n'
               +'#undef XSPIF_WRITE_SAMPLE'+'\n'
               +'\n')

    # processReplacing
    fcpp.write('#define XSPIF_WRITE_SAMPLE(dest,index,source) ((dest)[(index)] = (source))'+'\n'
               +'\n'
               +'//-------------------------------------------------------------'+'\n'
               +'void '+pluginLabel+'::processReplacing(float **inputs, float **outputs, long sampleframes)'+'\n'
               +'{'+'\n')

    i=0
    for pin in pins:
        dir = getText(pin,'dir')
        if dir == 'In':
            label = getText(pin,'label')
            channels = int(str(getText(pin,'channels')))
            for j in range(0,channels):
                i = i+1
                fcpp.write(T+'float *'+label+str(j+1)+' = inputs['+str(i-1)+'];'+'\n')
        
    i=0
    for pin in pins:
        dir = getText(pin,'dir')
        if dir == 'Out':
            label = getText(pin,'label')
            channels = int(str(getText(pin,'channels')))
            for j in range(0,channels):
                i = i+1
                fcpp.write(T+'float *'+label+str(j+1)+' = outputs['+str(i-1)+'];'+'\n')
               
    fcpp.write(T+'vector_size = sampleframes;'+'\n'
               +'\n'
               +processCode+'\n'
               +'}'+'\n'
               +'\n'
               +'#undef XSPIF_WRITE_SAMPLE'+'\n'
               +'\n')
    
    #----------------------------------------------------------------------------
    # main entry point
    
    fcpp.write(
'''
//-------------------------------------------------------------
// main entry point
//-------------------------------------------------------------
bool oome = false;
#if MAC
#pragma export on
#endif

// prototype of the export function main
#if BEOS
#define main main_plugin
extern "C" __declspec(dllexport) AEffect *main_plugin (audioMasterCallback audioMaster);

#elif MACX
#define main main_macho
extern "C" AEffect *main_macho (audioMasterCallback audioMaster);

#else
AEffect *main (audioMasterCallback audioMaster);
#endif

AEffect *main (audioMasterCallback audioMaster)
{
  // get vst version
  if (!audioMaster (0, audioMasterVersion, 0, 0, 0, 0))
    return 0;  // old version

  AudioEffect* effect = new '''+pluginLabel+'''(audioMaster);
  if (!effect)
    return 0;
  if (oome)
  {
    delete effect;
    return 0;
  }
  return effect->getAeffect ();
}

#if MAC
#pragma export off
#endif

#if WIN32
#include <windows.h>
void* hInstance;
BOOL WINAPI DllMain (HINSTANCE hInst, DWORD dwReason, LPVOID lpvReserved)
{
  hInstance = hInst;
  return 1;
}
#endif
''')

    fcpp.close
    print T+'done'    

    # def file for windows: exports the plugins entry point
    print T+'writing : '+filename_prefix+'.vst.def'
    fdef = file(filename_prefix + '.vst.def','w')

    fdef.write('LIBRARY	'+pluginLabel+'\n'
               +"DESCRIPTION '"+pluginCaption+"'"+'\n'
               +'EXPORTS main'+'\n')
    
    fdef.close
    print T+'done'    
    
    return
