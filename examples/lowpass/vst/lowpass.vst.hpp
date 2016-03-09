/****************************************************************
XSPIF: cross(X) Standard PlugIn Framework: XSPIF to VST
  lowpass.vst.hpp

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

#include "audioeffectx.h"
#include <string.h>

#define XSPIF_GET_SAMPLE_RATE() (sr)
#define XSPIF_GET_VECTOR_SIZE() (vector_size)

// from lowpass.xml 
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
    
//-------------------------------------------------------------
// Parameters constant and declarations

const double e = exp(1.0);

// cutoff (Hz)
// this is the cutoff frequency of the plugin
const float cutoffDefault = 1000.0;
const float cutoffMin = 100.0;
const float cutoffMax = 10000.0;

enum
{
  kcutoff,

  kNumParams
};

//-------------------------------------------------------------

class LowPass;

//-------------------------------------------------------------
//LowPassProgram

class LowPassProgram
{
friend class LowPass;
public:
  LowPassProgram();
  ~LowPassProgram() {}
private:
  float fcutoff; // normalized param
  char name[24];
};

//-------------------------------------------------------------
//LowPass

class LowPass : public AudioEffectX
{
public:
  LowPass(audioMasterCallback audioMaster);
  ~LowPass();

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
  LowPassProgram *programs;

  // <parameters>
  float cutoff; // param
  float fcutoff; // normalized param

  // </parameters>

  float sr;
  long vector_size;

  // states
  float lp2;
  float lp1;
  float lambda;
};

