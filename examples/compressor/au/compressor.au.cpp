/****************************************************************
XSPIF: cross(X) Standard PlugIn Framework: XSPIF to AudioUnits
  compressor.au.cpp


 This file is generated automatically from the file: compressor.xspif
 DO NOT EDIT BY HAND
  plugin ID: 'MCMP'
  manufacturer ID: 'mdsp'
  maker: mdsp @ smartelectronix
  copyright: GPL
 ***************************************************************/


#include <AUEffectBase.h>

// XSPIF macros
#define XSPIF_GET_SAMPLE_RATE() (GetSampleRate())
#define XSPIF_GET_VECTOR_SIZE() (vector_size)
#define XSPIF_CONTROLOUT() (// NO control out until macosx 10.3)

// <from compressor.xspif>

#include <math.h>
    

// </from compressor.xspif>
class Comp: public AUEffectBase
{
public:
  Comp(AudioUnit component);
  ~Comp();
  
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
    kattack,
    krelease,
    kthreshold,
    kratio,
    kpreamp,
    kvolume,
  
    kNumParams
  };

  static const float attackDefault = 10.0;
  static const float attackMin = 10.0;
  static const float attackMax = 50.0;
  float attack;

  static const float releaseDefault = 100.0;
  static const float releaseMin = 10.0;
  static const float releaseMax = 500.0;
  float release;

  static const float thresholdDefault = -10.0;
  static const float thresholdMin = -40.0;
  static const float thresholdMax = 0.0;
  float threshold;

  static const float ratioDefault = 6.0;
  static const float ratioMin = 1.0;
  static const float ratioMax = 40.0;
  float ratio;

  static const float preampDefault = 0.0;
  static const float preampMin = 0.0;
  static const float preampMax = 40.0;
  float preamp;

  static const float volumeDefault = 0.0;
  static const float volumeMin = -40.0;
  static const float volumeMax = 0.0;
  float volume;

  enum {
    kNumSupportedNumChannels = 2
  };

  static AUChannelInfo m_aobSupportedNumChannels[kNumSupportedNumChannels];

  OSStatus Process(const AudioBufferList& obInBuffers,
                   AudioBufferList& obOutBuffers,
                   UInt32 inFramesToProcess,
                   AudioUnitRenderActionFlags& ioactionFlags);

  // states
  float ga;
  float gr;
  float cThres;
  float cSlope;
  float boost;
  float makeup;
  float last_peak;
  float last_gain;
  float attenuation;

  long vector_size;
};


//----------------------------------------------------------------------------
// IMPLEMENTATION 
//--------------------------------------------------------------------------
        
//------------------------------------------------------
COMPONENT_ENTRY(Comp)

#define NUM_INPUTS 2
#define NUM_OUTPUTS 2
//------------------------------------------------------
AUChannelInfo Comp::m_aobSupportedNumChannels[Comp::kNumSupportedNumChannels] = {{2,2}};

//------------------------------------------------------
Comp::Comp(AudioUnit component): AUEffectBase(component)
{
  CreateElements();


  // instantiate callback
  
    ga = gr = boost = attenuation = makeup = cSlope = cThres = 0;
    last_peak = last_gain = 0;
    

  SetParameter(kattack,attackDefault);
  SetParameter(krelease,releaseDefault);
  SetParameter(kthreshold,thresholdDefault);
  SetParameter(kratio,ratioDefault);
  SetParameter(kpreamp,preampDefault);
  SetParameter(kvolume,volumeDefault);
}

//------------------------------------------------------
Comp::~Comp()
{

  // deinstantiate callback
  

}

//------------------------------------------------------
UInt32 Comp::SupportedNumChannels(const AUChannelInfo **outInfo)
{
  if(outInfo != NULL)
    *outInfo = &m_aobSupportedNumChannels[0];
  return kNumSupportedNumChannels;
}

