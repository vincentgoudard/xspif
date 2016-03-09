/****************************************************************
XSPIF: cross(X) Standard PlugIn Framework: XSPIF to VST
  lowpass.vst.cpp

A simple lowpass with saturation
 This file is generated automatically from the file: lowpass.xspif
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
#define XSPIF_CONTROLOUT(label, index, value) (controlOut(label,index,value))

// from lowpass.xspif

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
// This is the cutoff frequency of the plugin
const float cutoffDefault = 1000.0;
const float cutoffMin = 100.0;
const float cutoffMax = 10000.0;

enum
{
  kcutoff,

  kNumParams
};


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
  virtual long canDo(char *text);
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
  float lambda;
  float lp1;
  float lp2;
};


//----------------------------------------------------------------------------
// IMPLEMENTATION 
//----------------------------------------------------------------------------

#include <stdio.h>
#include <string.h>
//-------------------------------------------------------------
// Config
#define NUM_INPUTS 2
#define NUM_OUTPUTS 2
#define NUM_PRESETS 4
//infos
#define ID 'lowp'
#define NAME "Lowpass"
#define VENDOR "Remy Muller"

#define CAN_PROCESS_REPLACING true
#define CAN_MONO true


//-------------------------------------------------------------
// LowPassProgram class implementation

LowPassProgram::LowPassProgram()
{
  fcutoff = log(cutoffDefault/cutoffMin)/(log(cutoffMax/cutoffMin));
  
  strcpy(name,"Lowpass");
}

//-------------------------------------------------------------
// LowPass class implementation

LowPass::LowPass(audioMasterCallback audioMaster)
: AudioEffectX(audioMaster, NUM_PRESETS, kNumParams)
{
  programs = new LowPassProgram[numPrograms];
  
  sr = getSampleRate();
  if(sr<0.f) sr = 44100.f;

  fcutoff = log(cutoffDefault/cutoffMin)/(log(cutoffMax/cutoffMin));

  // instantiate callback
  
	// Initialize the internal states
	lambda = lp1 = lp2 = 0.;
   	


  if(programs) setProgram(0);

  setUniqueID(ID);
  setNumInputs(NUM_INPUTS);
  setNumOutputs(NUM_OUTPUTS);
  canProcessReplacing(CAN_PROCESS_REPLACING);
  canMono(CAN_MONO);
}

//-------------------------------------------------------------
LowPass::~LowPass()
{
  if(programs)
    delete[] programs;

  // deinstantiate callback
  

}

//-------------------------------------------------------------
// LowPass information

bool LowPass::getEffectName(char *name) {
  strcpy(name, NAME); // name max 32 char
  return true;}

bool LowPass::getVendorString(char *text) {
  strcpy(text, VENDOR); // vendor max 64 char
  return true;}

long LowPass::canDo(char* text)
	{
  //if (!strcmp (text, "receiveVstEvents")) return 1;
  //if (!strcmp (text, "receiveVstMidiEvent")) return 1;
  return 0; // explicitly can't do; 0 => don't know
}
//-------------------------------------------------------------
void LowPass::resume()
{
  
}

void LowPass::suspend()
{
  
	// clears memories so that no sound is output
	// when plugin is reactivated with no input
	lp1 = lp2 = 0.;
    	
}

//-------------------------------------------------------------
void LowPass::setProgram(long program)
{
  LowPassProgram *ap = &programs[program];

  curProgram = program;
  setParameter(kcutoff, ap->fcutoff);
}

//-------------------------------------------------------------
void LowPass::setProgramName(char *name)
{
  strcpy(programs[curProgram].name, name);
}

//-------------------------------------------------------------
void LowPass::getProgramName(char *name)
{
  strcpy(name, programs[curProgram].name);
}

//-------------------------------------------------------------
void LowPass::setParameter(long index, float value)
{
  LowPassProgram *ap = &programs[curProgram];

  switch(index)
  {
    case kcutoff :
      fcutoff = ap->fcutoff = value;
      cutoff = (float)cutoffMin*pow(cutoffMax/cutoffMin,fcutoff);

      // cutoff and samplerate are both in Hertz
      lambda = exp(- cutoff / XSPIF_GET_SAMPLE_RATE()); 
          break;

      default: break;
  }
}

//-------------------------------------------------------------
float LowPass::getParameter(long index)
{
  float v = 0.f;

  switch(index)
  {
    case kcutoff : v = fcutoff; break;
    default: break;
  }
  return v;
}

//-------------------------------------------------------------
void LowPass::getParameterName(long index, char *label)
{
  switch(index)
  {
    case kcutoff : strcpy(label, "cutoff (Hz)"); break;
    default: break;
  }
}

//-------------------------------------------------------------
void LowPass::getParameterDisplay(long index, char *text)
{
  switch(index)
  {
    case kcutoff : float2string(cutoff, text); break;
    default: break;
  }
}

//-------------------------------------------------------------
void LowPass::getParameterLabel(long index, char *label)
{
  switch(index)
  {
    case kcutoff : strcpy(label, "Hz"); break;
    default: break;
  }
}

#define XSPIF_WRITE_SAMPLE(dest,index,source) ((dest)[(index)] += (source))

//-------------------------------------------------------------
void LowPass::process(float **inputs, float **outputs, long sampleframes)
{
  float *input1 = inputs[0];
  float *input2 = inputs[1];
  float *output1 = outputs[0];
  float *output2 = outputs[1];
  vector_size = sampleframes;


    int i = 0;
    for(i=0;i < XSPIF_GET_VECTOR_SIZE();i++)
    {
         // in and out names are derived from the label in the pin declaration
         lp1 = (1.f-lambda)*input1[i] + lambda*lp1;
         lp2 = (1.f-lambda)*input2[i] + lambda*lp2;
	 XSPIF_WRITE_SAMPLE(output1, i, saturate(lp1));
	 XSPIF_WRITE_SAMPLE(output2, i, saturate(lp2));  
    }
   	
}

#undef XSPIF_WRITE_SAMPLE

#define XSPIF_WRITE_SAMPLE(dest,index,source) ((dest)[(index)] = (source))

//-------------------------------------------------------------
void LowPass::processReplacing(float **inputs, float **outputs, long sampleframes)
{
  float *input1 = inputs[0];
  float *input2 = inputs[1];
  float *output1 = outputs[0];
  float *output2 = outputs[1];
  vector_size = sampleframes;


    int i = 0;
    for(i=0;i < XSPIF_GET_VECTOR_SIZE();i++)
    {
         // in and out names are derived from the label in the pin declaration
         lp1 = (1.f-lambda)*input1[i] + lambda*lp1;
         lp2 = (1.f-lambda)*input2[i] + lambda*lp2;
	 XSPIF_WRITE_SAMPLE(output1, i, saturate(lp1));
	 XSPIF_WRITE_SAMPLE(output2, i, saturate(lp2));  
    }
   	
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

  AudioEffect* effect = new LowPass(audioMaster);
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
