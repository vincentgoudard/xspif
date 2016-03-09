/****************************************************************
XSPIF: cross(X) Standard PlugIn Framework: XSPIF to VST
  XspifDelay.vst.hpp

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

#include "audioeffectx.h"
#include <string.h>

#define XSPIF_GET_SAMPLE_RATE() (sr)
#define XSPIF_GET_VECTOR_SIZE() (vector_size)

// from XspifDelay.xml 
#include <math.h>
#include <stdlib.h>
#define MAX_DELAY 5

/*****************************************************************************/

#define LIMIT_BETWEEN_0_AND_1(x)          \
(((x) < 0) ? 0 : (((x) > 1) ? 1 : (x)))
#define LIMIT_BETWEEN_0_AND_MAX_DELAY(x)  \
(((x) < 0) ? 0 : (((x) > MAX_DELAY) ? MAX_DELAY : (x)))
    
//-------------------------------------------------------------
// Parameters constant and declarations

const double e = exp(1.0);

// Delay Length (sec)
// Delay length of the plugin
const float DelayDefault = 1;
const float DelayMin = 0.;
const float DelayMax = 5.;


// Mix dry/wet (%)
// Percentage of wet/dry in the ouput
const float DryWetDefault = 1;
const float DryWetMin = 0.;
const float DryWetMax = 1.;

enum
{
  kDelay,
  kDryWet,

  kNumParams
};

//-------------------------------------------------------------

class XspifDelay;

//-------------------------------------------------------------
//XspifDelayProgram

class XspifDelayProgram
{
friend class XspifDelay;
public:
  XspifDelayProgram();
  ~XspifDelayProgram() {}
private:
  float fDryWet; // normalized param
  float fDelay; // normalized param
  char name[24];
};

//-------------------------------------------------------------
//XspifDelay

class XspifDelay : public AudioEffectX
{
public:
  XspifDelay(audioMasterCallback audioMaster);
  ~XspifDelay();

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
  virtual void suspend();

private:
  XspifDelayProgram *programs;

  // <parameters>
  float DryWet; // param
  float fDryWet; // normalized param

  float Delay; // param
  float fDelay; // normalized param

  // </parameters>

  float sr;
  long vector_size;

  // states
  unsigned long m_lBufferSize;
  float * Buffer;
  unsigned long m_lWritePointer;
};

