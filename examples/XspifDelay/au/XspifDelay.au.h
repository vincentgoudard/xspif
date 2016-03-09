/****************************************************************
XSPIF: cross(X) Standard PlugIn Framework: XSPIF to AudioUnits
  XspifDelay.au.hpp

 A simple delay
 It is based on the delay implemented by Richard W.E. Furse for LADSPA.
 Some comments about Input
 Some comments about Ouput
 Delay length of the plugin
 Percentage of wet/dry in the ouput
 This file is generated automatically from the file: XspifDelay.xml
 DO NOT EDIT BY HAND
  plugin ID: 'dlay'
  manufacturer ID: 'ViGo'
  maker: Vincent Goudard
  copyright: GPL
 ***************************************************************/


#include <AUEffectBase.h>

// XSPIF macros
#define XSPIF_GET_SAMPLE_RATE() (GetSampleRate())
#define XSPIF_GET_VECTOR_SIZE() (vector_size)

// <from XspifDelay.xml>

#include <math.h>
#include <stdlib.h>
#define MAX_DELAY 5

/*****************************************************************************/

#define LIMIT_BETWEEN_0_AND_1(x)          \
(((x) < 0) ? 0 : (((x) > 1) ? 1 : (x)))
#define LIMIT_BETWEEN_0_AND_MAX_DELAY(x)  \
(((x) < 0) ? 0 : (((x) > MAX_DELAY) ? MAX_DELAY : (x)))
    
// </from XspifDelay.xml>
class XspifDelay: public AUEffectBase
{
public:
  XspifDelay(AudioUnit component);
  ~XspifDelay();
  
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
    kDryWet,
    kDelay,
  
    kNumParams
  };

  static const float DryWetDefault = 1;
  static const float DryWetMin = 0.;
  static const float DryWetMax = 1.;
  float DryWet;

  static const float DelayDefault = 1;
  static const float DelayMin = 0.;
  static const float DelayMax = 5.;
  float Delay;

  // </params>

  enum {
    kNumSupportedNumChannels = 1
  };

  static AUChannelInfo m_aobSupportedNumChannels[kNumSupportedNumChannels];

  OSStatus Process(const AudioBufferList& obInBuffers,
                   AudioBufferList& obOutBuffers,
                   UInt32 inFramesToProcess,
                   AudioUnitRenderActionFlags& ioactionFlags);

  // states
  unsigned long m_lBufferSize;
  float * Buffer;
  unsigned long m_lWritePointer;

  long vector_size;
};

/* EOF */
