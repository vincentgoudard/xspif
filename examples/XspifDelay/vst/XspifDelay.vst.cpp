/****************************************************************
XSPIF: cross(X) Standard PlugIn Framework: XSPIF to VST
  XspifDelay.vst.cpp

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

#include <stdio.h>
#include <string.h>
#include "XspifDelay.vst.hpp"
//-------------------------------------------------------------
// Config
#define NUM_INPUTS 1
#define NUM_OUTPUTS 1
#define NUM_PRESETS 4
//infos
#define ID 'dlay'
#define NAME "Delay"
#define VENDOR "Vincent Goudard"

#define CAN_PROCESS_REPLACING true
#define CAN_MONO true


//-------------------------------------------------------------
// XspifDelayProgram class implementation

XspifDelayProgram::XspifDelayProgram()
{
  fDryWet = (DryWetDefault-DryWetMin)/(DryWetMax-DryWetMin);
  fDelay = (DelayDefault-DelayMin)/(DelayMax-DelayMin);
  
  strcpy(name,"Delay");
}

//-------------------------------------------------------------
// XspifDelay class implementation

XspifDelay::XspifDelay(audioMasterCallback audioMaster)
: AudioEffectX(audioMaster, NUM_PRESETS, kNumParams)
{
  programs = new XspifDelayProgram[numPrograms];
  
  sr = getSampleRate();
  if(sr<0.f) sr = 44100.f;

  fDryWet = (DryWetDefault-DryWetMin)/(DryWetMax-DryWetMin);
  DryWet = DryWetDefault;
  fDelay = (DelayDefault-DelayMin)/(DelayMax-DelayMin);
  Delay = DelayDefault;

  // instantiate callback
  

    unsigned long lMinimumBufferSize;
   
    /* Buffer size is a power of two bigger than max delay time. */
    lMinimumBufferSize = (unsigned long)((float)XSPIF_GET_SAMPLE_RATE() * MAX_DELAY);
    m_lBufferSize = 1;
    while (m_lBufferSize < lMinimumBufferSize)
    	m_lBufferSize <<= 1;
	
    Buffer = (float *)malloc(m_lBufferSize * sizeof(float));
 
    m_lWritePointer = 0;
     

  if(programs) setProgram(0);

  setUniqueID(ID);
  setNumInputs(NUM_INPUTS);
  setNumOutputs(NUM_OUTPUTS);
  canProcessReplacing(CAN_PROCESS_REPLACING);
  canMono(CAN_MONO);
}

//-------------------------------------------------------------
XspifDelay::~XspifDelay()
{
  if(programs)
    delete[] programs;

  // deinstantiate callback
  
/* Throw away a simple delay line. */
	free(Buffer);

    

}

//-------------------------------------------------------------
// XspifDelay information

bool XspifDelay::getEffectName(char *name) {
  strcpy(name, NAME); // name max 32 char
  return true;}

bool XspifDelay::getVendorString(char *text) {
  strcpy(text, VENDOR); // vendor max 64 char
  return true;}

//-------------------------------------------------------------
void XspifDelay::resume()
{
  
/* Need to reset the delay history in this function rather than
     instantiate() in case deactivate() followed by activate() have
     been called to reinitialise a delay line. */
  memset(Buffer, 0, sizeof(float) * m_lBufferSize);

    
}

void XspifDelay::suspend()
{
  
    //clears internal states
    
}

//-------------------------------------------------------------
void XspifDelay::setProgram(long program)
{
  XspifDelayProgram *ap = &programs[program];

  curProgram = program;
  setParameter(kDryWet, ap->fDryWet);
  setParameter(kDelay, ap->fDelay);
}

//-------------------------------------------------------------
void XspifDelay::setProgramName(char *name)
{
  strcpy(programs[curProgram].name, name);
}

//-------------------------------------------------------------
void XspifDelay::getProgramName(char *name)
{
  strcpy(name, programs[curProgram].name);
}

//-------------------------------------------------------------
void XspifDelay::setParameter(long index, float value)
{
  XspifDelayProgram *ap = &programs[curProgram];

  switch(index)
  {
    case kDryWet :
      fDryWet = ap->fDryWet = value;
      DryWet = value*(DryWetMax-DryWetMin)+DryWetMin;

          break;

    case kDelay :
      fDelay = ap->fDelay = value;
      Delay = value*(DelayMax-DelayMin)+DelayMin;

          break;

      default: break;
  }
}

//-------------------------------------------------------------
float XspifDelay::getParameter(long index)
{
  float v = 0.f;

  switch(index)
  {
    case kDryWet : v = fDryWet; break;
    case kDelay : v = fDelay; break;
    default: break;
  }
  return v;
}

//-------------------------------------------------------------
void XspifDelay::getParameterName(long index, char *label)
{
  switch(index)
  {
    case kDryWet : strcpy(label, "Mix dry/wet (%)"); break;
    case kDelay : strcpy(label, "Delay Length (sec)"); break;
    default: break;
  }
}

//-------------------------------------------------------------
void XspifDelay::getParameterDisplay(long index, char *text)
{
  switch(index)
  {
    case kDryWet : float2string(DryWet, text); break;
    case kDelay : float2string(Delay, text); break;
    default: break;
  }
}

//-------------------------------------------------------------
void XspifDelay::getParameterLabel(long index, char *label)
{
  switch(index)
  {
    case kDryWet : strcpy(label, "%"); break;
    case kDelay : strcpy(label, "Second"); break;
    default: break;
  }
}

#define XSPIF_WRITE_SAMPLE(dest,index,source) ((dest)[(index)] += (source))

//-------------------------------------------------------------
void XspifDelay::process(float **inputs, float **outputs, long sampleframes)
{
  float *input1 = inputs[0];
  float *output1 = outputs[0];
  vector_size = sampleframes;


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
    
}

#undef XSPIF_WRITE_SAMPLE

#define XSPIF_WRITE_SAMPLE(dest,index,source) ((dest)[(index)] = (source))

//-------------------------------------------------------------
void XspifDelay::processReplacing(float **inputs, float **outputs, long sampleframes)
{
  float *input1 = inputs[0];
  float *output1 = outputs[0];
  vector_size = sampleframes;


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
    
}

#undef XSPIF_WRITE_SAMPLE


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

  AudioEffect* effect = new XspifDelay (audioMaster);
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

