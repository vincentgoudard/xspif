/****************************************************************
XSPIF: cross(X) Standard PlugIn Framework: XSPIF to VST
  envFollower.vst.cpp

This is the envelope value. This file is generated automatically from the file: envFollower.xspif
 DO NOT EDIT BY HAND
  plugin ID: 'envf'
  manufacturer ID: 'IRCAM'
  maker: Vincent Goudard
  copyright: GPL
 ***************************************************************/

#include <stdio.h>
#include <string.h>
#include "envFollower.vst.hpp"
//-------------------------------------------------------------
// Config
#define NUM_INPUTS 2
#define NUM_OUTPUTS 0
#define NUM_PRESETS 4
//infos
#define ID 'envf'
#define NAME "Envelope follower"
#define VENDOR "Vincent Goudard"

#define CAN_PROCESS_REPLACING true
#define CAN_MONO true


//-------------------------------------------------------------
// EnvFollowerProgram class implementation

EnvFollowerProgram::EnvFollowerProgram()
{
  fattack = (attackDefault-attackMin)/(attackMax-attackMin);
  frelease = (releaseDefault-releaseMin)/(releaseMax-releaseMin);
  
  strcpy(name,"Envelope follower");
}

//-------------------------------------------------------------
// EnvFollower class implementation

EnvFollower::EnvFollower(audioMasterCallback audioMaster)
: AudioEffectX(audioMaster, NUM_PRESETS, kNumParams)
{
  programs = new EnvFollowerProgram[numPrograms];
  
  sr = getSampleRate();
  if(sr<0.f) sr = 44100.f;

  fattack = (attackDefault-attackMin)/(attackMax-attackMin);
  attack = attackDefault;
  frelease = (releaseDefault-releaseMin)/(releaseMax-releaseMin);
  release = releaseDefault;

  // instantiate callback
  

  if(programs) setProgram(0);

  setUniqueID(ID);
  setNumInputs(NUM_INPUTS);
  setNumOutputs(NUM_OUTPUTS);
  canProcessReplacing(CAN_PROCESS_REPLACING);
  canMono(CAN_MONO);
}

//-------------------------------------------------------------
EnvFollower::~EnvFollower()
{
  if(programs)
    delete[] programs;

  // deinstantiate callback
  

}

//-------------------------------------------------------------
// control out

void EnvFollower::controlout(long label, long index, float value)
{
  char out=0;
  char cc=0;
  switch(label)
  {
    case env :
      cc = 38;
      out = 127*((value-envMin)/(envMax-envMin));

    default: return;
  }

  if(index>vector_size)
    index = vector_size;

  VstMidiEvent vstEvent;
  VstEvents vstEvents; 
  vstEvents.numEvents =1; 
  vstEvents.reserved = 0; 
  vstEvents.events[0] = (VstEvent*)(&vstEvent); 
  vstEvents.events[1]= NULL; 

  memset(&vstEvent, 0, sizeof(vstEvent));
  vstEvent.type = kVstMidiType;
  vstEvent.byteSize = 24;
  vstEvent.deltaFrames = index; 
  vstEvent.midiData[0]=0xb0; // tells it sends midi CC
  vstEvent.midiData[1]=cc; 
  vstEvent.midiData[2]=out; 
  ((AudioEffectX *)this)->sendVstEventsToHost(&vstEvents);
}
//-------------------------------------------------------------
// EnvFollower information

bool EnvFollower::getEffectName(char *name) {
  strcpy(name, NAME); // name max 32 char
  return true;}

bool EnvFollower::getVendorString(char *text) {
  strcpy(text, VENDOR); // vendor max 64 char
  return true;}

long EnvFollower::canDo(char* text)
	{
  if (!strcmp (text, "sendVstMidiEvent")) return 1;
  if (!strcmp (text, "sendVstEvents")) return 1;
  //if (!strcmp (text, "receiveVstEvents")) return 1;
  //if (!strcmp (text, "receiveVstMidiEvent")) return 1;
  return 0; // explicitly can't do; 0 => don't know
}
//-------------------------------------------------------------
void EnvFollower::resume()
{
  wantEvents();
  
}

