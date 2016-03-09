/****************************************************************
XSPIF: cross(X) Standard PlugIn Framework: XSPIF to VST
  compressor.vst.cpp


 This file is generated automatically from the file: compressor.xspif
 DO NOT EDIT BY HAND
  plugin ID: 'MCMP'
  manufacturer ID: 'mdsp'
  maker: mdsp @ smartelectronix
  copyright: GPL
 ***************************************************************/

#include "audioeffectx.h"
#include <string.h>

#define XSPIF_GET_SAMPLE_RATE() (sr)
#define XSPIF_GET_VECTOR_SIZE() (vector_size)
#define XSPIF_CONTROLOUT(label, index, value) (controlOut(label,index,value))

// from compressor.xspif

#include <math.h>
    

//-------------------------------------------------------------
// Parameters constant and declarations

const double e = exp(1.0);

// Attack
// 
const float attackDefault = 10.0;
const float attackMin = 10.0;
const float attackMax = 50.0;


// Release
// 
const float releaseDefault = 100.0;
const float releaseMin = 10.0;
const float releaseMax = 500.0;


// Threshold
// 
const float thresholdDefault = -10.0;
const float thresholdMin = -40.0;
const float thresholdMax = 0.0;


// Ratio
// 
const float ratioDefault = 6.0;
const float ratioMin = 1.0;
const float ratioMax = 40.0;


// Preamp
// 
const float preampDefault = 0.0;
const float preampMin = 0.0;
const float preampMax = 40.0;


// Volume
// 
const float volumeDefault = 0.0;
const float volumeMin = -40.0;
const float volumeMax = 0.0;

enum
{
  kattack,
  krelease,
  kthreshold,
  kratio,
  kpreamp,
  kvolume,

  kNumParams
};


class Comp;

//-------------------------------------------------------------
//CompProgram

class CompProgram
{
friend class Comp;
public:
  CompProgram();
  ~CompProgram() {}
private:
  float fattack; // normalized param
  float frelease; // normalized param
  float fthreshold; // normalized param
  float fratio; // normalized param
  float fpreamp; // normalized param
  float fvolume; // normalized param
  char name[24];
};


//-------------------------------------------------------------
//Comp

class Comp : public AudioEffectX
{
public:
  Comp(audioMasterCallback audioMaster);
  ~Comp();

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
  CompProgram *programs;

  // <parameters>
  float attack; // param
  float fattack; // normalized param

  float release; // param
  float frelease; // normalized param

  float threshold; // param
  float fthreshold; // normalized param

  float ratio; // param
  float fratio; // normalized param

  float preamp; // param
  float fpreamp; // normalized param

  float volume; // param
  float fvolume; // normalized param

  // </parameters>

