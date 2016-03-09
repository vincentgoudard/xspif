/****************************************************************
XSPIF: cross(X) Standard PlugIn Framework: XSPIF to AudioUnits
  lowpass.au.hpp

 A simple lowpass with saturation
 This is a comment to test the xml framework
 Some comments about Input
 Some comments about Ouput
 this is the cutoff frequency of the plugin
 This file is generated automatically from the file: lowpass.xml
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

// <from lowpass.xml>

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
    
// </from lowpass.xml>
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

  // </params>

  enum {
    kNumSupportedNumChannels = 2
  };

  static AUChannelInfo m_aobSupportedNumChannels[kNumSupportedNumChannels];

  OSStatus Process(const AudioBufferList& obInBuffers,
                   AudioBufferList& obOutBuffers,
                   UInt32 inFramesToProcess,
                   AudioUnitRenderActionFlags& ioactionFlags);

  // states
  float lp2;
  float lp1;
  float lambda;

  long vector_size;
};

/* EOF */