void EnvFollower::suspend()
{
  
    //clear envelope
    envelope = 0.0;
    
}

//-------------------------------------------------------------
void EnvFollower::setProgram(long program)
{
  EnvFollowerProgram *ap = &programs[program];

  curProgram = program;
  setParameter(kattack, ap->fattack);
  setParameter(krelease, ap->frelease);
}

//-------------------------------------------------------------
void EnvFollower::setProgramName(char *name)
{
  strcpy(programs[curProgram].name, name);
}

//-------------------------------------------------------------
void EnvFollower::getProgramName(char *name)
{
  strcpy(name, programs[curProgram].name);
}

//-------------------------------------------------------------
void EnvFollower::setParameter(long index, float value)
{
  EnvFollowerProgram *ap = &programs[curProgram];

  switch(index)
  {
    case kattack :
      fattack = ap->fattack = value;
      attack = (float)(value*(attackMax-attackMin)+attackMin);

	attack_coef = exp(log(0.01)/( attack * XSPIF_GET_SAMPLE_RATE() * 0.001));
          break;

    case krelease :
      frelease = ap->frelease = value;
      release = (float)(value*(releaseMax-releaseMin)+releaseMin);

	release_coef = exp(log(0.01)/( release * XSPIF_GET_SAMPLE_RATE()  * 0.001));
          break;

      default: break;
  }
}

//-------------------------------------------------------------
float EnvFollower::getParameter(long index)
{
  float v = 0.f;

  switch(index)
  {
    case kattack : v = fattack; break;
    case krelease : v = frelease; break;
    default: break;
  }
  return v;
}

//-------------------------------------------------------------
void EnvFollower::getParameterName(long index, char *label)
{
  switch(index)
  {
    case kattack : strcpy(label, "Attack time"); break;
    case krelease : strcpy(label, "Release time"); break;
    default: break;
  }
}

//-------------------------------------------------------------
void EnvFollower::getParameterDisplay(long index, char *text)
{
  switch(index)
  {
    case kattack : float2string(attack, text); break;
    case krelease : float2string(release, text); break;
    default: break;
  }
}

//-------------------------------------------------------------
void EnvFollower::getParameterLabel(long index, char *label)
{
  switch(index)
  {
    case kattack : strcpy(label, "ms"); break;
    case krelease : strcpy(label, "ms"); break;
    default: break;
  }
}

#define XSPIF_WRITE_SAMPLE(dest,index,source) ((dest)[(index)] += (source))

//-------------------------------------------------------------
void EnvFollower::process(float **inputs, float **outputs, long sampleframes)
{
  float *input1 = inputs[0];
  float *input2 = inputs[1];
  vector_size = sampleframes;


    float tmp;
    int i = 0;
    for(i=0; i < XSPIF_GET_VECTOR_SIZE(); i++)
    {
	tmp = fabs(input1[i]) + fabs(input2[i]);
	if(tmp >  envelope)
		envelope = attack_coef * (envelope - tmp) + tmp;
	else
		envelope = release_coef * (envelope - tmp) + tmp;
    }
    XSPIF_CONTROL_OUT(env, 0, envelope);
    
}

#undef XSPIF_WRITE_SAMPLE

#define XSPIF_WRITE_SAMPLE(dest,index,source) ((dest)[(index)] = (source))

//-------------------------------------------------------------
void EnvFollower::processReplacing(float **inputs, float **outputs, long sampleframes)
{
  float *input1 = inputs[0];
  float *input2 = inputs[1];
  vector_size = sampleframes;


    float tmp;
    int i = 0;
    for(i=0; i < XSPIF_GET_VECTOR_SIZE(); i++)
    {
	tmp = fabs(input1[i]) + fabs(input2[i]);
	if(tmp >  envelope)
		envelope = attack_coef * (envelope - tmp) + tmp;
	else
		envelope = release_coef * (envelope - tmp) + tmp;
    }
    XSPIF_CONTROL_OUT(env, 0, envelope);
    
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

  AudioEffect* effect = new EnvFollower (audioMaster);
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

