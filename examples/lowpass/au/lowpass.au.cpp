/****************************************************************
XSPIF: cross(X) Standard PlugIn Framework: XSPIF to AudioUnits
  lowpass.au.cpp

A simple lowpass with saturation
 This file is generated automatically from the file: lowpass.xspif
 DO NOT EDIT BY HAND
  plugin ID: 'lowp'
  manufacturer ID: 'ReMu'
  maker: Remy Muller
  copyright: GPL
 ***************************************************************/


#include <AUEffectBase.h>

// XSPIF macros
#define XSPIF_GET_SAMPLE_RATE() (GetSampleRate())
#define XSPIF_GET_VECTOR_SIZE() (vector_size)
#define XSPIF_CONTROLOUT() (// NO control out until macosx 10.3)

// <from lowpass.xspif>

#include <math.h>
/******************************************/
/* Put all independent code here */
float saturate(float x)
{
if(x>0.f)
    x = 2.f*x-x*x;
else
    x=  2.f*x + x*x;
return x;
}
/******************************************/
    

// </from lowpass.xspif>
class LowPass: public AUEffectBase
{
public:
  LowPass(AudioUnit component);
  ~LowPass();
  
  virtual OSStatus ProcessBufferLists( AudioUnitRenderActionFlags & ioActionFlags,
                                       const AudioBufferList & inBuffer,
                                       AudioBufferList & outBuffer,
                                       UInt32 inFramesToProcess);
  
  virtual UInt32 SupportedNumChannels(const AUChannelInfo** outInfo);
  virtual ComponentResult Initialize();
  virtual ComponentResult GetParameterInfo( AudioUnitScope inScope,
                                            AudioUnitParameterID inParameterId,
                                            AudioUnitParameterInfo &outParameterInfo);
  
private:
  //params
  enum Parameters
  {
    kcutoff,
  
    kNumParams
  };

  static const float cutoffDefault = 1000.0;
  static const float cutoffMin = 100.0;
  static const float cutoffMax = 10000.0;
  float cutoff;

  enum {
    kNumSupportedNumChannels = 2
  };

  static AUChannelInfo m_aobSupportedNumChannels[kNumSupportedNumChannels];

  OSStatus Process(const AudioBufferList& obInBuffers,
                   AudioBufferList& obOutBuffers,
                   UInt32 inFramesToProcess,
                   AudioUnitRenderActionFlags& ioactionFlags);

  // states
  float lambda;
  float lp1;
  float lp2;

  long vector_size;
};

/* EOF */

        //----------------------------------------------------------------------------
        // IMPLEMENTATION 
        //--------------------------------------------------------------------------
        
        //------------------------------------------------------
COMPONENT_ENTRY(LowPass)

#define NUM_INPUTS 2
#define NUM_OUTPUTS 2
//------------------------------------------------------
AUChannelInfo LowPass::m_aobSupportedNumChannels[LowPass::kNumSupportedNumChannels] = {{2,2}};

//------------------------------------------------------
LowPass::LowPass(AudioUnit component): AUEffectBase(component)
{
  CreateElements();


  // instantiate callback
  
	// Initialize the internal states
	lambda = lp1 = lp2 = 0.;
   	

  SetParameter(kcutoff,cutoffDefault);
}

//------------------------------------------------------
LowPass::~LowPass()
{

  // deinstantiate callback
  

}

//------------------------------------------------------
UInt32 LowPass::SupportedNumChannels(const AUChannelInfo **outInfo)
{
  if(outInfo != NULL)
    *outInfo = &m_aobSupportedNumChannels[0];
  return kNumSupportedNumChannels;
}

//------------------------------------------------------
ComponentResult LowPass::GetParameterInfo(AudioUnitScope inScope,
                                                  AudioUnitParameterID inParameterID,
                                                  AudioUnitParameterInfo &outParameterInfo)
{
  if(inScope != kAudioUnitScope_Global)
    return kAudioUnitErr_InvalidParameter;

  ComponentResult result = noErr;

  outParameterInfo.flags = kAudioUnitParameterFlag_IsWritable | kAudioUnitParameterFlag_IsReadable | kAudioUnitParameterFlag_Global;

  char *pcName = outParameterInfo.name;

  switch(inParameterID)
  {
    case kcutoff:
      strcpy(pcName,"cutoff (Hz)");
      outParameterInfo.unit = kAudioUnitParameterUnit_Generic;
      outParameterInfo.minValue = cutoffMin;
      outParameterInfo.maxValue = cutoffMax;
      outParameterInfo.defaultValue = cutoffDefault;
      break;

    default:
      result = kAudioUnitErr_InvalidParameter;
      break;
  }

  return result;
  }
//------------------------------------------------------
ComponentResult LowPass::Initialize()
{
  return noErr;
}
//------------------------------------------------------
OSStatus LowPass::ProcessBufferLists(AudioUnitRenderActionFlags &ioActionFlags,
                                             const AudioBufferList &inBuffer,
                                             AudioBufferList &outBuffer,
                                             UInt32 inFramesToProcess)
{
  ioActionFlags |= kAudioUnitRenderAction_OutputIsSilence;

  UInt32 uiInBuffers = inBuffer.mNumberBuffers;
  UInt32 uiOutBuffers = outBuffer.mNumberBuffers;

  if(uiInBuffers != NUM_INPUTS || uiOutBuffers != NUM_OUTPUTS)
    return kAudioUnitErr_FormatNotSupported;

  return Process(inBuffer, outBuffer, inFramesToProcess, ioActionFlags);
}

#define XSPIF_WRITE_SAMPLE(dest,index,source) ((dest)[(index)] = (source))

//------------------------------------------------------
OSStatus LowPass::Process(const AudioBufferList &obInBuffers,
                                  AudioBufferList &obOutBuffers,
                                  UInt32 inFramesToProcess,
                                  AudioUnitRenderActionFlags &ioActionFlags)
{
  ioActionFlags &= ~kAudioUnitRenderAction_OutputIsSilence;

  const AudioBuffer &obInBuffer0 = obInBuffers.mBuffers[0];
  const AudioBuffer &obInBuffer1 = obInBuffers.mBuffers[1];
  AudioBuffer &obOutBuffer0 = obOutBuffers.mBuffers[0];
  AudioBuffer &obOutBuffer1 = obOutBuffers.mBuffers[1];
  const Float32 *input1 = (const Float32 *)obInBuffer0.mData;
  const Float32 *input2 = (const Float32 *)obInBuffer1.mData;
  Float32 *output1 = (Float32 *)obOutBuffer0.mData;
  Float32 *output2 = (Float32 *)obOutBuffer1.mData;
  vector_size = inFramesToProcess;

  //retrieving params
  cutoff = GetParameter(kcutoff);
  //updating states
  
      // cutoff and samplerate are both in Hertz
      lambda = exp(- cutoff / XSPIF_GET_SAMPLE_RATE()); 
      
  //****************************************

    int i = 0;
    for(i=0;i < XSPIF_GET_VECTOR_SIZE();i++)
    {
         // in and out names are derived from the label in the pin declaration
         lp1 = (1.f-lambda)*input1[i] + lambda*lp1;
         lp2 = (1.f-lambda)*input2[i] + lambda*lp2;
	 XSPIF_WRITE_SAMPLE(output1, i, saturate(lp1));
	 XSPIF_WRITE_SAMPLE(output2, i, saturate(lp2));  
    }
   	
//****************************************

  return noErr;
}