//------------------------------------------------------
ComponentResult Comp::GetParameterInfo(AudioUnitScope inScope,
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
    case kattack:
      strcpy(pcName,"Attack");
      outParameterInfo.unit = kAudioUnitParameterUnit_Generic;
      outParameterInfo.minValue = attackMin;
      outParameterInfo.maxValue = attackMax;
      outParameterInfo.defaultValue = attackDefault;
      break;

    case krelease:
      strcpy(pcName,"Release");
      outParameterInfo.unit = kAudioUnitParameterUnit_Generic;
      outParameterInfo.minValue = releaseMin;
      outParameterInfo.maxValue = releaseMax;
      outParameterInfo.defaultValue = releaseDefault;
      break;

    case kthreshold:
      strcpy(pcName,"Threshold");
      outParameterInfo.unit = kAudioUnitParameterUnit_Generic;
      outParameterInfo.minValue = thresholdMin;
      outParameterInfo.maxValue = thresholdMax;
      outParameterInfo.defaultValue = thresholdDefault;
      break;

    case kratio:
      strcpy(pcName,"Ratio");
      outParameterInfo.unit = kAudioUnitParameterUnit_Generic;
      outParameterInfo.minValue = ratioMin;
      outParameterInfo.maxValue = ratioMax;
      outParameterInfo.defaultValue = ratioDefault;
      break;

    case kpreamp:
      strcpy(pcName,"Preamp");
      outParameterInfo.unit = kAudioUnitParameterUnit_Generic;
      outParameterInfo.minValue = preampMin;
      outParameterInfo.maxValue = preampMax;
      outParameterInfo.defaultValue = preampDefault;
      break;

    case kvolume:
      strcpy(pcName,"Volume");
      outParameterInfo.unit = kAudioUnitParameterUnit_Generic;
      outParameterInfo.minValue = volumeMin;
      outParameterInfo.maxValue = volumeMax;
      outParameterInfo.defaultValue = volumeDefault;
      break;

    default:
      result = kAudioUnitErr_InvalidParameter;
      break;
  }

  return result;
  }
//------------------------------------------------------
ComponentResult Comp::Initialize()
{
  return noErr;
}
//------------------------------------------------------
OSStatus Comp::ProcessBufferLists(AudioUnitRenderActionFlags &ioActionFlags,
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
OSStatus Comp::Process(const AudioBufferList &obInBuffers,
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
  attack = GetParameter(kattack);
  release = GetParameter(krelease);
  threshold = GetParameter(kthreshold);
  ratio = GetParameter(kratio);
  preamp = GetParameter(kpreamp);
  volume = GetParameter(kvolume);
  //updating states
  
      // 2.2 is the compensation factor to define attack time as t90-t10
      ga = (float)exp(-2.2/(XSPIF_GET_SAMPLE_RATE()*(attack*0.001))); 
      
  
      // 2.2 is the compensation factor to define attack time as t90-t10
      gr = (float)exp(-2.2/(XSPIF_GET_SAMPLE_RATE()*(release*0.001)));
      
  
      cThres = pow(10.0,threshold/20);
      makeup = pow(10.0, -(threshold*cSlope)/20.0);
      
  
      cSlope = 1.0 - 1.0/ratio; // 2:1 <-> 40:1
      makeup = pow(10.0, -(threshold*cSlope)/20.0);
      
  
      boost = pow(10.,preamp/20.0);
      
  
      attenuation = pow(10.,volume/20.0);
      
  //****************************************

    float gain, delta_peak, in1, in2;
    int i;
    for(i=0;i < XSPIF_GET_VECTOR_SIZE();i++)
    {
      in1 = boost * input1[i];
      in2 = boost * input2[i];
      
      // get peak data: 
      // if greater than last peak, add difference filtered with attack time
      // else let decay with release time
      delta_peak = 0.5*(fabs(in1) + fabs(in2)) - last_peak;
      if (delta_peak<0) delta_peak = 0;
      last_peak *= gr;
      last_peak += (1.0-ga)*delta_peak;

      if(last_peak>cThres)
	gain = pow(last_peak/cThres, - cSlope); //compression
      else 
	gain = 1.f; // no compression

      //filter w/ attack and release
      if(last_gain < gain)
	{
	  last_gain *= 1.0-ga;
	  last_gain += ga*gain;
	}
      else
	{
	  last_gain *= 1.0-gr;
	  last_gain += gr*gain;
	}
      
      // write y(n) = postamp * g(n) * makeup * x(n)
      XSPIF_WRITE_SAMPLE( output1, i, attenuation * last_gain * makeup * in1);
      XSPIF_WRITE_SAMPLE( output2, i, attenuation * last_gain * makeup * in2);
    } 
    
//****************************************

  return noErr;
}
