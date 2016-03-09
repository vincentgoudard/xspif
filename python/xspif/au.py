#-----------------------------------------------------------------------
# XSPIF: a (X)cross Standard PlugIn Framework
# Copyright (C) 2003 IRCAM - Centre Pompidou
# Authors: Remy Muller and Vincent Goudard
# Module xspif.au : XSPIF to AudioUnits translator
#-----------------------------------------------------------------------


from xspif.parsexml import getText

tab = 2
T = ' '*tab

def write(plugin,filename_prefix):
    fcpp = file(filename_prefix + '.au.cpp','w')
    xml_filename  = filename_prefix + ".xspif"
    print T+'writing : '+filename_prefix+'.au.cpp'

   ######## independent code here ############

    # Variables
    plugId        = getText(plugin,'plugId')
    manufId       = getText(plugin,'manufId')
    maker         = getText(plugin,'maker')
    pluginLabel   = getText(plugin,'label')
    pluginLabel.replace(' ', '') #remove spaces in
    pluginLabel.title(); # forces the first letter to upper case
    copyright     = getText(plugin,'copyright')
    comment = getText(plugin,'comment')+'\n'
    pluginCode = getText(plugin,'code')+'\n'
    pluginCaption = getText(plugin,'caption')

    params = plugin.getElementsByTagName('param')    
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
        + 'XSPIF to AudioUnits\n'
        + T+filename_prefix+'.au.cpp'+'\n\n'
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

    #includes and independent code
    fcpp.write('\n'
             +'#include <AUEffectBase.h>'+'\n'
             +'\n'
             +'// XSPIF macros'+'\n'
             +'#define XSPIF_GET_SAMPLE_RATE() (GetSampleRate())'+'\n'
             +'#define XSPIF_GET_VECTOR_SIZE() (vector_size)'+'\n'
             +'#define XSPIF_CONTROLOUT() (// NO control out until macosx 10.3)'+'\n'
             +'\n'
             +'// <from '+xml_filename+'>'+'\n'
             +pluginCode+'\n'
             +'// </from '+xml_filename+'>'+'\n')

    #----------------------------------------------------------------------------
    # Class declaration (TODO:change the base according to the purpose)

    fcpp.write('class '+pluginLabel+': public AUEffectBase'+'\n'
               +'{'+'\n'
               +'public:'+'\n'
               +T+pluginLabel+'(AudioUnit component);'+'\n'
               +T+'~'+pluginLabel+'();'+'\n'
               +T+''+'\n'
               +T+'virtual OSStatus ProcessBufferLists( AudioUnitRenderActionFlags & ioActionFlags,'+'\n'
               +T+'                                     const AudioBufferList & inBuffer,'+'\n'
               +T+'                                     AudioBufferList & outBuffer,'+'\n'
               +T+'                                     UInt32 inFramesToProcess);'+'\n'
               +T+''+'\n'
               +T+'virtual UInt32 SupportedNumChannels(const AUChannelInfo** outInfo);'+'\n'
               +T+'virtual ComponentResult Initialize();'+'\n'
               +T+'virtual ComponentResult GetParameterInfo( AudioUnitScope inScope,'+'\n'
               +T+'                                          AudioUnitParameterID inParameterId,'+'\n'
               +T+'                                          AudioUnitParameterInfo &outParameterInfo);'+'\n'
               +T+''+'\n'
               +'private:'+'\n'
               )
    
    # declare params
    if params != []:
        fcpp.write(T+'//params'+'\n'
                   +T+'enum Parameters'+'\n'
                   +T+'{'+'\n')
        
        for param in params:
            label   = getText(param,'label')
            fcpp.write(T*2+'k'+label+','+'\n')

        fcpp.write(T+''+'\n'
                   +T*2+'kNumParams'+'\n'
                   +T+'};'+'\n'
                   +'\n')

        for param in params:
            label   = getText(param,'label')
            default = getText(param,'default')
            min     = getText(param,'min')
            max     = getText(param,'max')
            fcpp.write(T+'static const float '+label+'Default = '+default+';'+'\n'
                     +T+'static const float '+label+'Min = '+min+';'+'\n'
                     +T+'static const float '+label+'Max = '+max+';'+'\n'
                     +T+'float '+label+';'+'\n'
                     +'\n')

    # declare supported  number of channels
    numInputs = numOutputs = 0
    
    for pin in pins:
        dir      = getText(pin,'dir')
        channels = int(str(getText(pin,'channels')))
        if dir == 'In':
            numInputs += channels
        elif dir == 'Out':
            numOutputs += channels

    if numInputs < numOutputs:
        numchannels = numInputs
    else:
        numchannels = numOutputs
        
    numchannels = str(numchannels)
    numInputs  = str(numInputs)
    numOutputs = str(numOutputs)

    
    fcpp.write(T+'enum {'+'\n'
             +T*2+'kNumSupportedNumChannels = '+numchannels+'\n'
             +T+'};'+'\n'
             +'\n'
             +T+'static AUChannelInfo m_aobSupportedNumChannels[kNumSupportedNumChannels];'+'\n'
             +'\n'
             )
    
    # process declaration
    fcpp.write(T+'OSStatus Process(const AudioBufferList& obInBuffers,'+'\n'
             +T+'                 AudioBufferList& obOutBuffers,'+'\n'
             +T+'                 UInt32 inFramesToProcess,'+'\n'
             +T+'                 AudioUnitRenderActionFlags& ioactionFlags);'+'\n'
             +'\n'
             )
    
    # states
    if states != []:
        fcpp.write(T+'// states'+'\n')
    
        for state in states:
            label = getText(state,'label')
            type  = getText(state,'type')
            fcpp.write(T+type+' '+label+';'+'\n')
                
    fcpp.write('\n'
             +T+'long vector_size;'+'\n'
             +'};'+'\n'
             +'\n'
             )
    
    #----------------------------------------------------------------------------
    # CPP file
    #--------------------------------------------------------------------------
    fcpp.write(
"""
//----------------------------------------------------------------------------
// IMPLEMENTATION 
//--------------------------------------------------------------------------
        
""")

    #--------------------------------------------------------------------------
    fcpp.write('//------------------------------------------------------'+'\n'
               +'COMPONENT_ENTRY('+pluginLabel+')'+'\n'
               +'\n'
               )
    
    #--------------------------------------------------------------------------
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

    fcpp.write('#define NUM_INPUTS '+numInputs+'\n'
               +'#define NUM_OUTPUTS '+numOutputs+'\n'
               )

    fcpp.write('//------------------------------------------------------'+'\n'
               +'AUChannelInfo '+pluginLabel+'::m_aobSupportedNumChannels['+pluginLabel+'::kNumSupportedNumChannels] = {{'+numInputs+','+numOutputs+'}};'+'\n'
               +'\n'
               )
    
    #--------------------------------------------------------------------------
    # Plugin Class
    # Plugin Constructor
    fcpp.write('//------------------------------------------------------'+'\n'
               +pluginLabel+'::'+pluginLabel+'(AudioUnit component): AUEffectBase(component)'+'\n'
               +'{'+'\n'
               +T+'CreateElements();'+'\n'
               +'\n')

    fcpp.write('\n'
               +T+'// instantiate callback'+'\n'
               +T+instantiateCode+'\n'
               +'\n')

    if params != []:
         for param in params:
            label   = getText(param,'label')
            fcpp.write(T+'SetParameter(k'+label+','+label+'Default);'+'\n')

    fcpp.write('}'+'\n'
               +'\n')

    # Plugin Deconstructor
    fcpp.write('//------------------------------------------------------'+'\n'
               +pluginLabel+'::~'+pluginLabel+'()'+'\n'
               +'{'+'\n'
               )
    
    fcpp.write('\n'
               +T+'// deinstantiate callback'+'\n'
               +T+deinstantiateCode+'\n'
               +'\n')

    fcpp.write('}'+'\n'
               +'\n')
    
    # Plugin infos
    fcpp.write('//------------------------------------------------------'+'\n'
               +'UInt32 '+pluginLabel+'::SupportedNumChannels(const AUChannelInfo **outInfo)'+'\n'
               +'{'+'\n'
               +T+'if(outInfo != NULL)'+'\n'
               +T*2+'*outInfo = &m_aobSupportedNumChannels[0];'+'\n'
               +T+'return kNumSupportedNumChannels;'+'\n'
               +'}'+'\n'
               +'\n'
               )

    fcpp.write('//------------------------------------------------------'+'\n'
               +'ComponentResult '+pluginLabel+'::GetParameterInfo(AudioUnitScope inScope,'+'\n'
               +'                                                  AudioUnitParameterID inParameterID,'+'\n'
               +'                                                  AudioUnitParameterInfo &outParameterInfo)'+'\n'
               +'{'+'\n'
               +T+'if(inScope != kAudioUnitScope_Global)'+'\n'
               +T*2+'return kAudioUnitErr_InvalidParameter;'+'\n'
               +'\n'
               +T+'ComponentResult result = noErr;'+'\n'
               +'\n'
               +T+'outParameterInfo.flags = kAudioUnitParameterFlag_IsWritable | kAudioUnitParameterFlag_IsReadable | kAudioUnitParameterFlag_Global;'+'\n'
               +'\n'
               +T+'char *pcName = outParameterInfo.name;'+'\n'
               +'\n'
               +T+'switch(inParameterID)'+'\n'
               +T+'{'+'\n')
    if params != []:
         for param in params:
            label   = getText(param,'label')
            caption = getText(param,'caption')
            fcpp.write(T*2+'case k'+label+':'+'\n'
                       +T*3+'strcpy(pcName,"'+caption+'");'+'\n'
                       +T*3+'outParameterInfo.unit = kAudioUnitParameterUnit_Generic;'+'\n'
                       +T*3+'outParameterInfo.minValue = '+label+'Min;'+'\n'
                       +T*3+'outParameterInfo.maxValue = '+label+'Max;'+'\n'
                       +T*3+'outParameterInfo.defaultValue = '+label+'Default;'+'\n'
                       +T*3+'break;'+'\n'
                       +'\n'
                       )
                
    fcpp.write(T*2+'default:'+'\n'
               +T*3+'result = kAudioUnitErr_InvalidParameter;'+'\n'
               +T*3+'break;'+'\n'
               +T+'}'+'\n'
               +'\n'
               +T+'return result;'+'\n'
               +T+'}'+'\n'
               )
    
    # Plugin suspend and resume
    fcpp.write('//------------------------------------------------------'+'\n'
               +'ComponentResult '+pluginLabel+'::Initialize()'+'\n'
               +'{'+'\n'
               +T+'return noErr;'+'\n'
               +'}'+'\n')
               

    #--------------------------------------------------------------------------
    # processing
    fcpp.write('//------------------------------------------------------'+'\n'
               +'OSStatus '+pluginLabel+'::ProcessBufferLists(AudioUnitRenderActionFlags &ioActionFlags,'+'\n'
               +'                                             const AudioBufferList &inBuffer,'+'\n'
               +'                                             AudioBufferList &outBuffer,'+'\n'
               +'                                             UInt32 inFramesToProcess)'+'\n'
               +'{'+'\n'
               +T+'ioActionFlags |= kAudioUnitRenderAction_OutputIsSilence;'+'\n'
               +'\n'
               +T+'UInt32 uiInBuffers = inBuffer.mNumberBuffers;'+'\n'
               +T+'UInt32 uiOutBuffers = outBuffer.mNumberBuffers;'+'\n'
               +'\n'
               +T+'if(uiInBuffers != NUM_INPUTS || uiOutBuffers != NUM_OUTPUTS)'+'\n'
               +T*2+'return kAudioUnitErr_FormatNotSupported;'+'\n'
               +'\n'
               +T+'return Process(inBuffer, outBuffer, inFramesToProcess, ioActionFlags);'+'\n'
               +'}'+'\n'
               +'\n')

    fcpp.write('#define XSPIF_WRITE_SAMPLE(dest,index,source) ((dest)[(index)] = (source))'+'\n'
               +'\n')

    fcpp.write('//------------------------------------------------------'+'\n'
               +'OSStatus '+pluginLabel+'::Process(const AudioBufferList &obInBuffers,'+'\n'
               +'                                  AudioBufferList &obOutBuffers,'+'\n'
               +'                                  UInt32 inFramesToProcess,'+'\n'
               +'                                  AudioUnitRenderActionFlags &ioActionFlags)'+'\n'
               +'{'+'\n'
               +T+'ioActionFlags &= ~kAudioUnitRenderAction_OutputIsSilence;'+'\n'
               +'\n')

    for i in range(0,int(numInputs)):
               fcpp.write(T+'const AudioBuffer &obInBuffer'+str(i)+' = obInBuffers.mBuffers['+str(i)+'];'+'\n')

    for i in range(0,int(numOutputs)):
               fcpp.write(T+'AudioBuffer &obOutBuffer'+str(i)+' = obOutBuffers.mBuffers['+str(i)+'];'+'\n')

    i=0
    for pin in pins:
        dir   = getText(pin,'dir')
        if dir == 'In':
            i = i+1
            label = getText(pin,'label')
            channels = int(str(getText(pin,'channels')))
            for j in range(0,channels):
                fcpp.write(T+'const Float32 *'+label+str(i+j)+' = (const Float32 *)obInBuffer'+str(i+j-1)+'.mData;'+'\n')

    i=0
    for pin in pins:
        dir   = getText(pin,'dir')
        if dir == 'Out':
            i = i+1
            label = getText(pin,'label')
            channels = int(str(getText(pin,'channels')))
            for j in range(0,channels):
                fcpp.write(T+'Float32 *'+label+str(i+j)+' = (Float32 *)obOutBuffer'+str(i+j-1)+'.mData;'+'\n')            

    fcpp.write(T+'vector_size = inFramesToProcess;'+'\n'
               +'\n'
               )

    if params != []:
        fcpp.write(T+'//retrieving params'+'\n')
        for param in params:
            label   = getText(param,'label')
            fcpp.write(T+label+' = GetParameter(k'+label+');'+'\n')

        fcpp.write(T+'//updating states'+'\n')
        for param in params:
            paramCode = getText(param,'code')
            fcpp.write(T+paramCode+'\n')

    fcpp.write(T+'//****************************************'+'\n'
               +processCode+'\n'
               +'//****************************************'+'\n'
               +'\n'
               +T+'return noErr;'+'\n'
               +'}'+'\n'
               )

    fcpp.close
    print T+'done'
    
    #--------------------------------------------------------------------------
    # r
    fr = file(filename_prefix + '.au.r','w')
    print T+'writing : '+filename_prefix+'.au.r'

    fr.write('#include <AudioUnit/AudioUnit.r>'+'\n'
             +'\n'
             +'// Note that resource IDs must be spaced 2 apart for the '+"'STR'"+' name and description'+'\n'
             +'#define kAudioUnitResID_'+pluginLabel+'				10000'+'\n'
             +'\n'
             +'// So you need to define these appropriately for your audio unit.'+'\n'
             +"// For the name the convention is to provide your company name and end it with a ':',"+'\n'
             +'// then provide the name of the AudioUnit.'+'\n'
             +'// The Description can be whatever you want.'+'\n'
             +'// For an effect unit the Type and SubType should be left the way they are defined here...'+'\n'
             +'//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'+'\n'
             +'// SampleEffectUnit'+'\n'
             +'#define RES_ID			kAudioUnitResID_'+pluginLabel+'\n'
             +'#define COMP_TYPE		'+"'aufx'"+'\n'
             +'#define COMP_SUBTYPE		'+plugId+'\n'
             +'#define COMP_MANUF		'+manufId+'\n' 	
             +'#define VERSION			0x00010000'+'\n'
             +'#define NAME			"'+maker+': '+pluginCaption+'"'+'\n'
             +'#define DESCRIPTION		"'+pluginCaption+'"'+'\n'
             +'#define ENTRY_POINT		"'+pluginLabel+'Entry"'+'\n'
             +'\n'
             +'#include "AUResources.r"'+'\n'
             )    
    fr.close

    print T+'done'

    fexp = file(filename_prefix + '.exp','w')
    print T+'writing : '+filename_prefix+'.exp'
    fexp.write('_'+pluginLabel+'Entry')
    fexp.close
    print T+'done'
    
    return