  float sr;
  long vector_size;

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
#define ID 'MCMP'
#define NAME "Compressor"
#define VENDOR "mdsp @ smartelectronix"

#define CAN_PROCESS_REPLACING true
#define CAN_MONO true


//-------------------------------------------------------------
// CompProgram class implementation

CompProgram::CompProgram()
{
  fattack = (attackDefault-attackMin)/(attackMax-attackMin);
  frelease = (releaseDefault-releaseMin)/(releaseMax-releaseMin);
  fthreshold = (thresholdDefault-thresholdMin)/(thresholdMax-thresholdMin);
  fratio = (ratioDefault-ratioMin)/(ratioMax-ratioMin);
  fpreamp = (preampDefault-preampMin)/(preampMax-preampMin);
  fvolume = (volumeDefault-volumeMin)/(volumeMax-volumeMin);
  
  strcpy(name,"Compressor");
}

//-------------------------------------------------------------
// Comp class implementation

Comp::Comp(audioMasterCallback audioMaster)
: AudioEffectX(audioMaster, NUM_PRESETS, kNumParams)
{
  programs = new CompProgram[numPrograms];
  
  sr = getSampleRate();
  if(sr<0.f) sr = 44100.f;

  fattack = (attackDefault-attackMin)/(attackMax-attackMin);
  attack = attackDefault;
  frelease = (releaseDefault-releaseMin)/(releaseMax-releaseMin);
  release = releaseDefault;
  fthreshold = (thresholdDefault-thresholdMin)/(thresholdMax-thresholdMin);
  threshold = thresholdDefault;
  fratio = (ratioDefault-ratioMin)/(ratioMax-ratioMin);
  ratio = ratioDefault;
  fpreamp = (preampDefault-preampMin)/(preampMax-preampMin);
  preamp = preampDefault;
  fvolume = (volumeDefault-volumeMin)/(volumeMax-volumeMin);
  volume = volumeDefault;

  // instantiate callback
  
    ga = gr = boost = attenuation = makeup = cSlope = cThres = 0;
    last_peak = last_gain = 0;
    


  if(programs) setProgram(0);

  setUniqueID(ID);
  setNumInputs(NUM_INPUTS);
  setNumOutputs(NUM_OUTPUTS);
  canProcessReplacing(CAN_PROCESS_REPLACING);
  canMono(CAN_MONO);
}

//-------------------------------------------------------------
Comp::~Comp()
{
  if(programs)
    delete[] programs;

  // deinstantiate callback
  

}

//-------------------------------------------------------------
// Comp information

bool Comp::getEffectName(char *name) {
  strcpy(name, NAME); // name max 32 char
  return true;}

bool Comp::getVendorString(char *text) {
  strcpy(text, VENDOR); // vendor max 64 char
  return true;}

long Comp::canDo(char* text)
	{
  //if (!strcmp (text, "receiveVstEvents")) return 1;
  //if (!strcmp (text, "receiveVstMidiEvent")) return 1;
  return 0; // explicitly can't do; 0 => don't know
}
//-------------------------------------------------------------
void Comp::resume()
{
  
}

void Comp::suspend()
{
  
    last_peak = last_gain = 0;    
    
}

//-------------------------------------------------------------
void Comp::setProgram(long program)
{
  CompProgram *ap = &programs[program];

  curProgram = program;
  setParameter(kattack, ap->fattack);
  setParameter(krelease, ap->frelease);
  setParameter(kthreshold, ap->fthreshold);
  setParameter(kratio, ap->fratio);
  setParameter(kpreamp, ap->fpreamp);
  setParameter(kvolume, ap->fvolume);
}

//-------------------------------------------------------------
void Comp::setProgramName(char *name)
{
  strcpy(programs[curProgram].name, name);
}

//-------------------------------------------------------------
void Comp::getProgramName(char *name)
{
  strcpy(name, programs[curProgram].name);
}

//-------------------------------------------------------------
void Comp::setParameter(long index, float value)
{
  CompProgram *ap = &programs[curProgram];

  switch(index)
  {
    case kattack :
      fattack = ap->fattack = value;
      attack = (float)(value*(attackMax-attackMin)+attackMin);

      // 2.2 is the compensation factor to define attack time as t90-t10
      ga = (float)exp(-2.2/(XSPIF_GET_SAMPLE_RATE()*(attack*0.001))); 
          break;

    case krelease :
      frelease = ap->frelease = value;
      release = (float)(value*(releaseMax-releaseMin)+releaseMin);

      // 2.2 is the compensation factor to define attack time as t90-t10
      gr = (float)exp(-2.2/(XSPIF_GET_SAMPLE_RATE()*(release*0.001)));
          break;

    case kthreshold :
      fthreshold = ap->fthreshold = value;
      threshold = (float)(value*(thresholdMax-thresholdMin)+thresholdMin);

      cThres = pow(10.0,threshold/20);
      makeup = pow(10.0, -(threshold*cSlope)/20.0);
          break;

    case kratio :
      fratio = ap->fratio = value;
      ratio = (float)(value*(ratioMax-ratioMin)+ratioMin);

      cSlope = 1.0 - 1.0/ratio; // 2:1 <-> 40:1
      makeup = pow(10.0, -(threshold*cSlope)/20.0);
          break;

    case kpreamp :
      fpreamp = ap->fpreamp = value;
      preamp = (float)(value*(preampMax-preampMin)+preampMin);

      boost = pow(10.,preamp/20.0);
          break;

    case kvolume :
      fvolume = ap->fvolume = value;
      volume = (float)(value*(volumeMax-volumeMin)+volumeMin);

      attenuation = pow(10.,volume/20.0);
          break;

      default: break;
  }
}

//-------------------------------------------------------------
float Comp::getParameter(long index)
{
  float v = 0.f;

  switch(index)
  {
    case kattack : v = fattack; break;
    case krelease : v = frelease; break;
    case kthreshold : v = fthreshold; break;
    case kratio : v = fratio; break;
    case kpreamp : v = fpreamp; break;
    case kvolume : v = fvolume; break;
    default: break;
  }
  return v;
}

//-------------------------------------------------------------
void Comp::getParameterName(long index, char *label)
{
  switch(index)
  {
    case kattack : strcpy(label, "Attack"); break;
    case krelease : strcpy(label, "Release"); break;
    case kthreshold : strcpy(label, "Threshold"); break;
    case kratio : strcpy(label, "Ratio"); break;
    case kpreamp : strcpy(label, "Preamp"); break;
    case kvolume : strcpy(label, "Volume"); break;
    default: break;
  }
}

//-------------------------------------------------------------
void Comp::getParameterDisplay(long index, char *text)
{
  switch(index)
  {
    case kattack : float2string(attack, text); break;
    case krelease : float2string(release, text); break;
    case kthreshold : float2string(threshold, text); break;
    case kratio : float2string(ratio, text); break;
    case kpreamp : float2string(preamp, text); break;
    case kvolume : float2string(volume, text); break;
    default: break;
  }
}

//-------------------------------------------------------------
void Comp::getParameterLabel(long index, char *label)
{
  switch(index)
  {
    case kattack : strcpy(label, "ms"); break;
    case krelease : strcpy(label, "ms"); break;
    case kthreshold : strcpy(label, "dB"); break;
    case kratio : strcpy(label, " : 1"); break;
    case kpreamp : strcpy(label, "dB"); break;
    case kvolume : strcpy(label, "dB"); break;
    default: break;
  }
}

#define XSPIF_WRITE_SAMPLE(dest,index,source) ((dest)[(index)] += (source))

//-------------------------------------------------------------
void Comp::process(float **inputs, float **outputs, long sampleframes)
{
  float *input1 = inputs[0];
  float *input2 = inputs[1];
  float *output1 = outputs[0];
  float *output2 = outputs[1];
  vector_size = sampleframes;
  
  
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
  
}

#undef XSPIF_WRITE_SAMPLE

#define XSPIF_WRITE_SAMPLE(dest,index,source) ((dest)[(index)] = (source))

//-------------------------------------------------------------
void Comp::processReplacing(float **inputs, float **outputs, long sampleframes)
{
  float *input1 = inputs[0];
  float *input2 = inputs[1];
  float *output1 = outputs[0];
  float *output2 = outputs[1];
  vector_size = sampleframes;

  
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
    
    AudioEffect* effect = new Comp(audioMaster);
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
