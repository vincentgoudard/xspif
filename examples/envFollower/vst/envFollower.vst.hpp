/****************************************************************
XSPIF: cross(X) Standard PlugIn Framework: XSPIF to VST
  envFollower.vst.hpp


This is a simple envelope follower which code was taken from www.musicdsp.org
This example is meant to make use of the control outputs.
    
 This file is generated automatically from the file: envFollower.xspif
 DO NOT EDIT BY HAND
  plugin ID: 'envf'
  manufacturer ID: 'IRCAM'
  maker: Vincent Goudard
  copyright: GPL
 ***************************************************************/

#include "audioeffectx.h"
#include <string.h>

#define XSPIF_GET_SAMPLE_RATE() (sr)
#define XSPIF_GET_VECTOR_SIZE() (vector_size)
#define XSPIF_CONTROL_OUT(label, index, value) (controlOut(label,index,value))

// from envFollower.xspif 
    

//-------------------------------------------------------------
// Parameters constant and declarations

const double e = exp(1.0);

// Attack time
// This is the release time in ms of the envelope follower
const float attackDefault = 10;
const float attackMin = 1;
const float attackMax = 500;


// Release time
// This is the attack time in ms of the envelope follower
const float releaseDefault = 100;
const float releaseMin = 1;
const float releaseMax = 500;

enum
{
  kattack,
  krelease,

  kNumParams
};


//-------------------------------------------------------------
// control out ranges constant and declarations


// Enveloppe value
// This is the envelope value.
const float envMin = 0;
const float envMax = 1;

enum
{
  env,

  kNumControlouts
};


class EnvFollower;

//-------------------------------------------------------------
//EnvFollowerProgram

class EnvFollowerProgram
{
friend class EnvFollower;
public:
  EnvFollowerProgram();
  ~EnvFollowerProgram() {}
private:
  float fattack; // normalized param
  float frelease; // normalized param
  char name[24];
};

//-------------------------------------------------------------
//EnvFollower

class EnvFollower : public AudioEffectX
{
public:
  EnvFollower(audioMasterCallback audioMaster);
  ~EnvFollower();

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
  virtual void canDo(char *text);
  virtual void suspend();

private:
  EnvFollowerProgram *programs;

  // <parameters>
  float attack; // param
  float fattack; // normalized param

  float release; // param
  float frelease; // normalized param

  // </parameters>

  float sr;
  long vector_size;

  // states
  float envelope;
  float attack_coef;
  float release_coef;
};

