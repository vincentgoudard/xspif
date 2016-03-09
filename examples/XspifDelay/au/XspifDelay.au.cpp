/****************************************************************
XSPIF: cross(X) Standard PlugIn Framework: XSPIF to AU
  XspifDelay.au.cpp

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

#include "XspifDelay.au.h"

//------------------------------------------------------
COMPONENT_ENTRY(XspifDelay)

#define NUM_INPUTS 1
#define NUM_OUTPUTS 1
//------------------------------------------------------
XspifDelay::XspifDelay(AudioUnit component): AUEffectBase(component)
{
  CreateElements();


  // instantiate callback
  

    unsigned long lMinimumBufferSize;
   
    /* Buffer size is a power of two bigger than max delay time. */
    lMinimumBufferSize = (unsigned long)((float)XSPIF_GET_SAMPLE_RATE() * MAX_DELAY);
    m_lBufferSize = 1;
    while (m_lBufferSize < lMinimumBufferSize)
    	m_lBufferSize <<= 1;
	
    Buffer = (float *)malloc(m_lBufferSize * sizeof(float));
 
    m_lWritePointer = 0;
     

  SetParameter(kDryWet,DryWetDefault);
  SetParameter(kDelay,DelayDefault);
}

//------------------------------------------------------
XspifDelay::~XspifDelay()
{

  // deinstantiate callback
  
/* Throw away a simple delay line. */
	free(Buffer);

    

}

//------------------------------------------------------
UInt32 XspifDelay::SupportedNumChannels(const AUChannelInfo **outInfo)
{
  if(outInfo != NULL)
    *outInfo = &m_aobSupportedNumChannels[0];
  return kNumSupportedNumChannels;
}

//------------------------------------------------------
ComponentResult XspifDelay::GetParameterInfo(AudioUnitScope inScope,
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
    case kDryWet:
      strcpy(pcName,"Mix dry/wet (%)");
      outParameterInfo.unit = kAudioUnitParameterUnit_Generic;
      outParameterInfo.minValue = DryWetMin;
      outParameterInfo.maxValue = DryWetMax;
      outParameterInfo.defaultValue = DryWetDefault;
      break;

    case kDelay:
      strcpy(pcName,"Delay Length (sec)");
      outParameterInfo.unit = kAudioUnitParameterUnit_Generic;
      outParameterInfo.minValue = DelayMin;
      outParameterInfo.maxValue = DelayMax;
      outParameterInfo.defaultValue = DelayDefault;
      break;

    default:
      result = kAudioUnitErr_InvalidParameter;
      break;
  }

  return result;
  }
//------------------------------------------------------
ComponentResult XspifDelay::Initialize()
{
  return noErr;
}
//------------------------------------------------------
OSStatus XspifDelay::ProcessBufferLists(AudioUnitRenderActionFlags &ioActionFlags,
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
OSStatus XspifDelay::Process(const AudioBufferList &obInBuffers,
                                  AudioBufferList &obOutBuffers,
                                  UInt32 inFramesToProcess,
                                  AudioUnitRenderActionFlags &ioActionFlags)
{
  ioActionFlags &= ~kAudioUnitRenderAction_OutputIsSilence;

  const AudioBuffer &obInBuffer0 = obInBuffers.mBuffers[0];
  AudioBuffer &obOutBuffer0 = obOutBuffers.mBuffers[0];
  const Float32 *input1 = (const Float32 *)obInBuffer0.mData;
  Float32 *output1 = (Float32 *)obOutBuffer0.mData;
  vector_size = inFramesToProcess;

  // retrieve parameter values
  DryWet = GetParameter(kDryWet);
  Delay = GetParameter(kDelay);
  //****************************************

    float fDry;
    float fWet;
    float fInputSample;
    float fOutputSample;
    unsigned long lBufferReadOffset;
    unsigned long lBufferSizeMinusOne;
    unsigned long lBufferWriteOffset;
    unsigned long lDelay;
    unsigned long lSampleIndex;
    
    lBufferSizeMinusOne = m_lBufferSize - 1;
    lDelay = (unsigned long)
    (LIMIT_BETWEEN_0_AND_MAX_DELAY(Delay)*(XSPIF_GET_SAMPLE_RATE()));
    lBufferWriteOffset = m_lWritePointer;
    lBufferReadOffset = lBufferWriteOffset + m_lBufferSize - lDelay;
    fWet = LIMIT_BETWEEN_0_AND_1(DryWet);
    fDry = 1 - fWet;
 
    for(lSampleIndex = 0;
    	lSampleIndex < XSPIF_GET_VECTOR_SIZE();
	lSampleIndex++)
    {
    	fInputSample = input1[lSampleIndex];
  	fOutputSample = (fDry * fInputSample
		     + fWet * Buffer[((lSampleIndex + lBufferReadOffset)
					& lBufferSizeMinusOne)]);
	XSPIF_WRITE_SAMPLE(output1, lSampleIndex, fOutputSample);
	Buffer[((lSampleIndex + lBufferWriteOffset)
	      & lBufferSizeMinusOne)] = fInputSample;
    }
    m_lWritePointer
    	= ((m_lWritePointer + XSPIF_GET_VECTOR_SIZE())
	& lBufferSizeMinusOne);
    
//****************************************

  return noErr;
}
